# ==============================================
# KALKULATOR MASSA SENYAWA 
# ==============================================

# Kamus massa atom unsur periodik (1–118) dalam satuan g/mol
massa_atom = {
    "H":1.008,"He":4.0026,"Li":6.94,"Be":9.0122,"B":10.81,"C":12.011,"N":14.007,"O":15.999,"F":18.998,"Ne":20.180,
    "Na":22.990,"Mg":24.305,"Al":26.982,"Si":28.085,"P":30.974,"S":32.06,"Cl":35.45,"Ar":39.948,"K":39.098,"Ca":40.078,
    "Sc":44.956,"Ti":47.867,"V":50.942,"Cr":51.996,"Mn":54.938,"Fe":55.845,"Co":58.933,"Ni":58.693,"Cu":63.546,"Zn":65.38,
    "Ga":69.723,"Ge":72.630,"As":74.922,"Se":78.971,"Br":79.904,"Kr":83.798,"Rb":85.468,"Sr":87.62,"Y":88.906,"Zr":91.224,
    "Nb":92.906,"Mo":95.95,"Tc":98,"Ru":101.07,"Rh":102.91,"Pd":106.42,"Ag":107.87,"Cd":112.41,"In":114.82,"Sn":118.71,
    "Sb":121.76,"Te":127.60,"I":126.90,"Xe":131.29,"Cs":132.91,"Ba":137.33,"La":138.91,"Ce":140.12,"Pr":140.91,"Nd":144.24,
    "Pm":145,"Sm":150.36,"Eu":151.96,"Gd":157.25,"Tb":158.93,"Dy":162.50,"Ho":164.93,"Er":167.26,"Tm":168.93,"Yb":173.05,
    "Lu":174.97,"Hf":178.49,"Ta":180.95,"W":183.84,"Re":186.21,"Os":190.23,"Ir":192.22,"Pt":195.08,"Au":196.97,"Hg":200.59,
    "Tl":204.38,"Pb":207.2,"Bi":208.98,"Po":209,"At":210,"Rn":222,"Fr":223,"Ra":226,"Ac":227,"Th":232.04,
    "Pa":231.04,"U":238.03,"Np":237,"Pu":244,"Am":243,"Cm":247,"Bk":247,"Cf":251,"Es":252,"Fm":257,
    "Md":258,"No":259,"Lr":266,"Rf":267,"Db":268,"Sg":269,"Bh":270,"Hs":269,"Mt":278,"Ds":281,
    "Rg":282,"Cn":285,"Nh":286,"Fl":289,"Mc":290,"Lv":293,"Ts":294,"Og":294
}

import re

# ----------------------------------------------
# FUNGSI — perbaiki huruf & buang spasi/dot/·
# ----------------------------------------------
def normalize_formula(formula: str) -> str:
    # Hapus spasi
    formula = formula.replace(" ", "")
    # Samakan dot & middle dot menjadi titik
    formula = formula.replace("·", ".")
    # Koreksi kapitalisasi unsur (regex: kelompok huruf besar-kecil-angka)
    # Ubahlah huruf awal unsur menjadi kapital, huruf kedua (jika ada) menjadi kecil
    def fix_token(m):
        token = m.group(0)
        if token[0].isalpha():
            if len(token) == 1:
                return token.upper()
            elif token[1].isalpha():
                return token[0].upper() + token[1:].lower()
        return token
    formula = re.sub(r"[A-Za-z]{1,2}", fix_token, formula)
    return formula

# ----------------------------------------------
# FUNGSI — hitung massa satu fragmen (tanpa titik)
# ----------------------------------------------
def molar_mass_segment(segment: str) -> float:
    # Dukungan kurung (), [], {}
    stack = [0]
    i = 0
    while i < len(segment):
        if segment[i] in "([{":
            stack.append(0)
            i += 1
        elif segment[i] in ")]}":
            val = stack.pop()
            i += 1
            num = ""
            while i < len(segment) and segment[i].isdigit():
                num += segment[i]
                i += 1
            mul = int(num) if num else 1
            stack[-1] += val * mul
        else:
            if segment[i].isupper():
                elem = segment[i]
                i += 1
                if i < len(segment) and segment[i].islower():
                    elem += segment[i]
                    i += 1
                num = ""
                while i < len(segment) and segment[i].isdigit():
                    num += segment[i]
                    i += 1
                cnt = int(num) if num else 1
                if elem not in massa_atom:
                    raise ValueError(f"Unsur tidak dikenal: {elem}")
                stack[-1] += massa_atom[elem] * cnt
            else:
                raise ValueError("Format rumus tidak valid")
    if len(stack) != 1:
        raise ValueError("Kurung tidak seimbang")
    return stack[0]

# ----------------------------------------------
# FUNGSI — hitung massa total dengan titik hidrat
# ----------------------------------------------
def molar_mass(formula: str) -> float:
    parts = formula.split(".")
    total = 0
    for part in parts:
        if part == "":
            continue
        total += molar_mass_segment(part)
    return total

# ==============================================
# BAGIAN 2 — PROGRAM UTAMA, MENU, DAN KONVERSI
# ==============================================

