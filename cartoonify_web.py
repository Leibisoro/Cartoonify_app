import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Cartoonify", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Force pastel background everywhere */
    [data-testid="stAppViewContainer"] {
        background-color: #fef7f5 !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #fef7f5 !important;
        height: 0px !important;
    }
    
    .main {
        background-color: #fef7f5 !important;
        padding-top: 0rem !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }
    
    /* Hide menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title styling - exact match */
    h1 {
        color: #ffb3d9 !important;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.2rem !important;
        margin-top: 1rem !important;
        padding: 0 !important;
    }
    
    /* Subtitle styling - exact match */
    .subtitle {
        color: #d4a5c3 !important;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        font-size: 1rem !important;
        margin-top: 0px !important;
        margin-bottom: 2rem !important;
    }
    
    /* Column headers - exact match */
    .column-header-left {
        color: #ff99cc !important;
        background-color: #fff5f8 !important;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        font-size: 14px !important;
        font-weight: bold !important;
        padding: 20px 10px 10px 10px;
        border: 3px solid #ffc4dd;
        border-bottom: none;
        border-radius: 10px 10px 0 0;
    }
    
    .column-header-right {
        color: #99ccff !important;
        background-color: #f5f8ff !important;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        font-size: 14px !important;
        font-weight: bold !important;
        padding: 20px 10px 10px 10px;
        border: 3px solid #c4ddff;
        border-bottom: none;
        border-radius: 10px 10px 0 0;
    }
    
    /* Image containers - exact match */
    .image-container-left {
        background-color: #fff5f8 !important;
        border: 3px solid #ffc4dd !important;
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 20px;
        min-height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .image-container-right {
        background-color: #f5f8ff !important;
        border: 3px solid #c4ddff !important;
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 20px;
        min-height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Make images fit properly */
    .image-container-left img, .image-container-right img {
        max-height: 460px !important;
        width: auto !important;
        object-fit: contain !important;
    }
    
    /* Upload button styling - exact match */
    .stButton button {
        background-color: #ffb3d9 !important;
        color: white !important;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        font-size: 13px !important;
        font-weight: bold !important;
        padding: 15px 35px !important;
        border: none !important;
        border-radius: 5px !important;
        cursor: pointer !important;
    }
    
    .stButton button:hover {
        background-color: #ff99cc !important;
    }
    
    /* Download button styling - exact match */
    .stDownloadButton button {
        background-color: #b8d4ff !important;
        color: white !important;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        font-size: 13px !important;
        font-weight: bold !important;
        padding: 15px 35px !important;
        border: none !important;
        border-radius: 5px !important;
    }
    
    .stDownloadButton button:hover {
        background-color: #99c2ff !important;
    }
    
    /* Status messages - exact match */
    .status-message {
        color: #d4a5c3 !important;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        font-size: 11px !important;
        padding: 20px;
        background-color: #fef7f5;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: transparent !important;
    }
    
    [data-testid="stFileUploader"] section {
        background-color: #fef7f5 !important;
        border: 2px dashed #ffc4dd !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #ffb3d9 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        font-weight: bold !important;
    }
    
    /* Remove Streamlit branding colors */
    .stSpinner > div {
        border-top-color: #ffb3d9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1>✨ Cartoonify ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your photos into adorable cartoons</p>', unsafe_allow_html=True)

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

st.markdown("<br>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("🖼️ UPLOAD IMAGE", type=["jpg", "jpeg", "png", "bmp"])

st.markdown("<br>", unsafe_allow_html=True)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    
    with st.spinner("✨ Creating magic... ✨"):
        cartoon_image = cartoonify_image(original_image)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="column-header-left">💫 ORIGINAL 💫</div>', unsafe_allow_html=True)
        st.markdown('<div class="image-container-left">', unsafe_allow_html=True)
        st.image(original_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="column-header-right">🎨 CARTOON 🎨</div>', unsafe_allow_html=True)
        st.markdown('<div class="image-container-right">', unsafe_allow_html=True)
        st.image(cartoon_image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        buf = BytesIO()
        cartoon_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 SAVE CARTOON",
            data=byte_im,
            file_name="cartoon.png",
            mime="image/png"
        )
    
    st.markdown('<p class="status-message">💖 Ta-da! Your cartoon is ready! 💖</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="status-message">✨ Ready to create magic! ✨</p>', unsafe_allow_html=True)
