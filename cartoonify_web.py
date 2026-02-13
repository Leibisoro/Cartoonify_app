import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Cartoonify", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');
    
    .main {
        background-color: #fef7f5;
    }
    
    .stApp {
        background-color: #fef7f5;
    }
    
    .stButton>button {
        background-color: #ffb3d9;
        color: white;
        font-weight: bold;
        border-radius: 15px;
        padding: 15px 40px;
        border: none;
        font-size: 18px;
        font-family: 'Comic Neue', 'Comic Sans MS', cursive;
        box-shadow: 0 4px 6px rgba(255, 179, 217, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #ff99cc;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(255, 153, 204, 0.4);
    }
    
    .stDownloadButton>button {
        background-color: #b8d4ff;
        color: white;
        font-weight: bold;
        border-radius: 15px;
        padding: 15px 40px;
        border: none;
        font-size: 18px;
        font-family: 'Comic Neue', 'Comic Sans MS', cursive;
        box-shadow: 0 4px 6px rgba(184, 212, 255, 0.3);
    }
    
    .stDownloadButton>button:hover {
        background-color: #99c2ff;
    }
    
    h1 {
        color: #ffb3d9;
        text-align: center;
        font-family: 'Comic Neue', 'Comic Sans MS', cursive;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(255, 179, 217, 0.2);
    }
    
    h3 {
        color: #d4a5c3;
        text-align: center;
        font-family: 'Comic Neue', 'Comic Sans MS', cursive;
        font-weight: 400;
        margin-top: 0;
    }
    
    .uploadedFile {
        background-color: #fff5f8;
        border: 2px solid #ffc4dd;
        border-radius: 10px;
    }
    
    .stMarkdown {
        font-family: 'Comic Neue', 'Comic Sans MS', cursive;
    }
    
    div[data-testid="stImage"] {
        border: 3px solid #ffc4dd;
        border-radius: 15px;
        padding: 10px;
        background-color: #fff5f8;
        box-shadow: 0 4px 6px rgba(255, 196, 221, 0.2);
    }
    
    .stAlert {
        background-color: #fff5f8;
        border: 2px solid #ffb3d9;
        border-radius: 10px;
        font-family: 'Comic Neue', 'Comic Sans MS', cursive;
    }
    
    .stSpinner > div {
        border-top-color: #ffb3d9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Cartoonify ✨")
st.markdown("### Transform your photos into adorable cartoons")

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

st.markdown("---")

uploaded_file = st.file_uploader("🖼️ Upload an image", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    
    with st.spinner("✨ Creating magic..."):
        cartoon_image = cartoonify_image(original_image)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💫 ORIGINAL")
        st.image(original_image, use_container_width=True)
    
    with col2:
        st.markdown("### 🎨 CARTOON")
        st.image(cartoon_image, use_container_width=True)
    
    st.markdown("---")
    
    st.download_button(
        label="💾 Download Cartoon Image",
        data=cartoon_image.tobytes(),
        file_name="cartoon.png",
        mime="image/png"
    )
    
    st.success("💖 Ta-da! Your cartoon is ready!")
else:
    st.info("👆 Upload an image to get started!")
