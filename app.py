import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="FOD System", layout="wide")

st.title("🛡️ Sistem Pelaporan FOD")

# Link Google Sheets Anda
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Brn8tQCL6QrChfdwLxCwPCNPpAI4kE-dqTGo89rEOms/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    st.success("📍 GPS Terkunci")
    
    foto = st.camera_input("Ambil Foto Bukti")
    keterangan = st.text_input("Jenis Temuan (Misal: Baut, Kawat, Batu)")

    if st.button("KIRIM LAPORAN KE KANTOR"):
        if foto:
            waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            data_baru = pd.DataFrame([{
                "Waktu": waktu,
                "Koordinat": f"{lat}, {lon}",
                "Link_Maps": maps_link,
                "Temuan": keterangan
            }])
            
            try:
                # Membaca data yang ada
                existing_data = conn.read(spreadsheet=SHEET_URL)
                # Menggabungkan data
                updated_df = pd.concat([existing_data, data_baru], ignore_index=True)
                # Mengirim kembali ke Google Sheets
                conn.update(spreadsheet=SHEET_URL, data=updated_df)
                
                st.balloons()
                st.success("✅ Terkirim ke Google Sheets!")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Ambil foto dulu!")
else:
    st.warning("🔄 Menunggu GPS... Klik 'Allow' jika muncul permintaan izin lokasi.")

st.divider()
st.subheader("📊 Dashboard Pantauan")
try:
    df_view = conn.read(spreadsheet=SHEET_URL)
    st.dataframe(df_view, use_container_width=True)
except:
    st.info("Menghubungkan ke data...")
