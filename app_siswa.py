import streamlit as st
import pyotp
import qrcode
import time
from datetime import datetime
import random
import io
import base64

# Konfigurasi Halaman & Tema
st.set_page_config(page_title="VAULT AUTH", page_icon="🔐", layout="centered")

# CSS untuk UI Modern, Simpel, dan Ketat
st.markdown("""
    <style>
    /* Sembunyikan semua elemen Streamlit untuk keamanan */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0d1117;}
    
    /* Container Card Utama */
    .auth-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Tampilan Jam Digital */
    .digital-clock {
        color: #58a6ff;
        font-family: 'Courier New', monospace;
        font-size: 2.2rem;
        font-weight: bold;
        margin: 15px 0;
        text-shadow: 0 0 10px rgba(88,166,255,0.5);
    }

    /* Status Label */
    .status-active {
        color: #3fb950;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        animation: blink 1.5s infinite;
    }

    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }

    .info-text {
        color: #8b949e;
        font-size: 0.8rem;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Ambil Key dari URL
user_key = st.query_params.get("key")

if user_key:
    try:
        totp = pyotp.TOTP(user_key)
        placeholder = st.empty()

        while True:
            # Data Keamanan
            kode = totp.now()
            now = datetime.now()
            seed = int(time.time() * 2) # Detik sinkronisasi
            
            # Buat QR Code
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2)
            qr.add_data(f"VAULT|{kode}|{seed}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="#0d1117", back_color="white")
            
            # Convert image ke base64 agar ringan & tidak flicker
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode()

            # Render UI
            with placeholder.container():
                st.markdown(f"""
                    <div class="auth-card">
                        <div class="status-active">● System Secured</div>
                        <div class="digital-clock">{now.strftime('%H:%M:%S')}</div>
                        <div style="background: white; padding: 10px; border-radius: 12px; display: inline-block;">
                            <img src="data:image/png;base64,{img_b64}" width="250">
                        </div>
                        <div class="info-text">
                            DEVICE SYNC ID: {seed}<br>
                            Tunjukkan ke Guru sekarang.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            time.sleep(0.5) # Refresh sangat cepat untuk akurasi tinggi
    except:
        st.error("Kunci enkripsi rusak.")
else:
    st.markdown("""
        <div style="text-align:center; padding:50px; color:white;">
            <h3>⚠️ Akses Dibatalkan</h3>
            <p style="color:#8b949e;">Silakan gunakan link resmi yang diberikan oleh Guru.</p>
        </div>
    """, unsafe_allow_html=True)
