import streamlit as st
import requests
import base64
from datetime import datetime
from streamlit_js_eval import get_geolocation

# --- KONFIGURASI ---
# Masukkan API Key ImgBB Anda di sini
IMGBB_API_KEY = "d15d1dd744019c92a391bd2154d015b9"
# Masukkan nomor WA tujuan (contoh: 62812345678)
NOMOR_WA_TUJUAN = "6283833012669"

st.set_page_config(page_title="FOD Reporting System", layout="centered")
st.title("📸 Pelaporan FOD Lapangan")

# Ambil Lokasi GPS
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    st.success("📍 GPS Terkunci")
    
    foto = st.camera_input("Ambil Foto Temuan")
    keterangan = st.text_input("Jenis Temuan (Contoh: Baut, Serpihan Ban)")

    if st.button("BUAT LAPORAN WHATSAPP"):
        if foto and keterangan:
            with st.spinner('Mengunggah foto...'):
                try:
                    # 1. Upload ke ImgBB
                    img_bytes = foto.getvalue()
                    encoded_string = base64.b64encode(img_bytes).decode()
                    res = requests.post(
                        "https://api.imgbb.com/1/upload",
                        data={"key": IMGBB_API_KEY, "image": encoded_string}
                    )
                    url_foto = res.json()["data"]["url"]

                    # 2. Susun Pesan WA
                    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    pesan = (
                        f"*LAPORAN TEMUAN FOD*%0A"
                        f"--------------------------%0A"
                        f"🕒 *Waktu:* {waktu}%0A"
                        f"🔎 *Temuan:* {keterangan}%0A"
                        f"📍 *Lokasi:* {maps_link}%0A"
                        f"🖼️ *Link Foto:* {url_foto}%0A"
                        f"--------------------------"
                    )
                    
                    wa_url = f"https://wa.me/{NOMOR_WA_TUJUAN}?text={pesan}"
                    
                    st.success("Foto berhasil diunggah!")
                    st.link_button("📲 KIRIM KE WHATSAPP KANTOR", wa_url, use_container_width=True)
                    
                except Exception as e:
                    st.error("Gagal mengunggah foto. Cek API Key ImgBB Anda.")
        else:
            st.warning("Lengkapi Foto dan Keterangan!")
else:
    st.info("🔄 Mencari sinyal GPS... Pastikan izin lokasi aktif.")
