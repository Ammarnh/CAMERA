import streamlit as st
import pyotp
import qrcode
import time
from datetime import datetime
from PIL import Image

# Pengaturan dasar halaman
st.set_page_config(
    page_title="Absensi QR Digital",
    page_icon="📲",
    layout="centered"
)

# Custom CSS untuk mempercantik tampilan (UI Ringan)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        max-width: 500px;
        margin: 0 auto;
    }
    .qr-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
    }
    .status-badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .time-text {
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 1.5rem;
        color: #1e3a8a;
    }
    </style>
    """, unsafe_allow_html=True)

# Ambil kunci dari link
user_key = st.query_params.get("key")

if user_key:
    try:
        totp = pyotp.TOTP(user_key)
        
        # Header
        st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>📲 Absensi Siswa</h2>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><span class='status-badge'>● SISTEM AKTIF</span></div>", unsafe_allow_html=True)
        st.write("")

        # Area QR dan Jam (Akan terus update)
        qr_place = st.empty()
        
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #666;'>Tunjukkan QR ini ke Guru.<br>QR dan Waktu akan berganti otomatis.</p>", unsafe_allow_html=True)

        while True:
            kode = totp.now()
            jam_skrg = datetime.now().strftime("%H:%M:%S")
            
            # Buat Gambar QR
            qr = qrcode.QRCode(box_size=10, border=1)
            qr.add_data(kode)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="#1e3a8a", back_color="white")
            
            # Tampilkan dalam satu box putih (Card)
            with qr_place.container():
                st.markdown('<div class="qr-card">', unsafe_allow_html=True)
                st.image(img_qr.get_image(), use_container_width=True)
                st.markdown(f"<div class='time-text'>{jam_skrg}</div>", unsafe_allow_html=True)
                st.markdown(f"<code style='color: #999;'>TOKEN: {kode}</code>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            time.sleep(1) # Refresh setiap detik agar jam berjalan smooth
            
    except Exception:
        st.error("Kunci tidak valid. Silakan minta link baru ke Guru.")
else:
    # Tampilan jika link salah/kosong
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.error("⚠️ Akses Ditolak")
    st.write("Silakan klik link absen yang dibagikan Guru melalui WhatsApp.")
    st.markdown("</div>", unsafe_allow_html=True)
