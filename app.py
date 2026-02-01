import streamlit as st
from datetime import datetime
from streamlit_js_eval import get_geolocation
import requests
import base64

st.set_page_config(page_title="FOD Pro Camera", layout="centered")

st.title("🛡️ FOD PRO: Foto + GPS + WA")

# 1. Ambil Lokasi
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    st.success(f"📍 GPS Aktif")

    # 2. Ambil Foto
    foto = st.camera_input("Ambil Foto FOD")

    if foto:
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        with st.spinner('Sedang mengupload foto...'):
            # Proses Upload ke Internet (Cloud)
            try:
                img_file = foto.getvalue()
                # Menggunakan API ImgBB (Kunci API gratis untuk tes)
                api_key = "6093d987d6050b4d455d57b447e17849" 
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": api_key,
                    "image": base64.b64encode(img_file).decode('utf-8'),
                }
                res = requests.post(url, payload)
                link_foto = res.json()['data']['url']
                
                st.image(link_foto, caption="Foto Berhasil di-Upload")

                # 3. Tombol Kirim WA
                nomor_wa = "628123456789" # <--- GANTI NOMOR ANDA
                pesan = f"--- LAPORAN FOD ---%0A🕒 Jam: {waktu}%0A📍 Lokasi: {maps_link}%0A📸 Foto: {link_foto}"
                
                wa_url = f"https://wa.me/{nomor_wa}?text={pesan}"
                
                st.write("---")
                st.link_button("📲 KIRIM KE WHATSAPP SEKARANG", wa_url)
                
            except:
                st.error("Gagal upload foto. Coba klik ambil foto lagi.")
else:
    st.warning("🔄 Mencari GPS... Pastikan izin lokasi aktif.")
