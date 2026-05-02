from lexer import tokenize

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
        tokens = tokenize(code)
        for token in tokens:
            print(token)
    except Exception as e:
        print(e)
