
# library imports untuk web app
import json
from pathlib import Path

import requests
import streamlit as st
from streamlit_option_menu import option_menu

from database import ambil_riwayat, hapus_semua_riwayat, init_database, simpan_riwayat
from scoring import buat_prompt, cek_ollama, jawab_dengan_streaming


# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="StudyMate AI",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inisialisasi database
init_database()

# Penghubung ke file assets CSS untuk styling
CSS_PATH = Path(__file__).resolve().parent / "assets" / "style.css"
if CSS_PATH.exists():
    css = CSS_PATH.read_text(encoding="utf-8")
    st.markdown("<style>\n" + css + "\n</style>", unsafe_allow_html=True)
# Sidebar dengan menu navigasi
with st.sidebar:
    st.markdown(
        """
        <h2 class="sidebar-brand">
            <i class="bi bi-robot"></i><span>StudyMate AI</span>
        </h2>
        <p class="sidebar-subtitle">Asisten Belajar Pintar Berbasis AI</p>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    halaman = option_menu(
        menu_title=None,
        options=["Jawab Soal", "Riwayat"],
        icons=["chat-left-text", "clock-history"],
        menu_icon=None,
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "5px", "background-color": "#17243D"},
            "icon": {"color": "#C7D2FE", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px", "text-align": "left", "margin": "4px",
                "color": "#F8FAFC", "--hover-color": "#354D9A",
            },
            "nav-link-selected": {
                "background-color": "#4F46E5", "color": "#FFFFFF",
                "font-weight": "600",
            },
        },
    )

    st.divider()
    st.markdown("### <i class='bi bi-cpu'></i> Model AI", unsafe_allow_html=True)
    st.caption("Mistral melalui Ollama")
    st.caption("localhost:11434")
    if cek_ollama():
        st.success("Ollama terhubung")
    else:
        st.error("Ollama tidak terhubung")

if halaman == "Jawab Soal":
    st.markdown(
        '<h1 class="main-title"><i class="bi bi-robot"></i> StudyMate AI</h1>',
        unsafe_allow_html=True,
    )
    st.write("Tempelkan soal dan dapatkan jawaban dengan bantuan AI lokal Ollama dan Mistral.")
    st.divider()

    soal = st.text_area(
        "Masukkan soal",
        placeholder="Contoh:\n1. Apa yang dimaksud dengan Komputasi Paralel?\n2. Sebutkan tiga teknik Komputasi Paralel.",
        height=120,
        max_chars=6000,
        key="input_soal",
    )

    tombol_jawab = st.button("Jawab Soal", type="primary", icon=":material/send:")
    if tombol_jawab:
        if not soal.strip():
            st.warning("Silakan masukkan soal terlebih dahulu.")
        else:
            try:
                st.subheader("Jawaban AI")
                with st.spinner("Mistral sedang menjawab..."):
                    jawaban = st.write_stream(jawab_dengan_streaming(buat_prompt(soal)))

                if isinstance(jawaban, str) and jawaban.strip():
                    simpan_riwayat(soal, jawaban)
                    st.success("Jawaban berhasil disimpan di menu Riwayat.")
                elif jawaban:
                    jawaban_teks = "".join(str(bagian) for bagian in jawaban)
                    if jawaban_teks.strip():
                        simpan_riwayat(soal, jawaban_teks)
                        st.success("Jawaban berhasil disimpan di menu Riwayat.")
            except requests.exceptions.ConnectionError:
                st.error("Ollama tidak terhubung. Pastikan aplikasi Ollama sedang berjalan.")
            except requests.exceptions.Timeout:
                st.error("Proses terlalu lama. Coba gunakan soal yang lebih pendek.")
            except requests.exceptions.HTTPError as error:
                st.error(f"Kesalahan HTTP: {error}")
            except (json.JSONDecodeError, KeyError):
                st.error("Respons dari Ollama tidak dapat dibaca.")
            except requests.exceptions.RequestException as error:
                st.error(f"Gagal menghubungi Ollama: {error}")
            except Exception as error:
                st.error(f"Terjadi kesalahan: {error}")

elif halaman == "Riwayat":
    st.markdown(
        '<h1 class="main-title"><i class="bi bi-clock-history"></i> Riwayat Jawaban</h1>',
        unsafe_allow_html=True,
    )
    st.write("Daftar pertanyaan dan jawaban yang tersimpan.")
    riwayat = ambil_riwayat()

    if not riwayat:
        st.info("Belum ada riwayat jawaban.")
    else:
        st.caption(f"Total riwayat: {len(riwayat)}")
        if st.button("Hapus Riwayat"):
            hapus_semua_riwayat()
            st.success("Semua riwayat telah dihapus.")
            st.rerun()

        for item in riwayat:
            with st.expander(f"Soal #{item['id']} — {item['waktu']}"):
                st.markdown("**Pertanyaan:**")
                st.write(item["soal"])
                st.markdown("**Jawaban StudyMate AI:**")
                st.markdown(item["jawaban"])
                st.download_button(
                    label="Download Jawaban",
                    data=item["jawaban"],
                    file_name=f"jawaban_soal_{item['id']}.txt",
                    mime="text/plain",
                    key=f"download_{item['id']}",
                )
