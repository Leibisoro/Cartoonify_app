import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")

st.markdown("""
<style>
body {background-color:#fef7f5;}

.title {
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#ffb3d9;
    font-family:'Comic Sans MS';
}

.subtitle {
    text-align:center;
    color:#d4a5c3;
    font-size:18px;
    font-family:'Comic Sans MS';
    margin-bottom:40px;
}

.left-box {
    background-color:#fff5f8;
    border:4px solid #ffc4dd;
    padding:20px;
    border-radius:10px;
}

.right-box {
    background-color:#f5f8ff;
    border:4px solid #c4ddff;
    padding:20px;
    border-radius:10px;
}

.section-title-left {
    text-align:center;
    color:#ff99cc;
    font-weight:bold;
    font-size:20px;
    font-family:'Comic Sans MS';
    margin-bottom:15px;
}

.section-title-right {
    text-align:center;
    color:#99ccff;
    font-weight:bold;
    font-size:20px;
    font-family:'Comic Sans MS';
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">✨ Cartoonify ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform your photos into adorable cartoons</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("🖼️ UPLOAD IMAGE", type=["jpg","jpeg","png","bmp"])

def cartoonify(image):
    original = np.array(image)

    # Fix format issues (important for Streamlit Cloud)
    if original.dtype != np.uint8:
        original = original.astype(np.uint8)

    if len(original.shape) == 4:
        original = cv2.cvtColor(original, cv2.COLOR_RGBA2RGB)

    smoothed = original.copy()
    for _ in range(2):
        smoothed = cv2.bilateralFilter(smoothed, 9, 75, 75)

    hsv = cv2.cvtColor(smoothed, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
    hsv = hsv.astype(np.uint8)
    vibrant = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, 7)

    edges = cv2.adaptiveThreshold(
        gray_blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        8
    )

    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    cartoon = cv2.bitwise_and(vibrant, edges_colored)

    return cartoon

if uploaded_file:
    image = Image.open(uploaded_file)
    cartoon_img = cartoonify(image)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="left-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title-left">💫 ORIGINAL 💫</div>', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="right-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title-right">🎨 CARTOON 🎨</div>', unsafe_allow_html=True)
        st.image(cartoon_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.download_button(
        "💾 SAVE CARTOON",
        data=cv2.imencode(".png", cv2.cvtColor(cartoon_img, cv2.COLOR_RGB2BGR))[1].tobytes(),
        file_name="cartoon.png",
        mime="image/png"
    )
