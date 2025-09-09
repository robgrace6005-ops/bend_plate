import math
import streamlit as st

st.set_page_config(page_title="Bend Plate Capacity", page_icon="🛠️", layout="centered")

st.title("🛠️ Plate Bending & Shear Check (AS 4100:2020)")
st.caption("Note: Inputs are unfactored working loads and moments.")

# --- Inputs ---
b = st.number_input("Plate width b (mm)", min_value=1.0, value=200.0, step=1.0)
t = st.number_input("Plate thickness t (mm)", min_value=1.0, value=10.0, step=0.1)
M_kNm = st.number_input("Applied bending moment M (kNm)", min_value=0.0, value=50.0, step=1.0)
P_kN = st.number_input("Applied total load P (kN)", min_value=0.0, value=100.0, step=1.0)
fy = st.number_input("Steel yield strength fy (MPa)", min_value=100.0, value=250.0, step=5.0)
phi = st.number_input("Capacity reduction factor φ", min_value=0.0, max_value=1.0, value=0.9, step=0.05)

# --- Section properties ---
A = b * t                     # mm²
I = b * t**3 / 12             # mm⁴ (about weak axis)
Ze = I / (t / 2)              # mm³ elastic section modulus

# Compactness check (very simple: b/t limit ~ 60ε, where ε = sqrt(250/fy))
eps = math.sqrt(250.0 / fy)
limit = 60.0 * eps
is_compact = (b / t) <= limit

# If non-compact, approximate with reduced Ze (elastic modulus used directly here)
Ze_eff = Ze if is_compact else 0.7 * Ze  # placeholder adjustment

# --- Capacities (AS 4100 simplified) ---
phiM = phi * fy * Ze_eff / 1e6          # kNm (fy in MPa = N/mm²; Ze in mm³ → N·mm)
phiV = phi * 0.6 * fy * A / 1e3         # kN (0.6fy * A, MPa×mm²= N → /1000 for kN)

# --- Actual stresses ---
M_Nmm = M_kNm * 1e6                     # kNm → N·mm
sigma_actual = M_Nmm / Ze               # MPa
tau_actual = (P_kN * 1e3) / A           # MPa (total load / area)

# --- Utilisations ---
util_M = 100.0 * M_kNm / phiM if phiM > 0 else 0.0
util_V = 100.0 * P_kN / phiV if phiV > 0 else 0.0

# --- Results ---
st.subheader("Results")

col1, col2 = st.columns(2)
with col1:
    st.metric("Design bending capacity φM", f"{phiM:,.2f} kNm")
    st.metric("Applied moment M", f"{M_kNm:,.2f} kNm")
    st.metric("Bending utilisation", f"{util_M:,.1f} %")
with col2:
    st.metric("Design shear capacity φV", f"{phiV:,.2f} kN")
    st.metric("Applied shear P", f"{P_kN:,.2f} kN")
    st.metric("Shear utilisation", f"{util_V:,.1f} %")

st.subheader("Calculated stresses")
st.write(f"- Actual bending stress σ = {sigma_actual:,.2f} MPa")
st.write(f"- Actual shear stress τ = {tau_actual:,.2f} MPa")

# --- Formulas displayed for transparency ---
st.subheader("Formulas used")
st.markdown("""
- Area: **A = b·t**
- Moment of inertia: **I = b·t³ / 12**
- Elastic section modulus: **Zₑ = I / (t/2)**
- Compactness limit: **b/t ≤ 60·ε**, with **ε = √(250/fy)**
- Design bending capacity: **φM = φ·fy·Zₑ / 10⁶**  (→ kNm)
- Design shear capacity: **φV = φ·0.6·fy·A / 1000**  (→ kN)
- Bending stress: **σ = M / Zₑ**
- Shear stress: **τ = P / A**
- Utilisation = applied / capacity × 100%
""")

st.info("Simplified implementation. For detailed checks, refer to AS 4100:2020 provisions.")
