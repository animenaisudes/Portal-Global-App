# 2_Balok_Kantilever.py
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("Simulasi 2: Balok Kantilever Sederhana")
st.markdown("Mencari lendutan maksimum ($\delta_{max}$) pada balok kantilever dengan beban P di ujung.")

# --- INPUT DARI PENGGUNA ---
st.header("1. Masukkan Data Balok")
L = st.slider("Panjang Balok (L) [m]", 1.0, 10.0, 5.0) 
P = st.number_input("Beban Terpusat (P) [kN]", 1.0, 100.0, 10.0)
E_gpa = st.number_input("Modulus Elastisitas (E) [GPa]", 100.0, 400.0, 200.0)
I = st.number_input("Momen Inersia (I) [m⁴]", 0.0001, 0.1, 0.001, format="%.4f")

E = E_gpa * 1e6 # Konversi GPa ke kN/m²

# --- PERHITUNGAN & VISUALISASI ---
st.header("2. Hasil Perhitungan")
try:
    delta_max = (P * (L**3)) / (3 * E * I)
    st.success(f"Lendutan Maksimum (δmax) = **{delta_max:.5f}** meter")
    
    # Visualisasi Matplotlib Sederhana
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot([0, L], [0, 0], color='blue', linewidth=5) 
    ax.plot([0, 0], [-0.5, 0.5], color='black', linewidth=10) # Jepitan
    ax.arrow(L, 0.5, 0, -1.0, head_width=0.2, head_length=0.3, fc='red', ec='red')
    ax.set_xlim(-0.5, L + 0.5)
    ax.set_ylim(-1.5, 1.0)
    ax.axis('off')
    st.pyplot(fig)
    
except ZeroDivisionError:
    st.error("Momen Inersia atau Modulus Elastisitas tidak boleh nol!")

st.subheader("3. Rumus yang Digunakan")
st.latex(r''' \delta_{max} = \frac{P L^3}{3 E I} ''')