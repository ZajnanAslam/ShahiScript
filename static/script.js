document.addEventListener('DOMContentLoaded', () => {
    const parseBtn = document.getElementById('parse-btn');
    const codeEditor = document.getElementById('code-editor');
    const errorBox = document.getElementById('error-box');
    const tokensContainer = document.getElementById('tokens-container');
    const astContainer = document.getElementById('ast-container');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Tabs logic
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    parseBtn.addEventListener('click', async () => {
        const code = codeEditor.value;
        parseBtn.textContent = 'Parsing...';
        errorBox.classList.add('hidden');
        
        try {
            const res = await fetch('/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            const data = await res.json();
            
            if (data.success) {
                renderTokens(data.tokens);
                renderAST(data.ast);
            } else {
                showError(data.error);
            }
        } catch (e) {
            showError("Network or Server error.");
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
        
        const width = 800;
        const dx = 50;
        const dy = width / 6;
        const margin = {top: 20, right: 120, bottom: 20, left: 120};

        const tree = d3.tree().nodeSize([dx, dy]);
        const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

        const root = d3.hierarchy(hierarchyData);
        root.x0 = dy / 2;
        root.y0 = 0;
        root.descendants().forEach((d, i) => {
            d.id = i;
            d._children = d.children;
        });

        const svg = d3.select("#ast-container").append("svg")
            .attr("width", width)
            .attr("height", dx)
            .attr("viewBox", [-margin.left, -margin.top, width, dx])
            .style("max-width", "100%")
            .style("height", "auto")
            .style("font", "12px sans-serif")
            .style("user-select", "none");

        const gLink = svg.append("g")
            .attr("fill", "none")
            .attr("stroke", "#d4af37")
            .attr("stroke-opacity", 0.4)
            .attr("stroke-width", 1.5);

        const gNode = svg.append("g")
            .attr("cursor", "pointer")
            .attr("pointer-events", "all");

        function update(source) {
            const duration = 250;
            const nodes = root.descendants().reverse();
            const links = root.links();

            tree(root);

            let left = root;
            let right = root;
            root.eachBefore(node => {
                if (node.x < left.x) left = node;
                if (node.x > right.x) right = node;
            });

            const height = right.x - left.x + margin.top + margin.bottom;
            const transition = svg.transition().duration(duration)
                .attr("height", height)
                .attr("viewBox", [-margin.left, left.x - margin.top, width, height])
                .tween("resize", window.ResizeObserver ? null : () => () => svg.dispatch("toggle"));

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
