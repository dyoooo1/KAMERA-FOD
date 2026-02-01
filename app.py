import streamlit as st
from datetime import datetime
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="Kamera GPS FOD", layout="centered")

st.title("📸 Kamera GPS Lapangan")

# 1. Ambil Lokasi
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    st.success(f"📍 Lokasi Terdeteksi")
    st.markdown(f"[Lihat di Google Maps]({maps_link})")

    # 2. Ambil Foto
    foto = st.camera_input("Ambil Foto FOD")

    if foto:
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        st.image(foto, caption="Foto Siap Dikirim")

        # 3. Tombol Kirim WA (Ganti nomor di bawah dengan nomor Anda)
        nomor_wa = "6283833012669" # <--- GANTI DENGAN NOMOR WA ANDA (Awali 62)
        pesan = f"LAPORAN FOD%0AJam: {waktu}%0ALokasi: {maps_link}"
        
        wa_url = f"https://wa.me/{nomor_wa}?text={pesan}"
        
        st.write("---")
        st.link_button("📲 KIRIM DATA KE WHATSAPP", wa_url)
        st.info("Klik tombol di atas untuk mengirim detail lokasi ke WA.")
else:
    st.warning("Menunggu GPS... Pastikan Izin Lokasi di Chrome HP sudah di-ALLOW.")
