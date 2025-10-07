# 1_Portal_Frame.py

# --- 1. IMPOR LIBRARY ---
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve # Alat untuk memecahkan persamaan matriks

# --- 2. JUDUL APLIKASI ---
st.title("🏗️ Simulasi 1: Portal Frame Dasar (FEM)")
st.markdown("Aplikasi sederhana untuk menghitung perpindahan dasar portal 2D dengan beban horizontal.")

# ----------------------------------------------------------------------
# --- 3. INPUT DARI PENGGUNA ---
# ----------------------------------------------------------------------

st.header("1. Masukkan Parameter Portal")

col1, col2 = st.columns(2)

with col1:
    # Geometri
    L = st.number_input("Panjang Bentang (L) [m]", 1.0, 10.0, 5.0, 0.5)
    H = st.number_input("Tinggi Kolom (H) [m]", 1.0, 5.0, 3.0, 0.5)

with col2:
    # Properti Material & Penampang
    E = st.number_input("Modulus Elastisitas (E) [GPa]", 100.0, 400.0, 200.0, 10.0) * 1e6  # Konversi ke kN/m²
    I = st.number_input("Momen Inersia (I) [m⁴]", 0.0001, 0.1, 0.001, format="%.4f")
    A = st.number_input("Luas Penampang (A) [m²]", 0.001, 0.5, 0.01, format="%.3f")

st.header("2. Beban")
P_hor = st.number_input("Gaya Horizontal (P) di Balok [kN]", 0.0, 50.0, 10.0)

# ----------------------------------------------------------------------
# --- 4. ANALISIS MATRIKS (CONTOH SANGAT SEDERHANA UNTUK DEMO) ---
# ----------------------------------------------------------------------

st.header("3. Hasil Analisis (Matriks)")

if st.button("Hitung Perpindahan (u)"):
    
    # Matriks Kekakuan Global (K) 3x3 yang sangat disederhanakan
    
    try:
        # Matriks K yang disederhanakan 
        K = np.array([
            # u1 (Horizontal)
            [ (24 * E * I) / (H**3),   0,                     0 ],
            # u2 (Vertikal)
            [ 0,                      (2 * E * A) / L,       0 ],
            # u3 (Rotasi)
            [ 0,                       0,                     (8 * E * I) / L ]
        ])
        
        # Vektor Beban Global (F)
        F = np.array([P_hor, 0, 0]) 
        
        # Solusi: Memecahkan sistem persamaan K * u = F
        u = solve(K, F)
        
        u1 = u[0] # Perpindahan horizontal
        u2 = u[1] # Perpindahan vertikal
        u3 = u[2] # Rotasi
        
        st.success("✅ Perhitungan Selesai!")
        st.write(f"**Perpindahan Horizontal (u1):** {u1:.6f} m")
        st.write(f"**Perpindahan Vertikal (u2):** {u2:.6f} m")
        st.write(f"**Rotasi (u3):** {u3:.6f} radian")
        
        # ---------------------------------------------------------------
        # --- Visualisasi Sederhana ---
        # ---------------------------------------------------------------
        
        st.subheader("Visualisasi Portal")
        fig, ax = plt.subplots(figsize=(6, 5))
        
        # Gambar Batang Vertikal (Kolom) dan Horizontal (Balok)
        ax.plot([0, 0], [0, H], 'k-', linewidth=3)
        ax.plot([L, L], [0, H], 'k-', linewidth=3)
        ax.plot([0, L], [H, H], 'k-', linewidth=3)
        
        # Gambar Beban Horizontal
        if P_hor > 0:
            ax.arrow(L/2, H, 0.5, 0, head_width=0.2, head_length=0.2, fc='red', ec='red')
            ax.text(L/2, H + 0.3, f'P={P_hor} kN', color='red')

        # Setting Axis
        ax.set_xlim(-0.5, L + 1)
        ax.set_ylim(-0.5, H + 1)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        
        st.pyplot(fig)
        
    except np.linalg.LinAlgError:
        st.error("Matriks Kekakuan (K) adalah singular. Struktur tidak stabil dengan parameter ini.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# ----------------------------------------------------------------------
# --- 5. RUMUS YANG DIGUNAKAN ---
# ----------------------------------------------------------------------
st.subheader("4. Konsep Dasar FEM")
st.markdown(r"""
Analisis Portal Frame didasarkan pada **Metode Elemen Hingga (FEM)**: $$\mathbf{K} \cdot \mathbf{u} = \mathbf{F}$$
""")