# ShahiScript Language Reference Manual

ShahiScript is a retro-inspired, high-level educational programming language that replaces standard keywords with regal Urdu/Persian vocabulary.

## General Structure
Every script **must** begin with `Bismillah` and end with `AllahHafiz`.

```
Bismillah
    // Your code here
AllahHafiz
```

## Data Types
Variables are declared using the `daulat` keyword. They can be prefixed with a type constraint for clarity:
- `adad` (Integer)
- `ashariya` (Float)
- `jumla` (String)
- `haqeeqat` (Boolean: `sach` or `ghalat`)
- `fehrist` (Array)

Example:
`adad daulat age = 25;`

## Conditionals
Use `agar` (if), `warna_agar` (else if), and `varna` (else). All blocks must be closed with `khatam;`.

```
agar (x > 10) phir
    farman "Greater";
khatam;
warna_agar (x == 10) phir
    farman "Equal";
khatam;
varna
    farman "Lesser";
khatam;
```

## Loops
### While Loop (`jab_tak`)
```
jab_tak (x < 5) phir
    x = x + 1;
khatam;
```

### For Loop (`har`)
```
har (adad daulat i = 0; i < 5; i = i + 1) phir
    farman i;
khatam;
```

### Do-While Loop (`dohrao`)
```
dohrao {
    farman "Once!";
} jab_tak (ghalat);
```

## Functions
Define functions with `hukam` and return values with `waapsi`.
```
hukam add(a, b) {
    waapsi a + b;
}
```

## I/O
- Output: `farman "Message";`
- Input: `jumla daulat name = darkhwast("Enter name: ");`
