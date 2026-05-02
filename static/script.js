document.addEventListener('DOMContentLoaded', () => {
    const pageCode = document.getElementById('page-code');
    const pageVisualizer = document.getElementById('page-visualizer');
    
    const parseBtn = document.getElementById('parse-btn');
    const backBtn = document.getElementById('back-btn');
    const viewAstBtn = document.getElementById('view-ast-btn');
    const exampleSelect = document.getElementById('example-select');
    
    const codeEditor = document.getElementById('code-editor');
    const stdInput = document.getElementById('std-input');
    const errorBox = document.getElementById('error-box');
    const tokensContainer = document.getElementById('tokens-container');
    const astContainer = document.getElementById('ast-container');
    const executionOutput = document.getElementById('execution-output');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // View Switching Logic
    function showVisualizer() {
        pageCode.classList.remove('active');
        pageCode.classList.add('hidden');
        pageVisualizer.classList.remove('hidden');
        pageVisualizer.classList.add('active');
    }

    function showCodeEditor() {
        pageVisualizer.classList.remove('active');
        pageVisualizer.classList.add('hidden');
        pageCode.classList.remove('hidden');
        pageCode.classList.add('active');
    }

    backBtn.addEventListener('click', showCodeEditor);
    viewAstBtn.addEventListener('click', showVisualizer);

    // Tabs logic
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // Example selector logic
    exampleSelect.addEventListener('change', (e) => {
        const val = e.target.value;
        if (val !== 'custom' && examplesData[val]) {
            codeEditor.value = examplesData[val];
        } else if (val === 'custom') {
            codeEditor.value = `Bismillah\n    // Enter your custom royal decree here\nAllahHafiz`;
        }
    });

    parseBtn.addEventListener('click', async () => {
        const code = codeEditor.value;
        const stdin = stdInput.value;
        parseBtn.textContent = 'Running...';
        errorBox.classList.add('hidden');
        
        try {
            const res = await fetch('/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, stdin })
            });
            const data = await res.json();

            if (data.success) {
                renderTokens(data.tokens);
                renderAST(data.ast);
                executionOutput.textContent = data.output || "No output generated.";
            } else {
                showError(data.error);
                // Also show error in execution output for visibility
                executionOutput.textContent = "Error:\n" + data.error;
            }
        } catch (e) {
            showError("Network or Server error.");
            executionOutput.textContent = "Network or Server error.";
        }
        
        parseBtn.textContent = 'Issue Decree';
    });

    function showError(msg) {
        errorBox.textContent = msg;
        errorBox.classList.remove('hidden');
        tokensContainer.innerHTML = '';
        astContainer.innerHTML = '';
    }

    function renderTokens(tokens) {
        tokensContainer.innerHTML = tokens.map(t => 
            `<span class="token-item">
                <span class="token-type">${t.type}</span>: 
                <span class="token-val">${t.value}</span>
            </span>`
        ).join('');
    }

    function buildHierarchy(node, name="Program") {
        if (!node) return { name: "null" };
        if (Array.isArray(node)) {
            return { name: "List", children: node.map((n, i) => buildHierarchy(n, `[${i}]`)) };
        }
        if (typeof node === 'object') {
            let type = node.type || name;
            let children = [];
            for (let [key, val] of Object.entries(node)) {
                if (key === 'type') continue;
                if (typeof val === 'object') {
                    children.push(buildHierarchy(val, key));
                } else {
                    children.push({ name: `${key}: ${val}` });
                }
            }
            return { name: type, children: children.length ? children : null };
        }
        return { name: String(node) };
    }

    function renderAST(astData) {
        astContainer.innerHTML = ''; // Clear previous
        const hierarchyData = buildHierarchy(astData);
        
        const dx = 50;
        const dy = 150; // fixed horizontal distance between nodes

        const tree = d3.tree().nodeSize([dx, dy]);
        const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

        const root = d3.hierarchy(hierarchyData);
        root.x0 = 0;
        root.y0 = 0;
        root.descendants().forEach((d, i) => {
            d.id = i;
            d._children = d.children;
        });

        // Setup SVG
        const containerRect = astContainer.getBoundingClientRect();
        const width = containerRect.width || 800;
        const height = containerRect.height || 600;

        const svg = d3.select("#ast-container").append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .style("font", "12px sans-serif")
            .style("user-select", "none");

        // The group containing everything that moves with zoom
        const g = svg.append("g");

        // Zoom setup
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => {
                g.attr("transform", event.transform);
            });

        svg.call(zoom);

        // Center the root node initially
        const initialTransform = d3.zoomIdentity.translate(width / 4, height / 2).scale(1);
        svg.call(zoom.transform, initialTransform);

        const gLink = g.append("g")
            .attr("fill", "none")
            .attr("stroke", "#d4af37")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 1.5);

        const gNode = g.append("g")
            .attr("cursor", "pointer")
            .attr("pointer-events", "all");

        function update(source) {
            const duration = 250;
            const nodes = root.descendants().reverse();
            const links = root.links();

            tree(root);

            const transition = svg.transition().duration(duration);

            const node = gNode.selectAll("g")
                .data(nodes, d => d.id);

            const nodeEnter = node.enter().append("g")
                .attr("transform", d => `translate(${source.y0},${source.x0})`)
                .attr("fill-opacity", 0)
                .attr("stroke-opacity", 0)
                .on("click", (event, d) => {
                    d.children = d.children ? null : d._children;
                    update(d);
                });

            nodeEnter.append("circle")
                .attr("r", 5)
                .attr("fill", d => d._children ? "#555" : "#999")
                .attr("stroke", "#d4af37")
                .attr("stroke-width", 2);

            nodeEnter.append("text")
                .attr("dy", "0.31em")
                .attr("x", d => d._children ? -8 : 8)
                .attr("text-anchor", d => d._children ? "end" : "start")
                .text(d => d.data.name)
                .attr("fill", "#f0e6d2")
                .attr("stroke", "rgba(0,0,0,0.5)")
                .attr("stroke-width", 0.5);

            const nodeUpdate = node.merge(nodeEnter).transition(transition)
                .attr("transform", d => `translate(${d.y},${d.x})`)
                .attr("fill-opacity", 1)
                .attr("stroke-opacity", 1);

            const nodeExit = node.exit().transition(transition).remove()
                .attr("transform", d => `translate(${source.y},${source.x})`)
                .attr("fill-opacity", 0)
                .attr("stroke-opacity", 0);

            const link = gLink.selectAll("path")
                .data(links, d => d.target.id);

            const linkEnter = link.enter().append("path")
                .attr("d", d => {
                    const o = {x: source.x0, y: source.y0};
                    return diagonal({source: o, target: o});
                });

            link.merge(linkEnter).transition(transition)
                .attr("d", diagonal);

            link.exit().transition(transition).remove()
                .attr("d", d => {
                    const o = {x: source.x, y: source.y};
                    return diagonal({source: o, target: o});
                });

            root.eachBefore(d => {
                d.x0 = d.x;
                d.y0 = d.y;
            });
        }
        update(root);
    }
});
