# A_Home.py
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

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
    st.markdown("Analisis gaya internal dan perpindahan portal 2D. Hasil dan visualisasi diperbarui secara langsung.")
    
    # --- KODE INPUT PORTAL FRAME ---
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("Panjang Bentang (L) [m]", 1.0, 10.0, 5.0, 0.5, key="pL") 
        H = st.number_input("Tinggi Kolom (H) [m]", 1.0, 5.0, 3.0, 0.5, key="pH")    
    with col2:
        E_gpa = st.number_input("Modulus Elastisitas (E) [GPa]", 100.0, 400.0, 200.0, 10.0, key="pE")
        I = st.number_input("Momen Inersia (I) [m⁴]", 0.0001, 0.1, 0.001, format="%.4f", key="pI")
        A = st.number_input("Luas Penampang (A) [m²]", 0.001, 0.5, 0.01, format="%.3f", key="pA")
    P_hor = st.number_input("Gaya Horizontal (P) di Balok [kN]", 0.0, 50.0, 10.0, key="pP")
    
    E = E_gpa * 1e6
    st.header("Hasil Analisis")

    try:
        # PERHITUNGAN MATRIKS GLOBAL
        K = np.array([
            [ (24 * E * I) / (H**3),   0,                     0 ],
            [ 0,                      (2 * E * A) / L,       0 ],
            [ 0,                       0,                     (8 * E * I) / L ]
        ])
        F = np.array([P_hor, 0, 0]) 
        u = solve(K, F)
        
        st.success("✅ Perhitungan Perpindahan Selesai!")
        st.write(f"**Perpindahan Horizontal (u1):** {u[0]:.6f} m")
        st.write(f"**Perpindahan Vertikal (u2):** {u[1]:.6f} m")
        st.write(f"**Rotasi (u3):** {u[2]:.6f} radian")

        # --- SELEKSI BATANG BARU ---
        st.subheader("Pilih Batang untuk Analisis Internal")
        pilihan_batang = st.selectbox(
            "Pilih Elemen",
            ("1. Kolom Kiri", "2. Balok Atas", "3. Kolom Kanan"),
            key="batang_select"
        )
        
        # --- LOGIKA GAYA INTERNAL ---
        
        if pilihan_batang == "1. Kolom Kiri":
            V = P_hor / 2.0 
            M_dasar = V * H
            N = 0 

            st.markdown(f"#### Hasil Gaya Internal untuk {pilihan_batang}")
            st.code(f"""
            Gaya Normal (N): {N:.2f} kN
            Gaya Geser (V): {V:.2f} kN
            Momen Dasar (M): {M_dasar:.2f} kNm
            """)
        elif pilihan_batang == "2. Balok Atas":
            st.markdown("#### Hasil Gaya Internal untuk Balok Atas")
            V_balok = 0 
            M_balok = 0
            N_balok = P_hor
            st.code(f"""
            Gaya Normal (N): {N_balok:.2f} kN (Gaya aksial akibat P_hor)
            Gaya Geser (V): {V_balok:.2f} kN
            Momen Maksimum (M): {M_balok:.2f} kNm 
            """)
        elif pilihan_batang == "3. Kolom Kanan":
            V = P_hor / 2.0
            M_dasar = V * H
            N = 0
            st.markdown(f"#### Hasil Gaya Internal untuk {pilihan_batang}")
            st.code(f"""
            Gaya Normal (N): {N:.2f} kN
            Gaya Geser (V): {V:.2f} kN
            Momen Dasar (M): {M_dasar:.2f} kNm
            """)
        
        # --- VISUALISASI PORTAL FRAME ---
        st.subheader("Visualisasi Portal")
        fig, ax = plt.subplots(figsize=(6, 5))
        
        # Gambar Batang Vertikal (Kolom) dan Horizontal (Balok)
        ax.plot([0, 0], [0, H], 'k-', linewidth=3, label='Batang 1')
        ax.plot([L, L], [0, H], 'k-', linewidth=3, label='Batang 3')
        ax.plot([0, L], [H, H], 'k-', linewidth=3, label='Batang 2')
        
        # Menandai Batang yang Dipilih (Opsional: ubah warna)
        if pilihan_batang == "1. Kolom Kiri":
            ax.plot([0, 0], [0, H], 'r-', linewidth=5) 
        elif pilihan_batang == "2. Balok Atas":
            ax.plot([0, L], [H, H], 'r-', linewidth=5)
        elif pilihan_batang == "3. Kolom Kanan":
            ax.plot([L, L], [0, H], 'r-', linewidth=5) 


        # Gambar Beban Horizontal
        if P_hor > 0:
            ax.arrow(L/2, H, 0.5, 0, head_width=0.2, head_length=0.2, fc='red', ec='red')
            ax.text(L/2, H + 0.3, f'P={P_hor} kN', color='red', ha='center')

        # Gambar Label Geometri
        ax.text(L/2, H + 0.1, f'L={L}m', ha='center', va='bottom')
        ax.text(-0.2, H/2, f'H={H}m', ha='right', va='center')


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

    st.subheader("Konsep Dasar FEM")
    st.markdown(r"""
    Analisis Portal Frame didasarkan pada **Metode Elemen Hingga (FEM)**: $$\mathbf{K} \cdot \mathbf{u} = \mathbf{F}$$
    """)

