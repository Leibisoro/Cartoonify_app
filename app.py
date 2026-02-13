import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Cartoonify", page_icon="✨", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.cdnfonts.com/css/comic-sans');
    
    /* Remove all default padding and margins */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, header, footer {visibility: hidden;}
    
    /* Background */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #fef7f5 !important;
    }
    
    /* Custom styles */
    .big-title {
        color: #ffb3d9;
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        margin: 20px 0 5px 0;
    }
    
    .subtitle {
        color: #d4a5c3;
        font-size: 18px;
        text-align: center;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        margin: 0 0 30px 0;
    }
    
    .frame-header-left {
        background-color: #fff5f8;
        border: 3px solid #ffc4dd;
        border-radius: 10px 10px 0 0;
        padding: 15px;
        text-align: center;
        color: #ff99cc;
        font-size: 18px;
        font-weight: bold;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        margin-bottom: 0;
    }
    
    .frame-header-right {
        background-color: #f5f8ff;
        border: 3px solid #c4ddff;
        border-radius: 10px 10px 0 0;
        padding: 15px;
        text-align: center;
        color: #99ccff;
        font-size: 18px;
        font-weight: bold;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        margin-bottom: 0;
    }
    
    .frame-body-left {
        background-color: #fffbfc;
        border: 3px solid #ffc4dd;
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 20px;
        min-height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .frame-body-right {
        background-color: #fbfcff;
        border: 3px solid #c4ddff;
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 20px;
        min-height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .status-text {
        color: #d4a5c3;
        font-size: 16px;
        text-align: center;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        margin: 20px 0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #ffb3d9 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 12px 40px !important;
        border-radius: 8px !important;
        border: none !important;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
    }
    
    .stButton > button:hover {
        background-color: #ff99cc !important;
    }
    
    .stDownloadButton > button {
        background-color: #b8d4ff !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 12px 40px !important;
        border-radius: 8px !important;
        border: none !important;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #99c2ff !important;
    }
</style>
""", unsafe_allow_html=True)

def cartoonify_image(image):
    img_array = np.array(image)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    smoothed = img_array.copy()
    for _ in range(2):
        smoothed = cv2.bilateralFilter(smoothed, 9, 75, 75)
    
    hsv = cv2.cvtColor(smoothed, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
    hsv = hsv.astype(np.uint8)
    vibrant = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 8)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(vibrant, edges_colored)
    
    cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cartoon_rgb)

st.markdown('<div class="big-title">✨ Cartoonify ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform your photos into adorable cartoons</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "bmp"], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    
    with st.spinner("✨ Creating magic... ✨"):
        cartoon_image = cartoonify_image(original_image)
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown('<div class="frame-header-left">💫 ORIGINAL 💫</div>', unsafe_allow_html=True)
        st.markdown('<div class="frame-body-left">', unsafe_allow_html=True)
        st.image(original_image, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="frame-header-right">🎨 CARTOON 🎨</div>', unsafe_allow_html=True)
        st.markdown('<div class="frame-body-right">', unsafe_allow_html=True)
        st.image(cartoon_image, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        buf = BytesIO()
        cartoon_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 SAVE CARTOON",
            data=byte_im,
            file_name="cartoon.png",
            mime="image/png",
            use_container_width=True
        )
    
    st.markdown('<div class="status-text">💖 Ta-da! Your cartoon is ready! 💖</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-text">✨ Ready to create magic! ✨</div>', unsafe_allow_html=True)
    