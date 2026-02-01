import streamlit as st
from datetime import datetime
from streamlit_js_eval import get_geolocation
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="FOD Pro Camera", layout="centered")

st.title("🛡️ FOD PRO: Foto + GPS")

# 1. Ambil Lokasi
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    st.success(f"📍 GPS Terkunci")

    # 2. Ambil Foto
    foto = st.camera_input("Ambil Foto FOD")

    if foto:
        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        with st.spinner('Sedang memproses & upload foto...'):
            try:
                # --- PROSES KOMPRESI FOTO (Biar Ringan) ---
                img = Image.open(foto)
                img.thumbnail((800, 800)) # Kecilkan ke ukuran standar
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=70) # Simpan sebagai JPG kualitas 70%
                img_bytes = buffer.getvalue()

                # --- UPLOAD KE IMGBB ---
                api_key = "6093d987d6050b4d455d57b447e17849" 
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": api_key,
                    "image": base64.b64encode(img_bytes).decode('utf-8'),
                }
                res = requests.post(url, payload)
                link_foto = res.json()['data']['url']
                
                st.image(link_foto, caption="Foto Siap Dikirim")

                # 3. Tombol Kirim WA (GANTI NOMOR ANDA DI SINI)
                nomor_wa = "6283833012669" 
                pesan = f"*LAPORAN INSPEKSI FOD*%0A🕒 *Waktu:* {waktu}%0A📍 *Lokasi:* {maps_link}%0A📸 *Link Foto:* {link_foto}"
                
                wa_url = f"https://wa.me/{nomor_wa}?text={pesan}"
                
                st.divider()
                st.link_button("📲 KIRIM KE WHATSAPP", wa_url, use_container_width=True)
                
            except Exception as e:
                st.error(f"Gagal upload. Coba ambil foto sekali lagi.")
                # st.write(e) # Aktifkan ini kalau mau lihat kode error aslinya
else:
    st.info("🔄 Menunggu GPS... Pastikan izin lokasi Chrome sudah 'Allow'.")
