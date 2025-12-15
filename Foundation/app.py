import streamlit as st
import base64
import os

st.set_page_config(page_title="AFVEL", layout="wide")

# ---------- Load background ----------
def load_bg_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = load_bg_image("assets/logo.jpg")

# ---------- CSS (UNCHANGED STYLE) ----------
st.markdown(
    f"""
    <style>
    html, body {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        background: black;
    }}

    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center 25%;
        background-repeat: no-repeat;
    }}

    .block-container {{
        padding: 0;
        margin: 0;
        max-width: 100%;
    }}

    .overlay {{
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: linear-gradient(
            rgba(255, 255, 255, 0.22),
            rgba(255, 255, 255, 0.05)
        );
    }}

    .title {{
        font-size: 70px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 5px;
        text-shadow:
            0 0 6px  #FFFFFF,
            0 0 14px rgba(255,255,255,0.8),
            0 0 30px rgba(255,255,255,0.6);
    }}

    .subtitle {{
        font-size: 20px;
        color: #F0F0F0;
        margin-bottom: 20px;
    }}

    .card {{
        width: 360px;
        background: rgba(0,0,0,0.65);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.15);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- UI HEADER ----------
st.markdown(
    """
    <div class="overlay">
        <div class="title">AFVEL</div>
        <div class="subtitle">AI Face & Voice Entry Lock</div>
    """,
    unsafe_allow_html=True
)

# ---------- MODE ----------
mode = st.radio("Select Mode", ["Enroll", "Verify"], horizontal=True)
name = st.text_input("Enter your name")

os.makedirs("data/faces", exist_ok=True)
os.makedirs("data/voices", exist_ok=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)

# ---------- ENROLL ----------
if mode == "Enroll":
    st.markdown("### 🧑 Enrollment")

    face = st.camera_input("Capture Face")
    voice = st.audio_input("Record Voice")

    if st.button("Save Identity"):
        if name and face and voice:
            with open(f"data/faces/{name}.jpg", "wb") as f:
                f.write(face.getbuffer())

            with open(f"data/voices/{name}.wav", "wb") as f:
                f.write(voice.getbuffer())

            st.success("✅ Identity Enrolled Successfully")
        else:
            st.warning("Please provide name, face and voice")

# ---------- VERIFY ----------
if mode == "Verify":
    st.markdown("### 🔐 Verification")

    face = st.camera_input("Capture Face")
    voice = st.audio_input("Record Voice")

    if st.button("Verify Identity"):
        face_path = f"data/faces/{name}.jpg"
        voice_path = f"data/voices/{name}.wav"

        if name and os.path.exists(face_path) and os.path.exists(voice_path):
            st.success("🔓 ACCESS GRANTED (basic match)")
        else:
            st.error("❌ ACCESS DENIED")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
