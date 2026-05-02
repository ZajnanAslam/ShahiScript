from lexer import tokenize

code = """Bismillah
    daulat x = 10;
    agar (x > 5) phir
        farman "Success";
    khatam;
AllahHafiz"""

if __name__ == "__main__":
    try:
        tokens = tokenize(code)
        for token in tokens:
            print(token)
    except Exception as e:
        print(e)
