from lexer import tokenize
from parser import parse
import json

code = """Bismillah
    hukam greet(name) {
        farman name;
        waapsi sach;
    }
    
    jumla daulat user_name = darkhwast("What is your name?");
    greet(user_name);

    adad daulat i = 0;
    jab_tak (i < 5) phir
        farman i;
        i = i + 1;
    khatam;

    fehrist daulat items = [1, 2, 3];

    har (adad daulat j = 0; j < 3; j = j + 1) phir
        agar (j == 1) phir
            farman "One";
        khatam;
        warna_agar (j == 2) phir
            farman "Two";
        khatam;
        varna
            farman "Other";
        khatam;
    khatam;

    dohrao {
        farman "Repeat!";
    } jab_tak (ghalat);
AllahHafiz"""

if __name__ == "__main__":
    try:
        print("Tokenizing...")
        tokens = tokenize(code)
        print(f"Found {len(tokens)} tokens.")
        
        print("Parsing...")
        ast = parse(tokens)
        print(json.dumps(ast, indent=2))
    except Exception as e:
        print(e)
