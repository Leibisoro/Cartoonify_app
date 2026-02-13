import web
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os

urls = (
    '/', 'Index',
    '/upload', 'Upload'
)

render = web.template.render('templates/')

class Index:
    def GET(self):
        return render.index()

class Upload:
    def POST(self):
        x = web.input(image={})
        
        if 'image' in x and x.image.filename:
            # Read uploaded image
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
            
            return render.result(original_b64, cartoon_b64)
        
        return render.index()

if __name__ == "__main__":
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app = web.application(urls, globals())
    app.run()




