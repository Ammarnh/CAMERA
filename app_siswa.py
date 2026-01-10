import streamlit as st
import pyotp
import qrcode
import time
from datetime import datetime

st.set_page_config(page_title="SECURE-AUTH", layout="centered")

# CSS Minimalis: Menghilangkan semua menu Streamlit agar tidak bisa diakali
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    .stApp {background-color: #000000;} /* Background Hitam untuk kontras tinggi */
    .sec-text {color: #00ff00; font-family: 'Courier New'; text-align: center; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

user_key = st.query_params.get("key")

if user_key:
    try:
        totp = pyotp.TOTP(user_key)
        qr_area = st.empty()
        
        while True:
            kode = totp.now()
            now = datetime.now()
            ts = now.strftime("%S") # Detik saat ini sebagai verifikator visual
            
            # Buat QR dengan High Error Correction (H) agar tetap terbaca meski layar HP kotor
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.add_data(f"SEC|{kode}|{now.strftime('%H%M%S')}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            with qr_area.container():
                # Visual Security: Tampilan berkedip antara Hijau dan Putih tiap detik
                blink_color = "#00ff00" if int(ts) % 2 == 0 else "#ffffff"
                st.markdown(f"<div style='border: 10px solid {blink_color}; padding: 10px; background: white;'>", unsafe_allow_html=True)
                st.image(img.get_image(), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Tampilan Waktu Server (Harus sama dengan laptop Guru)
                st.markdown(f"<p class='sec-text'>SERVER TIME: {now.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:red; text-align:center; font-size:10px;'>VOID IF STATIC / FOTO DILARANG</p>", unsafe_allow_html=True)
            
            time.sleep(0.5) # Update lebih cepat (0.5 detik) untuk akurasi tinggi
    except:
        st.error("ENCRYPTION ERROR")
else:
    st.error("ACCESS DENIED: NO KEY")
