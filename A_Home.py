# Home.py
import streamlit as st

st.set_page_config(layout="centered")
st.title("Proyek Simulasi Struktur Teknik Sipil")
st.header("Selamat Datang!")
st.markdown("""
Ini adalah platform yang dibuat untuk membantu mahasiswa teknik sipil RWTH Aachen memahami dasar-dasar analisis struktur melalui simulasi interaktif.

**Silakan pilih jenis simulasi dari menu di sidebar (kiri) di bawah 'Pages'.**

---

### Jenis-jenis Simulasi:
1.  **1 Portal Frame:** Analisis Kekakuan Global (FEM Dasar).
2.  **2 Balok Kantilever:** Analisis Lendutan Klasik.

""")