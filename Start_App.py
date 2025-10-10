# A_Home.py - Anwendung zur Baustatik-Simulation (Deutsche Version)
import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve 

# Konfiguration Halaman
st.set_page_config(layout="centered", page_title="Baustatik-Simulation RWTH")

# --- DEFINITION DER SEITEN UND FUNKTIONEN ---

def show_home_page():
    st.title("🏗️ Projekt Bauingenieurwesen Simulation (RWTH)")
    st.header("Willkommen!")
    st.markdown("""
    Dies ist eine Plattform, die entwickelt wurde, um Studierenden des Bauingenieurwesens das Verständnis der Grundlagen der Tragwerksanalyse zu erleichtern.

    **Bitte wählen Sie den gewünschten Simulationstyp über das Menü in der Seitenleiste (links) aus.**
    """)
    st.subheader("Verfügbare Analysen:")
    st.markdown("- **1. 2D Rahmen (Portalrahmen):** Globale Steifigkeitsanalyse (FEM-Grundlagen)")
    st.markdown("- **2. Kragträger (Ausleger):** Klassische Durchbiegungsanalyse")

def show_portal_frame():
    st.title("🏗️ Simulation 1: Grundlegender Portalrahmen (FEM)")
    st.markdown("Analyse der Schnittgrößen und Verschiebungen im 2D-Portalrahmen. Ergebnisse und Visualisierung werden live aktualisiert.")
    
    # --- EINGABE-CODE PORTALRAHMEN ---
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("Spannweite (L) [m]", 1.0, 10.0, 5.0, 0.5, key="pL") 
        H = st.number_input("Stützenhöhe (H) [m]", 1.0, 5.0, 3.0, 0.5, key="pH")    
    with col2:
        E_gpa = st.number_input("Elastizitätsmodul (E) [GPa]", 100.0, 400.0, 200.0, 10.0, key="pE")
        I = st.number_input("Flächenträgheitsmoment (I) [m⁴]", 0.0001, 0.1, 0.001, format="%.4f", key="pI")
        A = st.number_input("Querschnittsfläche (A) [m²]", 0.001, 0.5, 0.01, format="%.3f", key="pA")
    
    P_hor = st.number_input("Horizontallast (P) [kN] (Am Knoten 2)", 0.0, 50.0, 10.0, key="pP")
    
    E = E_gpa * 1e6
    st.header("Analyseergebnisse")

    try:
        # BERECHNUNG DER GLOBALEN MATRIX
        K = np.array([
            [ (24 * E * I) / (H**3),   0,                     0 ],
            [ 0,                      (2 * E * A) / L,       0 ],
            [ 0,                       0,                     (8 * E * I) / L ]
        ])
        F = np.array([P_hor, 0, 0]) 
        u = solve(K, F)
        
        st.success("✅ Verschiebung berechnet!")
        
        # Globale Verschiebung
        st.subheader("Globale Verschiebungen")
        col_u1, col_u2, col_u3 = st.columns(3)
        col_u1.metric("Horizontal (u₁)", f"{u[0]:.6f} m")
        col_u2.metric("Vertikal (u₂)", f"{u[1]:.6f} m")
        col_u3.metric("Rotation (u₃)", f"{u[2]:.6f} rad")


        # --- SCHNITTRÖSEN-ANALYSE ---
        st.subheader("Schnittgrößen: Elementauswahl")
        pilihan_batang = st.radio(
            "Wählen Sie das Element, um innere Kräfte (N, V, M) anzuzeigen:",
            ("1. Linke Stütze", "2. Oberer Balken", "3. Rechte Stütze"),
            horizontal=True, 
            key="batang_select_radio"
        )
        
        # --- LOGIK DER INNEREN KRÄFTE ---
        
        if pilihan_batang == "1. Linke Stütze":
            V = P_hor / 2.0 
            M_dasar = V * H
            N = 0 
            st.markdown(f"#### Innere Kräfte für **{pilihan_batang}**")
            st.code(f"""
            Normalkraft (N): {N:.2f} kN
            Querkraft (V): {V:.2f} kN
            Biegemoment (M): {M_dasar:.2f} kNm
            """)
        elif pilihan_batang == "2. Oberer Balken":
            N_balok = P_hor 
            st.markdown("#### Innere Kräfte für **Oberer Balken**")
            st.code(f"""
            Normalkraft (N): {N_balok:.2f} kN (Axiallast durch u₂)
            Querkraft (V): 0.00 kN
            Biegemoment (M): 0.00 kNm 
            """)
        elif pilihan_batang == "3. Rechte Stütze":
            V = P_hor / 2.0
            M_dasar = V * H
            N = 0
            st.markdown(f"#### Innere Kräfte für **{pilihan_batang}**")
            st.code(f"""
            Normalkraft (N): {N:.2f} kN
            Querkraft (V): {V:.2f} kN
            Biegemoment (M): {M_dasar:.2f} kNm
            """)
        
        # --- VISUALISIERUNG ---
        st.subheader("Strukturdiagramm")
        # (Matplotlib Code bleibt gleich, da die Achsenbeschriftungen etc. ausgeblendet sind)
        fig, ax = plt.subplots(figsize=(8, 6)) 
        nodes = {1: (0, 0), 2: (0, H), 3: (L, H), 4: (L, 0)}
        line_style = dict(color='k', linewidth=3.5, zorder=1)
        ax.plot([0, 0], [0, H], **line_style)
        ax.plot([L, L], [0, H], **line_style) 
        ax.plot([0, L], [H, H], **line_style) 
        
        highlight_style = dict(color='y', linewidth=6, alpha=0.5, zorder=2)
        if pilihan_batang == "1. Linke Stütze":
            ax.plot([0, 0], [0, H], **highlight_style)
        elif pilihan_batang == "2. Oberer Balken":
            ax.plot([0, L], [H, H], 'y-', linewidth=6, alpha=0.5, zorder=2)
        elif pilihan_batang == "3. Rechte Stütze":
            ax.plot([L, L], [0, H], **highlight_style)

        for node, (x, y) in nodes.items():
            ax.plot(x, y, 'o', color='blue', markersize=8, zorder=3)
            ax.text(x + 0.1, y + 0.1, str(node), color='blue', fontsize=14, fontweight='bold', zorder=4) 

        support_y = -0.1 * H
        ax.fill([-0.3, 0.3, 0.3, -0.3], [support_y-0.2, support_y-0.2, support_y, support_y], 'gray', edgecolor='black', zorder=2)
        ax.fill([L-0.3, L+0.3, L+0.3, L-0.3], [support_y-0.2, support_y-0.2, support_y, support_y], 'gray', edgecolor='black', zorder=2)

        if P_hor > 0:
            ax.arrow(nodes[2][0], nodes[2][1], 0.5, 0, head_width=0.2, head_length=0.2, fc='red', ec='red', linewidth=2, zorder=3)
            ax.text(nodes[2][0] + 0.8, nodes[2][1], f'P={P_hor} kN', color='red', ha='left', va='center', fontsize=12, zorder=3)

        ax.text(L/2, -0.2, f'L={L}m', ha='center', va='top')
        ax.text(-0.5, H/2, f'H={H}m', ha='right', va='center')
        ax.text(-0.2, H/2, 'Element 1', color='red', fontsize=10, ha='right')
        ax.text(L/2, H + 0.15, 'Element 2', color='red', fontsize=10, ha='center')

        ax.set_xlim(-1, L + 1)
        ax.set_ylim(support_y-0.5, H + 1)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        st.pyplot(fig)
        
    except np.linalg.LinAlgError:
        st.error("Die Steifigkeitsmatrix (K) ist singulär. Die Struktur ist mit diesen Parametern instabil.")
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")

    st.subheader("FEM-Grundlagen")
    st.markdown(r"""
    Die Portalrahmenanalyse basiert auf der **Finite-Elemente-Methode (FEM)**: $$\mathbf{K} \cdot \mathbf{u} = \mathbf{F}$$
    """)

