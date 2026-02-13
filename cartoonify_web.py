import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Cartoonify", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #fef7f5;
    }
    .stButton>button {
        background-color: #ffb3d9;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 30px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #ff99cc;
    }
    h1 {
        color: #ffb3d9;
        text-align: center;
        font-family: 'Comic Sans MS', cursive;
    }
    h3 {
        color: #d4a5c3;
        text-align: center;
        font-family: 'Comic Sans MS', cursive;
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
    
    buf = BytesIO()
    cartoon_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="💾 Download Cartoon Image",
        data=byte_im,
        file_name="cartoon.png",
        mime="image/png"
    )
    
    st.success("💖 Ta-da! Your cartoon is ready!")
else:
    st.info("👆 Upload an image to get started!")