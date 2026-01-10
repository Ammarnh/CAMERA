import streamlit as st
import pyotp
import qrcode
import time
from datetime import datetime
import random

st.set_page_config(page_title="RESTRICTED_AUTH", layout="centered")

# CSS: Hitam Total, menyembunyikan semua menu, dan border keamanan
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #000;}
    .pulse-text {color: #0f0; font-family: monospace; text-align: center; font-size: 12px;}
    </style>
    """, unsafe_allow_html=True)

user_key = st.query_params.get("key")

if user_key:
    try:
        totp = pyotp.TOTP(user_key)
        qr_area = st.empty()
        
        while True:
            kode = totp.now()
            # SEED Keamanan: Berubah tiap 0.5 detik untuk deteksi video palsu
            seed = int(time.time() * 2)
            random.seed(seed)
            # Warna berkedip acak namun terhitung secara matematis
            color = f"rgb({random.randint(100,255)}, {random.randint(100,255)}, 0)"
            
            # QR Data mengandung: PREFIX|TOKEN|TIMESTAMP_SEED
            qr_data = f"VAULT|{kode}|{seed}"
            qr = qrcode.make(qr_data)

            with qr_area.container():
                st.markdown(f"<div style='border: 15px solid {color}; padding: 10px; background: white; border-radius: 10px;'>", unsafe_allow_html=True)
                st.image(qr.get_image(), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown(f"<p class='pulse-text'>ID_SYNC: {seed}<br>SERVER_TIME: {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
            
            time.sleep(0.5)
    except:
        st.error("KEY_COMPROMISED")
else:
    st.markdown("<h1 style='color:red; text-align:center;'>ACCESS DENIED</h1>", unsafe_allow_html=True)
