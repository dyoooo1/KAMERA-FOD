import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURASI ---
# 1. Masukkan API Key ImgBB Anda di sini
IMGBB_API_KEY = "d15d1dd744019c92a391bd2154d015b9"

# 2. Link Google Sheets Anda
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Brn8tQCL6QrChfdwLxCwPCNPpAI4kE-dqTGo89rEOms/edit?usp=sharing"

st.set_page_config(page_title="FOD System + Photo", layout="wide")
st.title("🛡️ Sistem Pelaporan FOD (Auto Photo)")

conn = st.connection("gsheets", type=GSheetsConnection)
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    st.success("📍 GPS Terkunci")
    
    foto = st.camera_input("Ambil Foto Temuan")
    keterangan = st.text_input("Jenis Temuan (Misal: Baut, Batu, Plastik)")

    if st.button("KIRIM LAPORAN LENGKAP"):
        if foto and keterangan:
            with st.spinner('Sedang mengunggah foto dan menyimpan data...'):
                try:
                    # PROSES UPLOAD FOTO KE IMGBB
                    img_bytes = foto.getvalue()
                    encoded_string = base64.b64encode(img_bytes).decode()
                    
                    res = requests.post(
                        "https://api.imgbb.com/1/upload",
                        data={"key": IMGBB_API_KEY, "image": encoded_string}
                    )
                    json_data = res.json()
                    url_foto = json_data["data"]["url"] # Ini link foto aslinya

                    # PROSES SIMPAN KE GOOGLE SHEETS
                    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    data_baru = pd.DataFrame([{
                        "Waktu": waktu,
                        "Temuan": keterangan,
                        "Link_Maps": maps_link,
                        "Link_Foto": url_foto  # Link foto masuk ke kolom ini
                    }])
                    
                    existing_data = conn.read(spreadsheet=SHEET_URL)
                    updated_df = pd.concat([existing_data, data_baru], ignore_index=True)
                    conn.update(spreadsheet=SHEET_URL, data=updated_df)
                    
                    st.balloons()
                    st.success(f"✅ Berhasil! Foto tersimpan di: {url_foto}")
                except Exception as e:
                    st.error(f"Gagal: {e}")
        else:
            st.warning("Foto dan Keterangan wajib diisi!")
else:
    st.info("🔄 Menunggu GPS...")

st.divider()
st.subheader("📊 Data Laporan Kantor")
try:
    df_view = conn.read(spreadsheet=SHEET_URL)
    st.dataframe(df_view, use_container_width=True)
except:
    st.write("Menghubungkan ke database...")
