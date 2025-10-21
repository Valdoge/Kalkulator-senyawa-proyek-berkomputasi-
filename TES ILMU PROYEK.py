import re
import sys

# Kamus massa atom (g/mol) — elemen 1..118 (nilai umum/pendekatan)
MASS = {
 "H":1.008,"He":4.0026,"Li":6.94,"Be":9.0122,"B":10.81,"C":12.011,"N":14.007,"O":15.999,"F":18.998,"Ne":20.180,
 "Na":22.990,"Mg":24.305,"Al":26.982,"Si":28.085,"P":30.974,"S":32.06,"Cl":35.45,"Ar":39.948,"K":39.098,"Ca":40.078,
 "Sc":44.956,"Ti":47.867,"V":50.942,"Cr":51.996,"Mn":54.938,"Fe":55.845,"Co":58.933,"Ni":58.693,"Cu":63.546,"Zn":65.38,
 "Ga":69.723,"Ge":72.630,"As":74.922,"Se":78.971,"Br":79.904,"Kr":83.798,"Rb":85.468,"Sr":87.62,"Y":88.906,"Zr":91.224,
 "Nb":92.906,"Mo":95.95,"Tc":98.0,"Ru":101.07,"Rh":102.91,"Pd":106.42,"Ag":107.87,"Cd":112.41,"In":114.82,"Sn":118.71,
 "Sb":121.76,"Te":127.60,"I":126.90,"Xe":131.29,"Cs":132.91,"Ba":137.33,"La":138.91,"Ce":140.12,"Pr":140.91,"Nd":144.24,
 "Pm":145.0,"Sm":150.36,"Eu":151.96,"Gd":157.25,"Tb":158.93,"Dy":162.50,"Ho":164.93,"Er":167.26,"Tm":168.93,"Yb":173.05,
 "Lu":174.97,"Hf":178.49,"Ta":180.95,"W":183.84,"Re":186.21,"Os":190.23,"Ir":192.22,"Pt":195.08,"Au":196.97,"Hg":200.59,
 "Tl":204.38,"Pb":207.2,"Bi":208.98,"Po":209.0,"At":210.0,"Rn":222.0,"Fr":223.0,"Ra":226.0,"Ac":227.0,"Th":232.04,
 "Pa":231.04,"U":238.03,"Np":237.0,"Pu":244.0,"Am":243.0,"Cm":247.0,"Bk":247.0,"Cf":251.0,"Es":252.0,"Fm":257.0,
 "Md":258.0,"No":259.0,"Lr":266.0,"Rf":267.0,"Db":268.0,"Sg":269.0,"Bh":270.0,"Hs":277.0,"Mt":278.0,"Ds":281.0,
 "Rg":282.0,"Cn":285.0,"Nh":286.0,"Fl":289.0,"Mc":290.0,"Lv":293.0,"Ts":294.0,"Og":294.0
}

# Tokenizer: elemen, angka, atau bracket
TOKEN_RE = re.compile(r'([A-Z][a-z]?|\d+|[\(\)\[\]\{\}])')

# Mapping closers to openers
OPENERS = {'(':')','[':']','{':'}'}
CLOSERS = {v:k for k,v in OPENERS.items()}

def parse_formula(formula: str):
    """
    Parse chemical formula into dict {element: count}.
    Supports nested (), [], {} and multipliers.
    Raises ValueError on invalid token or mismatched parentheses or unknown element.
    """
    tokens = TOKEN_RE.findall(formula)
    if ''.join(tokens) != formula.replace(" ", ""):
        raise ValueError("Formula contains invalid characters or spacing.")
    stack = [ {} ]  # stack of dicts; top is current group
    opener_stack = []  # track openers for mismatch detection
    i = 0
    while i < len(tokens):
        tk = tokens[i]
        if tk in OPENERS:
            # start new group
            stack.append({})
            opener_stack.append(tk)
            i += 1
        elif tk in CLOSERS:
            # end group: pop top, apply multiplier if present
            if not opener_stack:
                raise ValueError(f"Unmatched closer {tk} at position {i}")
            last_opener = opener_stack.pop()
            expected_closer = OPENERS[last_opener]
            if tk != expected_closer:
                raise ValueError(f"Mismatched bracket: expected {expected_closer} but found {tk}")
            group = stack.pop()
            i += 1
            # check if next token is number multiplier
            mult = 1
            if i < len(tokens) and tokens[i].isdigit():
                mult = int(tokens[i]); i += 1
            # add into new top
            top = stack[-1]
            for el, cnt in group.items():
                top[el] = top.get(el, 0) + cnt * mult
        elif re.fullmatch(r'\d+', tk):
            # A number token here is multiplier for previous element — but previous should be element
            # This case should be handled immediately after element; encountering standalone number is error
            raise ValueError(f"Unexpected standalone number '{tk}' in formula at token index {i}")
        else:
            # element symbol
            el = tk
            # validate element known
            if el not in MASS:
                raise ValueError(f"Unknown element symbol: {el}")
            i += 1
            cnt = 1
            if i < len(tokens) and tokens[i].isdigit():
                cnt = int(tokens[i]); i += 1
            top = stack[-1]
            top[el] = top.get(el, 0) + cnt
    if opener_stack:
        raise ValueError("Mismatched parentheses/brackets: some openers not closed.")
    return stack[0]

def molar_mass_from_counts(counts: dict):
    total = 0.0
    for el, cnt in counts.items():
        total += MASS[el] * cnt
    return total

def main():
    print("Kalkulator Massa Molar — support (), [], {} dan nested. (Mode: input mol → hasil gram)")
    print("Contoh rumus: H2O, Ca(OH)2, K4[Fe(CN)6], Al2(SO4)3")
    formula = input("Masukkan rumus senyawa: ").strip()
    try:
        counts = parse_formula(formula)
    except ValueError as e:
        print("Error parsing formula:", e)
        sys.exit(1)
    mm = molar_mass_from_counts(counts)
    print("\nKomposisi terurai:")
    for el, cnt in sorted(counts.items()):
        print(f"  {el}: {cnt} atom")
    print(f"\nMassa molar {formula} = {mm:.5f} g/mol")
    # mode B: minta jumlah mol lalu konversi ke gram
    while True:
        try:
            mol = float(input("Masukkan jumlah mol (atau ketik 0 untuk selesai): "))
            if mol < 0:
                print("Jumlah mol tidak boleh negatif.")
                continue
            grams = mol * mm
            print(f"{mol} mol {formula} = {grams:.5f} gram")
            break
        except ValueError:
            print("Masukkan angka yang valid untuk mol.")

if __name__ == "__main__":
    main()