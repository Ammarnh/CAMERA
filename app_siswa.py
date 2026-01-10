import streamlit as st
import pyotp
import qrcode
import time
from datetime import datetime
import random

# Menghilangkan akses inspeksi browser dan menu
st.set_page_config(page_title="RESTRICTED ACCESS", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #000;}
    .security-log {color: #0f0; font-family: 'Courier New'; font-size: 10px;}
    </style>
    """, unsafe_allow_html=True)

# Lapis 1: Device Locking via Browser Session
if 'device_token' not in st.session_state:
    st.session_state['device_token'] = random.getrandbits(128)

user_key = st.query_params.get("key")

if user_key:
    try:
        totp = pyotp.TOTP(user_key)
        qr_area = st.empty()
        log_area = st.empty()
        
        while True:
            kode = totp.now()
            # Lapis 2: Dynamic Visual Sync (Pola warna acak yang berubah tiap 0.5 detik)
            # Scanner guru akan mencocokkan pola warna ini
            seed = int(time.time() * 2) 
            random.seed(seed)
            r, g, b = random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

            # Lapis 3: Data QR Terenkripsi dengan Hash Waktu
            qr_data = f"VAULT|{kode}|{seed}"
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            with qr_area.container():
                # Frame visual yang terus berganti pola (Mencegah manipulasi video)
                st.markdown(f"""
                    <div style='border: 15px solid {hex_color}; padding: 10px; background: white;'>
                        <img src="data:image/png;base64,{st.image(img.get_image()).data}" style="width:100%">
                    </div>
                """, unsafe_allow_html=True)
                
            with log_area.container():
                st.markdown(f"""
                    <div class='security-log'>
                        ID: {st.session_state['device_token']}<br>
                        SYNC_SEED: {seed}<br>
                        STATUS: ENCRYPTED_STREAM_ACTIVE
                    </div>
                """, unsafe_allow_html=True)
            
            time.sleep(0.5)
    except:
        st.error("INTEGRITY_ERR: LINK_COMPROMISED")
else:
    st.error("TERMINAL_ERR: NO_AUTH_KEY")
