import streamlit as st
import pyotp
import qrcode
import time
from PIL import Image

st.set_page_config(page_title="Absen Kelas", page_icon="🔐")

st.title("🔐 QR Absen Dinamis")
st.write("Masukkan kunci rahasia dari Guru untuk memunculkan QR Code.")

# Input Secret Key
user_secret = st.text_input("Masukkan Secret Key Anda:", type="password")

if user_secret:
    try:
        totp = pyotp.TOTP(user_secret.strip())
        
        # Container untuk QR agar tidak kedap-kedip
        qr_place = st.empty()
        timer_place = st.empty()

        while True:
            kode = totp.now()
            
            # Buat Gambar QR
            qr = qrcode.QRCode(box_size=10, border=2)
            qr.add_data(kode)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            with qr_place.container():
                st.image(img.get_image(), width=300)
                st.info(f"Kode Keamanan: {kode}")
            
            st.warning("QR ini otomatis berganti setiap 30 detik. Jangan di-screenshot!")
            time.sleep(1) # Refresh tiap detik
            
    except Exception:
        st.error("Format kunci salah. Pastikan benar!")
else:
    st.info("Kunci rahasia diperlukan untuk memulai.")
