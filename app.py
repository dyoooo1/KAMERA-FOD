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
    # Link Google Maps yang langsung menunjukkan titik merah
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    st.success(f"📍 GPS Terkunci!")
    st.info(f"Koordinat: {lat}, {lon}")

    # 2. Kamera
    foto = st.camera_input("Ambil Foto Temuan")

    if foto:
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        st.image(foto, caption="Foto berhasil diambil")

        # 3. Tombol WhatsApp (Ganti nomor Anda)
        nomor_wa = "6283833012669" 
        pesan = f"*LAPORAN FOD*%0A🕒 *Waktu:* {waktu}%0A📍 *Lokasi:* {maps_link}%0A📸 *Catatan:* Foto sudah diambil di lokasi."
        
        wa_url = f"https://wa.me/{nomor_wa}?text={pesan}"
        
        st.divider()
        st.link_button("📲 KIRIM KOORDINAT KE WA", wa_url, use_container_width=True)
else:
    st.warning("🔄 Sedang mengunci GPS... Mohon tunggu atau cek izin lokasi di browser.")