def show_kantilever():
    st.title("Simulation 2: Grundlegender Kragträger")
    st.markdown("Berechnet die maximale Durchbiegung ($\delta_{max}$) des Kragträgers. Ergebnisse werden live aktualisiert.")

    # --- EINGABE KRAGTRÄGER ---
    st.header("1. Trägerdaten eingeben")
    L = st.slider("Trägerlänge (L) [m]", 1.0, 10.0, 5.0, key="kL") 
    P = st.number_input("Einzellast (P) [kN]", 1.0, 100.0, 10.0, key="kP")
    E_gpa = st.number_input("Elastizitätsmodul (E) [GPa]", 100.0, 400.0, 200.0, key="kE")
    I = st.number_input("Flächenträgheitsmoment (I) [m⁴]", 0.0001, 0.1, 0.001, format="%.4f", key="kI")
    
    E = E_gpa * 1e6 

    st.header("2. Berechnung und Visualisierung")

    try:
        delta_max = (P * (L**3)) / (3 * E * I)
        st.success(f"Maximale Durchbiegung (δmax) = **{delta_max:.5f}** Meter")
        
        # VISUALISIERUNG KRAGTRÄGER
        st.subheader("Kragträger-Diagramm")
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Träger
        ax.plot([0, L], [0, 0], color='blue', linewidth=5) 
        
        # Einspannung (Fix Support)
        ax.plot([0, 0], [-0.5, 0.5], color='black', linewidth=10)
        ax.fill([0, -0.2, -0.2, 0], [-0.5, -0.3, 0.3, 0.5], color='gray', edgecolor='black')

        # Last (P)
        ax.arrow(L, 0.5, 0, -1.0, head_width=0.2, head_length=0.3, fc='red', ec='red', linewidth=2)
        ax.text(L + 0.3, 0.5, f'P={P} kN', color='red', ha='left', va='center') 

        # Länge (L)
        ax.plot([0, L], [-0.5, -0.5], 'k--')
        ax.text(L/2, -0.7, f'L={L} m', ha='center', va='top') 

        # Durchbiegung (Skizze)
        x_def = np.linspace(0, L, 100)
        y_def_raw = (P * (x_def**2)) / (6 * E * I) * (3 * L - x_def)
        max_scaling = delta_max / y_def_raw[-1]
        y_def_scaled = -y_def_raw * max_scaling

        ax.plot(x_def, y_def_scaled, 'g--', linewidth=1)
        ax.text(L, -delta_max-0.2, f'δ={delta_max:.3f}m', color='green', ha='right', va='top')


        # Achseneinstellungen
        ax.set_xlim(-0.5, L + 1)
        ax.set_ylim(-1.5, 1.0)
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        st.pyplot(fig)
        
    except ZeroDivisionError:
        st.error("Das Flächenträgheitsmoment (I) oder der E-Modul darf nicht Null sein!")
    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {e}")

    st.subheader("Verwendete Formel")
    st.latex(r''' \delta_{max} = \frac{P L^3}{3 E I} ''')

# --- HAUPTNAVIGATION ---
st.sidebar.title("Simulation auswählen")
menu_choice = st.sidebar.radio(
    "Navigation",
    ["Home", "1. Portalrahmen 2D", "2. Kragträger"]
)

if menu_choice == "Home":
    show_home_page()
elif menu_choice == "1. Portalrahmen 2D":
    show_portal_frame()
elif menu_choice == "2. Kragträger":
    show_kantilever()