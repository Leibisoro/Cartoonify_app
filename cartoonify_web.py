import web
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import json

urls = (
    '/', 'Index',
    '/upload', 'Upload'
)

INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cartoonify</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: #fef7f5;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            text-align: center;
            padding: 30px 0 0 0;
        }
        
        .title {
            font-size: 60px;
            font-weight: bold;
            color: #ffb3d9;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 18px;
            color: #d4a5c3;
            margin-bottom: 30px;
        }
        
        .content {
            flex: 1;
            padding: 0 40px 30px 40px;
            display: flex;
            flex-direction: column;
        }
        
        .display-frame {
            display: flex;
            gap: 20px;
            flex: 1;
            margin-bottom: 30px;
            min-height: 500px;
        }
        
        .image-panel {
            flex: 1;
            background: #fff5f8;
            border: 3px solid #ffc4dd;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
        }
        
        .image-panel.right {
            background: #f5f8ff;
            border-color: #c4ddff;
        }
        
        .panel-label {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            padding: 20px 0 10px 0;
        }
        
        .panel-label.original {
            color: #ff99cc;
        }
        
        .panel-label.cartoon {
            color: #99ccff;
        }
        
        .canvas-container {
            flex: 1;
            margin: 0 20px 20px 20px;
            background: #fffbfc;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .canvas-container.right {
            background: #fbfcff;
        }
        
        .canvas-container img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        
        .button-frame {
            text-align: center;
            padding-bottom: 20px;
        }
        
        .btn {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-size: 16px;
            font-weight: bold;
            color: white;
            border: none;
            padding: 18px 40px;
            margin: 0 10px;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.2s;
        }
        
        .btn-upload {
            background-color: #ffb3d9;
        }
        
        .btn-upload:hover {
            background-color: #ff99cc;
            transform: translateY(1px);
        }
        
        .btn-upload:active {
            transform: translateY(2px);
        }
        
        .btn-save {
            background-color: #d4a5c3;
        }
        
        .btn-save:disabled {
            background-color: #d4a5c3;
            opacity: 1;
            cursor: not-allowed;
        }
        
        .btn-save:not(:disabled) {
            background-color: #b8d4ff;
        }
        
        .btn-save:not(:disabled):hover {
            background-color: #99c2ff;
            transform: translateY(1px);
        }
        
        .btn-save:not(:disabled):active {
            transform: translateY(2px);
        }
        
        .status {
            text-align: center;
            font-size: 14px;
            color: #d4a5c3;
            padding-bottom: 20px;
        }
        
        input[type="file"] {
            display: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">✨ Cartoonify ✨</div>
        <div class="subtitle">Transform your photos into adorable cartoons</div>
    </div>
    
    <div class="content">
        <div class="display-frame">
            <div class="image-panel">
                <div class="panel-label original">💫 ORIGINAL 💫</div>
                <div class="canvas-container" id="original-canvas"></div>
            </div>
            
            <div class="image-panel right">
                <div class="panel-label cartoon">🎨 CARTOON 🎨</div>
                <div class="canvas-container right" id="cartoon-canvas"></div>
            </div>
        </div>
        
        <div class="button-frame">
            <input type="file" id="file-input" accept="image/*">
            <button type="button" class="btn btn-upload" onclick="document.getElementById('file-input').click()">
                🖼️ UPLOAD IMAGE
            </button>
            <button type="button" class="btn btn-save" id="save-btn" disabled onclick="saveImage()">
                💾 SAVE CARTOON
            </button>
        </div>
        
        <div class="status" id="status">✨ Ready to create magic! ✨</div>
    </div>
    
    <script>
        let cartoonImageData = null;
        
        document.getElementById('file-input').addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                document.getElementById('status').textContent = '✨ Creating magic... ✨';
                document.getElementById('status').style.color = '#ffb3d9';
                
                const formData = new FormData();
                formData.append('image', e.target.files[0]);
                
                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('original-canvas').innerHTML = 
                            '<img src="data:image/png;base64,' + data.original + '" alt="Original">';
                        document.getElementById('cartoon-canvas').innerHTML = 
                            '<img src="data:image/png;base64,' + data.cartoon + '" alt="Cartoon">';
                        
                        cartoonImageData = 'data:image/png;base64,' + data.cartoon;
                        document.getElementById('save-btn').disabled = false;
                        document.getElementById('status').textContent = '💖 Ta-da! Your cartoon is ready! 💖';
                        document.getElementById('status').style.color = '#ffb3d9';
                    } else {
                        document.getElementById('status').textContent = '❌ Oops! Something went wrong';
                        document.getElementById('status').style.color = '#ff9999';
                    }
                })
                .catch(error => {
                    document.getElementById('status').textContent = '❌ Oops! Something went wrong';
                    document.getElementById('status').style.color = '#ff9999';
                });
            }
        });
        
        function saveImage() {
            if (cartoonImageData) {
                const link = document.createElement('a');
                link.download = 'cartoon.png';
                link.href = cartoonImageData;
                link.click();
                
                document.getElementById('status').textContent = '💝 Saved successfully! Yay! 💝';
                document.getElementById('status').style.color = '#ffb3d9';
            }
        }
    </script>
</body>
</html>
"""

class Index:
    def GET(self):
        return INDEX_HTML

class Upload:
    def POST(self):
        try:
            x = web.input(image={})
            
            if 'image' not in x or not hasattr(x.image, 'file'):
                web.header('Content-Type', 'application/json')
                return json.dumps({'success': False})
            
            # Read image
            image_data = x.image.file.read()
            nparr = np.frombuffer(image_data, np.uint8)
            originalImage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
            
            # Cartoonify
            smoothed = originalImage.copy()
            for _ in range(2):
                smoothed = cv2.bilateralFilter(smoothed, 9, 75, 75)
            
            hsv = cv2.cvtColor(smoothed, cv2.COLOR_RGB2HSV).astype(np.float32)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)
            hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)
            hsv = hsv.astype(np.uint8)
            vibrant = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            
            gray = cv2.cvtColor(originalImage, cv2.COLOR_RGB2GRAY)
            gray_blur = cv2.medianBlur(gray, 7)
            edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                         cv2.THRESH_BINARY, 9, 8)
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            cartoonImage = cv2.bitwise_and(vibrant, edges_colored)
            
            # Convert to base64
            original_pil = Image.fromarray(originalImage)
            cartoon_pil = Image.fromarray(cartoonImage)
            
            original_buffer = BytesIO()
            cartoon_buffer = BytesIO()
            
            original_pil.save(original_buffer, format='PNG')
            cartoon_pil.save(cartoon_buffer, format='PNG')
            
            original_b64 = base64.b64encode(original_buffer.getvalue()).decode()
            cartoon_b64 = base64.b64encode(cartoon_buffer.getvalue()).decode()
            
            web.header('Content-Type', 'application/json')
            return json.dumps({
                'success': True,
                'original': original_b64,
                'cartoon': cartoon_b64
            })
        
        except Exception as e:
            web.header('Content-Type', 'application/json')
            return json.dumps({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


