# NAMA: VALDO
# NAMA ISTRI VALDO: MAHIRU SHIINA
# ==============================================
# KALKULATOR MASSA SENYAWA 
# ==============================================

import streamlit as st
import re
from PIL import Image
# ====== Kamus massa atom ======
massa_atom = {
    "H":1.008,"He":4.0026,"Li":6.94,"Be":9.0122,"B":10.81,"C":12.011,"N":14.007,"O":15.999,
    "F":18.998,"Ne":20.180,"Na":22.990,"Mg":24.305,"Al":26.982,"Si":28.085,"P":30.974,"S":32.06,
    "Cl":35.45,"Ar":39.948,"K":39.098,"Ca":40.078,"Sc":44.956,"Ti":47.867,"V":50.942,"Cr":51.996,
    "Mn":54.938,"Fe":55.845,"Co":58.933,"Ni":58.693,"Cu":63.546,"Zn":65.38,"Ga":69.723,"Ge":72.630,
    "As":74.922,"Se":78.971,"Br":79.904,"Kr":83.798,"Rb":85.468,"Sr":87.62,"Y":88.906,"Zr":91.224,
    "Nb":92.906,"Mo":95.95,"Tc":98,"Ru":101.07,"Rh":102.91,"Pd":106.42,"Ag":107.87,"Cd":112.41,
    "In":114.82,"Sn":118.71,"Sb":121.76,"Te":127.60,"I":126.90,"Xe":131.29,"Cs":132.91,"Ba":137.33,
    "La":138.91,"Ce":140.12,"Pr":140.91,"Nd":144.24,"Pm":145,"Sm":150.36,"Eu":151.96,"Gd":157.25,
    "Tb":158.93,"Dy":162.50,"Ho":164.93,"Er":167.26,"Tm":168.93,"Yb":173.05,"Lu":174.97,"Hf":178.49,
    "Ta":180.95,"W":183.84,"Re":186.21,"Os":190.23,"Ir":192.22,"Pt":195.08,"Au":196.97,"Hg":200.59,
    "Tl":204.38,"Pb":207.2,"Bi":208.98,"Po":209,"At":210,"Rn":222,"Fr":223,"Ra":226,"Ac":227,
    "Th":232.04,"Pa":231.04,"U":238.03,"Np":237,"Pu":244,"Am":243,"Cm":247,"Bk":247,"Cf":251,
    "Es":252,"Fm":257,"Md":258,"No":259,"Lr":266,"Rf":267,"Db":268,"Sg":269,"Bh":270,"Hs":269,
    "Mt":278,"Ds":281,"Rg":282,"Cn":285,"Nh":286,"Fl":289,"Mc":290,"Lv":293,"Ts":294,"Og":294
}

# ====== Fungsi normalisasi ======
def normalize_formula(formula: str) -> str:
    formula = formula.replace(" ", "").replace("·", ".").lower()
    i = 0
    hasil = ""
    while i < len(formula):
        if i + 1 < len(formula) and (formula[i].upper() + formula[i+1].lower()) in massa_atom:
            hasil += formula[i].upper() + formula[i+1].lower()
            i += 2
        elif formula[i].upper() in massa_atom:
            hasil += formula[i].upper()
            i += 1
        else:
            hasil += formula[i]
            i += 1
    return hasil

# ====== Hitung massa segmen ======
def molar_mass_segment(segment: str) -> float:
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
                raise ValueError("Format rumus tidak valid.")
    if len(stack) != 1:
        raise ValueError("Kurung tidak seimbang.")
    return stack[0]

# ====== Hitung massa total ======
def compute_total_molar_mass(formula: str) -> float:
    total = 0
    for part in formula.split("."):
        if not part:
            continue
        m = re.match(r"^(\d+)(.+)$", part)
        if m:
            mult = int(m.group(1))
            part = m.group(2)
        else:
            mult = 1
        total += molar_mass_segment(part) * mult
    return total

# ====== Streamlit UI ======
st.set_page_config(page_title="Kalkulator Massa Senyawa", layout="centered")

# Judul web di atas header
st.title("🧪 Kalkulator Massa Senyawa")

# Header Image
img = Image.open("images/mahiru.jpg")  # path sesuai folder proyek
st.image(img, use_container_width=True)

# Deskripsi
st.write("Masukkan rumus senyawa kimia (misal: CuSO4·5H2O atau H2O) dan pilih konversi:")

# Input rumus
raw_formula = st.text_input("Rumus Senyawa", "")

# Pilih mode konversi
mode = st.radio("Pilih Mode Konversi:", ("Mol → Gram", "Gram → Mol"))

# Input jumlah mol/gram dengan 10 digit desimal
if mode == "Mol → Gram":
    input_amount = st.number_input("Jumlah Mol", min_value=0.0, value=1.0, step=0.1, format="%.10f")
else:
    input_amount = st.number_input("Jumlah Gram", min_value=0.0, value=1.0, step=0.1, format="%.10f")

# Tombol Hitung
if st.button("Hitung"):
    try:
        normalized_formula = normalize_formula(raw_formula)
        mm = compute_total_molar_mass(normalized_formula)
        if mode == "Mol → Gram":
            result = input_amount * mm
            st.success(f"Massa molar: {mm:.5f} g/mol")
            st.info(f"{input_amount:.10f} mol → {result:.10f} gram")
        else:
            result = input_amount / mm
            st.success(f"Massa molar: {mm:.5f} g/mol")
            st.info(f"{input_amount:.10f} gram → {result:.10f} mol")
    except ValueError as e:
        st.error(f"❌ Error: {e}")
