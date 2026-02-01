import streamlit as st
from datetime import datetime
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="FOD Camera GPS", layout="centered")

st.title("📸 Kamera Inspeksi FOD")

# 1. Ambil Lokasi
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    st.success(f"📍 GPS Terkunci!")

    # 2. Kamera
    foto = st.camera_input("Ambil Foto Temuan")

    if foto:
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        st.image(foto, caption="Foto Berhasil")

        # Masukkan nomor WA kantor/tujuan (awali dengan 62)
        nomor_wa = "628123456789" 
        
        # Susun pesan
        pesan = f"*LAPORAN INSPEKSI FOD*%0A🕒 *Waktu:* {waktu}%0A📍 *Lokasi:* {maps_link}%0A📸 *Catatan:* Foto sudah diambil di lokasi."
        
        wa_url = f"https://wa.me/{nomor_wa}?text={pesan}"
        
        st.divider()
        st.subheader("Kirim ke Kantor:")
        st.link_button("📲 KIRIM VIA WHATSAPP", wa_url, use_container_width=True)
else:
    st.warning("🔄 Sedang mengunci GPS... Pastikan izin lokasi aktif.")