def show_kantilever():
    st.title("Simulasi 2: Balok Kantilever Sederhana")
    st.markdown("Mencari lendutan maksimum ($\delta_{max}$) pada balok kantilever dengan beban P di ujung. Hasil dan visualisasi diperbarui secara langsung.")

    # --- KODE INPUT KANTILEVER ---
    st.header("1. Masukkan Data Balok")
    L = st.slider("Panjang Balok (L) [m]", 1.0, 10.0, 5.0, key="kL") 
    P = st.number_input("Beban Terpusat (P) [kN]", 1.0, 100.0, 10.0, key="kP")
    E_gpa = st.number_input("Modulus Elastisitas (E) [GPa]", 100.0, 400.0, 200.0, key="kE")
    I = st.number_input("Momen Inersia (I) [m⁴]", 0.0001, 0.1, 0.001, format="%.4f", key="kI")
    
    E = E_gpa * 1e6 # Konversi GPa ke kN/m²

    st.header("2. Hasil Perhitungan dan Visualisasi")

    try:
        delta_max = (P * (L**3)) / (3 * E * I)
        st.success(f"Lendutan Maksimum (δmax) = **{delta_max:.5f}** meter")
        
        # VISUALISASI KANTILEVER
        st.subheader("Visualisasi Balok Kantilever")
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Balok
        ax.plot([0, L], [0, 0], color='blue', linewidth=5) 
        
        # Jepitan (Fix Support)
        ax.plot([0, 0], [-0.5, 0.5], color='black', linewidth=10)
        ax.fill([0, -0.2, -0.2, 0], [-0.5, -0.3, 0.3, 0.5], color='gray', edgecolor='black')

        # Beban Terpusat
        ax.arrow(L, 0.5, 0, -1.0, head_width=0.2, head_length=0.3, fc='red', ec='red', linewidth=2)
        ax.text(L + 0.3, 0.5, f'P={P} kN', color='red', ha='left', va='center') 

        # Panjang Balok
        ax.plot([0, L], [-0.5, -0.5], 'k--')
        ax.text(L/2, -0.7, f'L={L} m', ha='center', va='top') 

        # Lendutan (Garis putus-putus)
        x_def = np.linspace(0, L, 100)
        y_def = -delta_max * (x_def/L)**2 
        ax.plot(x_def, y_def, 'g--', linewidth=1)
        ax.text(L, -delta_max-0.2, f'δ={delta_max:.3f}m', color='green', ha='right', va='top')


        # Setting Axis
        ax.set_xlim(-0.5, L + 1)
        ax.set_ylim(-1.5, 1.0)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        st.pyplot(fig)
        
    except ZeroDivisionError:
        st.error("Momen Inersia atau Modulus Elastisitas tidak boleh nol!")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

    st.subheader("Rumus yang Digunakan")
    st.latex(r''' \delta_{max} = \frac{P L^3}{3 E I} ''')

# --- FUNGSI NAVIGASI UTAMA ---
st.sidebar.title("Pilih Simulasi")
menu_choice = st.sidebar.radio(
    "Navigasi",
    ["Home", "1. Portal Frame 2D", "2. Balok Kantilever"]
)

if menu_choice == "Home":
    show_home_page()
elif menu_choice == "1. Portal Frame 2D":
    show_portal_frame()
elif menu_choice == "2. Balok Kantilever":
    show_kantilever()