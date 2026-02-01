import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="FOD System", layout="wide")

st.title("🛡️ Sistem Pelaporan FOD")

# Koneksi ke Google Sheets (Dashboard Kantor)
conn = st.connection("gsheets", type=GSheetsConnection, spreadsheet="https://docs.google.com/spreadsheets/d/1Brn8tQCL6QrChfdwLxCwPCNPpAI4kE-dqTGo89rEOms/edit?gid=0#gid=0")

# Ambil Lokasi
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    
    st.success("📍 GPS Terkunci")
    
    foto = st.camera_input("Ambil Foto Bukti")
    keterangan = st.text_input("Jenis Temuan (Misal: Baut, Kawat, Plastik)")

    if st.button("KIRIM LAPORAN KE KANTOR"):
        if foto:
            waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            # Data yang akan dilihat kantor
            data_baru = pd.DataFrame([{
                "Waktu": waktu,
                "Koordinat": f"{lat}, {lon}",
                "Link_Maps": maps_link,
                "Temuan": keterangan
            }])
            
            # Simpan ke Google Sheets
            existing_data = conn.read()
            updated_df = pd.concat([existing_data, data_baru], ignore_index=True)
            conn.update(data=updated_df)
            
            st.balloons()
            st.success("✅ Terkirim! Data sudah masuk ke Dashboard Kantor.")
        else:
            st.error("Foto wajib diambil sebagai bukti.")
else:
    st.warning("🔄 Sedang mencari lokasi...")

# --- BAGIAN DASHBOARD (Yang Dilihat Kantor) ---
st.divider()
st.subheader("📊 Dashboard Pantauan Kantor (Real-Time)")
df_view = conn.read()
st.dataframe(df_view, use_container_width=True)
