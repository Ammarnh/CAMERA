import streamlit as st
import pyotp
import qrcode
import time
from datetime import datetime
import io
import base64

st.set_page_config(page_title="VAULT AUTH", layout="centered")

# JavaScript untuk Getar (Vibrate API)
vibrate_js = """
<script>
function triggerVibrate() {
    if ("vibrate" in navigator) {
        // Getar: 500ms getar, 200ms diam, 500ms getar
        navigator.vibrate([500, 200, 500]);
    }
}
// Pemicu jika layar kehilangan fokus (indikasi buka galeri/screenshot)
document.addEventListener("visibilitychange", function() {
    if (document.hidden) { triggerVibrate(); }
});
</script>
"""
st.components.v1.html(vibrate_js, height=0)

# CSS UI Tetap Simpel & Bagus
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0d1117;}
    .auth-card {
        background: #161b22;
        border: 2px solid #30363d;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
    }
    .status-msg { color: #3fb950; font-weight: bold; animation: pulse 2s infinite; }
    @keyframes pulse { 0% {opacity: 1;} 50% {opacity: 0.4;} 100% {opacity: 1;} }
    </style>
    """, unsafe_allow_html=True)

user_key = st.query_params.get("key")

if user_key:
    totp = pyotp.TOTP(user_key)
    placeholder = st.empty()
    
    while True:
        kode = totp.now()
        seed = int(time.time() * 2)
        
        qr = qrcode.make(f"VAULT|{kode}|{seed}")
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        img_b64 = base64.b64encode(buf.getvalue()).decode()

        with placeholder.container():
            st.markdown(f"""
                <div class="auth-card">
                    <div class="status-msg">● SECURITY ACTIVE</div>
                    <div style="color:white; font-size:2rem; margin:10px;">{datetime.now().strftime('%H:%M:%S')}</div>
                    <div style="background:white; padding:10px; border-radius:10px; display:inline-block;">
                        <img src="data:image/png;base64,{img_b64}" width="250">
                    </div>
                    <p style="color:#8b949e; font-size:0.8rem; margin-top:15px;">
                        ID SYNC: {seed}<br>Dilarang Screenshot / Replay
                    </p>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(0.5)
