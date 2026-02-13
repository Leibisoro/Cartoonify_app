# ✨ Cartoonify - Image Cartoonification App

Transform your photos into adorable cartoons with this cute pastel-themed web application!

## 🎨 Features

- **Cute Pastel UI** - Beautiful pink and blue themed interface
- **Real-time Preview** - See original and cartoon side-by-side
- **Bright Cartoon Effect** - Vibrant colors with smooth skin tones
- **Easy Download** - Save your cartoonified images instantly
- **Mobile Friendly** - Works on phones, tablets, and computers

## 🚀 Technologies Used

- **Python** - Core programming language
- **OpenCV** - Image processing and cartoonification algorithms
- **Streamlit** - Web framework for easy deployment
- **PIL/Pillow** - Image handling
- **NumPy** - Array operations

## 📋 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/cartoonify-app.git
cd cartoonify-app
```

2. Install required packages:
```bash
pip install streamlit opencv-python pillow numpy
```

3. Run the application:
```bash
streamlit run cartoonify_web.py
```

4. Open your browser and go to `http://localhost:8501`

## 🖥️ Desktop Version

A standalone Windows executable (.exe) is also available for offline use.

To create the executable:
```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed cartoonify.py
```

Find the .exe in the `dist` folder.

## 🎯 How It Works

The cartoonification process uses several OpenCV techniques:

1. **Bilateral Filtering** - Smooths the image while preserving edges
2. **HSV Color Enhancement** - Increases saturation and brightness for vibrant cartoon colors
3. **Edge Detection** - Uses adaptive thresholding to create bold outlines
4. **Bitwise Operations** - Combines smooth colors with detected edges

## 📱 Live Demo

Try it online: [Add your deployed link here]

## 🖼️ Screenshots

[Add screenshots of your app here]

## 📝 Usage

1. Click "Upload an image"
2. Select a photo (JPG, PNG, or BMP)
3. Wait for the magic to happen!
4. Download your cartoonified image

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with 💖 by [Your Name]

## 🙏 Acknowledgments

- OpenCV community for image processing techniques
- Streamlit for the amazing web framework
- Inspiration from various cartoon filter tutorials

---

⭐ If you like this project, please give it a star on GitHub!