def compute_total_molar_mass(normalized_formula: str) -> float:
    """
    Menghitung massa molar total dari formula yang sudah dinormalisasi.
    Mendukung bagian terpisah oleh '.' (titik) sebagai hidrasi/multiple segments,
    serta segmen yang diawali angka multiplikator seperti '5H2O'.
    Fungsi ini memakai molar_mass_segment untuk menghitung tiap segmen.
    """
    if normalized_formula == "":
        raise ValueError("Formula kosong setelah normalisasi.")
    parts = normalized_formula.split(".")
    total = 0.0
    for part in parts:
        if part == "":
            # lewati segmen kosong (misal input .. tidak valid tapi kita skip)
            continue
        # cek apakah part diawali angka multiplier
        m = re.match(r'^(\d+)(.+)$', part)
        if m:
            mult = int(m.group(1))
            seg = m.group(2)
            if seg == "":
                raise ValueError(f"Segmen '{part}' tidak valid (tidak ada formula setelah angka).")
        else:
            mult = 1
            seg = part
        # hitung massa segmen
        seg_mass = molar_mass_segment(seg)  # fungsi dari BAGIAN 1
        total += seg_mass * mult
    return total

def input_formula_loop():
    """
    Loop input formula: minta input, normalisasi, validasi parsing.
    Jika parsing gagal, tampil pesan error dan minta ulang (sesuai opsi B).
    Mengembalikan string formula yang dinormalisasi (untuk ditampilkan sama user).
    """
    while True:
        raw = input("Masukkan rumus senyawa (contoh: CuSO4·5H2O atau Ca(OH)2): ").strip()
        # hapus spasi dan perbaiki kapitalisasi
        try:
            normalized = normalize_formula(raw)  # fungsi dari BAGIAN 1
            # uji parsing minimal: coba hitung massa (untuk validasi)
            # compute_total_molar_mass akan melempar ValueError jika salah
            _ = compute_total_molar_mass(normalized)
            return raw, normalized  # kembalikan raw (untuk ditampilkan) dan normalized (untuk perhitungan)
        except ValueError as e:
            print("Error pada rumus yang dimasukkan:", e)
            print("Silakan coba lagi.\n")

def prompt_mode_loop():
    """
    Minta pilihan mode konversi (1 atau 2). Ulang jika input tidak valid.
    """
    print("\nPilih mode konversi:")
    print("  1 = mol -> gram")
    print("  2 = gram -> mol")
    while True:
        choice = input("Masukkan pilihan (1/2): ").strip()
        if choice in ('1', '2'):
            return choice
        print("Pilihan tidak valid. Ketik '1' atau '2'.")

def input_positive_number(prompt_text: str) -> float:
    """
    Minta input angka (float) > = 0. Jika input salah, minta ulang.
    """
    while True:
        s = input(prompt_text).strip()
        try:
            val = float(s)
            if val < 0:
                print("Angka tidak boleh negatif. Silakan ulangi.")
                continue
            return val
        except ValueError:
            print("Input tidak valid. Masukkan angka (contoh: 0.5 atau 36).")

def print_table_molar_result(raw_formula: str, normalized_formula: str, mm: float, input_amount: float, result_amount: float, mode: str):
    """
    Tampilkan hasil dalam gaya tabel sesuai pilihan B.
    Jika mode == '1', input_amount adalah mol dan result_amount adalah gram.
    Jika mode == '2', input_amount adalah gram dan result_amount adalah mol.
    """
    print("\n" + "-"*40)
    print(f"Rumus (input)    : {raw_formula}")
    print(f"Rumus (normalized): {normalized_formula}")
    print(f"Massa molar      : {mm:.5f} g/mol")
    if mode == '1':
        print(f"Massa input      : {input_amount:.5f} mol")
        print(f"Hasil konversi   : {result_amount:.5f} gram")
    else:
        print(f"Massa input      : {input_amount:.5f} gram")
        print(f"Hasil konversi   : {result_amount:.5f} mol")
    print("-"*40 + "\n")

def main():
    print("=== Kalkulator Massa Molar (Kelompok 1)===")
    print("Fitur:")
    print("- Support kurung (), [], {} dan nested")
    print("- Support hidrasi/multi-dot (titik '.' atau '·') dan segmen berawalan angka (misal '5H2O')")
    print("- Normalisasi kapitalisasi (misal 'cuSO4' -> 'CuSO4')\n")

    # 1) Input formula dengan loop validasi
    raw_formula, normalized_formula = input_formula_loop()

    # 2) Hitung massa molar total (g/mol)
    try:
        mm = compute_total_molar_mass(normalized_formula)
    except ValueError as e:
        # Seharusnya tidak terjadi karena sudah divalidasi, tapi hanya jaga-jaga
        print("Terjadi kesalahan saat menghitung massa molar:", e)
        print("Program akan keluar.")
        return

    # 3) Pilih mode konversi
    mode = prompt_mode_loop()

    if mode == '1':
        # mol -> gram
        mol = input_positive_number("Masukkan jumlah mol (contoh: 0.5 atau 2): ")
        grams = mol * mm
        print_table_molar_result(raw_formula, normalized_formula, mm, mol, grams, mode='1')
    else:
        # gram -> mol
        grams = input_positive_number("Masukkan massa dalam gram (contoh: 36 atau 0.5): ")
        mol = grams / mm if mm != 0 else float('inf')
        print_table_molar_result(raw_formula, normalized_formula, mm, grams, mol, mode='2')

    # Setelah satu kali perhitungan, program selesai
    print("Perhitungan selesai. Program keluar.")
    return

if __name__ == "__main__":
    main()