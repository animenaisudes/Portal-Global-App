# A_Home.py
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve # Digunakan oleh simulasi Portal Frame

st.set_page_config(layout="centered", page_title="Simulasi Struktur RWTH")

# --- DEFINISI FUNGSI SIMULASI ---

def show_home_page():
    st.title("Proyek Simulasi Struktur Teknik Sipil (RWTH)")
    st.header("Selamat Datang!")
    st.markdown("""
    Ini adalah platform yang dibuat untuk membantu mahasiswa teknik sipil memahami dasar-dasar analisis struktur.

    **Silakan pilih jenis simulasi dari menu di sidebar (kiri).**

    ---
    ### Analisis Tersedia:
    - Portal Frame 2D (Analisis FEM Dasar)
    - Balok Kantilever (Analisis Lendutan Klasik)
    """)

def show_portal_frame():
    st.title("🏗️ Simulasi 1: Portal Frame Dasar (FEM)")
    st.markdown("Menghitung perpindahan dasar portal 2D dengan beban horizontal.")
    
    # --- KODE INPUT PORTAL FRAME ---
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("Panjang Bentang (L) [m]", 1.0, 10.0, 5.0, 0.5)
        H = st.number_input("Tinggi Kolom (H) [m]", 1.0, 5.0, 3.0, 0.5)
    with col2:
        E = st.number_input("Modulus Elastisitas (E) [GPa]", 100.0, 400.0, 200.0, 10.0) * 1e6
        I = st.number_input("Momen Inersia (I) [m⁴]", 0.0001, 0.1, 0.001, format="%.4f")
        A = st.number_input("Luas Penampang (A) [m²]", 0.001, 0.5, 0.01, format="%.3f")
    P_hor = st.number_input("Gaya Horizontal (P) di Balok [kN]", 0.0, 50.0, 10.0)
    
    st.header("Hasil Analisis")

    if st.button("Hitung Perpindahan (u)"):
        # --- PERHITUNGAN MATRIKS PORTAL FRAME ---
        try:
            K = np.array([
                [ (24 * E * I) / (H**3),   0,                     0 ],
                [ 0,                      (2 * E * A) / L,       0 ],
                [ 0,                       0,                     (8 * E * I) / L ]
            ])
            F = np.array([P_hor, 0, 0]) 
            u = solve(K, F)
            
            st.success("✅ Perhitungan Selesai!")
            st.write(f"**Perpindahan Horizontal (u1):** {u[0]:.6f} m")

            # Visualisasi
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.plot([0, 0], [0, H], 'k-', linewidth=3)
            ax.plot([L, L], [0, H], 'k-', linewidth=3)
            ax.plot([0, L], [H, H], 'k-', linewidth=3)
            if P_hor > 0:
                ax.arrow(L/2, H, 0.5, 0, head_width=0.2, head_length=0.2, fc='red', ec='red')
            ax.set_aspect('equal', adjustable='box')
            ax.axis('off')
            st.pyplot(fig)
            
        except:
            st.error("Gagal melakukan perhitungan. Cek input!")

def show_kantilever():
    st.title("Simulasi 2: Balok Kantilever Sederhana")
    st.markdown("Mencari lendutan maksimum ($\delta_{max}$) pada balok kantilever dengan beban P di ujung.")

    # --- KODE INPUT KANTILEVER ---
    st.header("1. Masukkan Data Balok")
    L = st.slider("Panjang Balok (L) [m]", 1.0, 10.0, 5.0) 
    P = st.number_input("Beban Terpusat (P) [kN]", 1.0, 100.0, 10.0)
    E_gpa = st.number_input("Modulus Elastisitas (E) [GPa]", 100.0, 400.0, 200.0)
    I = st.number_input("Momen Inersia (I) [m⁴]", 0.0001, 0.1, 0.001, format="%.4f")
    
    E = E_gpa * 1e6 # Konversi GPa ke kN/m²

    st.header("2. Hasil Perhitungan")
    try:
        delta_max = (P * (L**3)) / (3 * E * I)
        st.success(f"Lendutan Maksimum (δmax) = **{delta_max:.5f}** meter")
        
        # Visualisasi
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot([0, L], [0, 0], color='blue', linewidth=5) 
        ax.plot([0, 0], [-0.5, 0.5], color='black', linewidth=10)
        ax.arrow(L, 0.5, 0, -1.0, head_width=0.2, head_length=0.3, fc='red', ec='red')
        ax.set_xlim(-0.5, L + 0.5)
        ax.set_ylim(-1.5, 1.0)
        ax.axis('off')
        st.pyplot(fig)
        
    except:
        st.error("Gagal melakukan perhitungan. Cek input!")

# --- FUNGSI NAVIGASI UTAMA ---
# Sidebar dibuat secara manual untuk navigasi yang stabil

# Tambahkan pilihan di sidebar
st.sidebar.title("Pilih Simulasi")
menu_choice = st.sidebar.radio(
    "Navigasi",
    ["Home", "1. Portal Frame 2D", "2. Balok Kantilever"]
)

# Panggil fungsi yang sesuai berdasarkan pilihan user
if menu_choice == "Home":
    show_home_page()
elif menu_choice == "1. Portal Frame 2D":
    show_portal_frame()
elif menu_choice == "2. Balok Kantilever":
    show_kantilever()