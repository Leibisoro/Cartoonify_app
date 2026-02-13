import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Canvas
from PIL import ImageTk, Image

class CuteCartoonifyApp:
    def __init__(self):
        self.top = tk.Tk()
        self.top.geometry('1200x800')
        self.top.title('Cartoonify')
        self.top.configure(background='#fef7f5')
        
        self.cartoonified_image = None
        self.original_image_pil = None
        self.cartoon_image_pil = None
        
        header = tk.Frame(self.top, background='#fef7f5', height=100)
        header.pack(fill='x', pady=(30, 0))
        
        title = tk.Label(header, 
                        text="✨ Cartoonify ✨", 
                        font=('Comic Sans MS', 48, 'bold'),
                        fg='#ffb3d9',
                        bg='#fef7f5')
        title.pack()
        
        subtitle = tk.Label(header,
                           text="Transform your photos into adorable cartoons",
                           font=('Comic Sans MS', 14),
                           fg='#d4a5c3',
                           bg='#fef7f5')
        subtitle.pack()
        
        content = tk.Frame(self.top, background='#fef7f5')
        content.pack(expand=True, fill='both', padx=40, pady=30)
        
        self.display_frame = tk.Frame(content, background='#fef7f5')
        self.display_frame.pack(expand=True, fill='both')
        
        left_frame = tk.Frame(self.display_frame, background='#fff5f8', 
                             highlightbackground='#ffc4dd', highlightthickness=3)
        left_frame.pack(side='left', expand=True, fill='both', padx=(0, 10))
        
        left_label = tk.Label(left_frame,
                             text="💫 ORIGINAL 💫",
                             font=('Comic Sans MS', 14, 'bold'),
                             fg='#ff99cc',
                             bg='#fff5f8')
        left_label.pack(pady=(20, 10))
        
        self.original_canvas = Canvas(left_frame, 
                                     background='#fffbfc',
                                     highlightthickness=0)
        self.original_canvas.pack(expand=True, fill='both', padx=20, pady=(0, 20))
        
        right_frame = tk.Frame(self.display_frame, background='#f5f8ff',
                              highlightbackground='#c4ddff', highlightthickness=3)
        right_frame.pack(side='right', expand=True, fill='both', padx=(10, 0))
        
        right_label = tk.Label(right_frame,
                              text="🎨 CARTOON 🎨",
                              font=('Comic Sans MS', 14, 'bold'),
                              fg='#99ccff',
                              bg='#f5f8ff')
        right_label.pack(pady=(20, 10))
        
        self.cartoon_canvas = Canvas(right_frame,
                                    background='#fbfcff',
                                    highlightthickness=0)
        self.cartoon_canvas.pack(expand=True, fill='both', padx=20, pady=(0, 20))
        
        button_frame = tk.Frame(self.top, background='#fef7f5')
        button_frame.pack(pady=(0, 40))
        
        self.upload_btn = tk.Button(button_frame,
                                   text="🖼️ UPLOAD IMAGE",
                                   command=self.upload,
                                   font=('Comic Sans MS', 13, 'bold'),
                                   fg='#ffffff',
                                   bg='#ffb3d9',
                                   activeforeground='#ffffff',
                                   activebackground='#ff99cc',
                                   bd=0,
                                   padx=35,
                                   pady=15,
                                   cursor='hand2',
                                   relief='raised')
        self.upload_btn.pack(side='left', padx=10)
        
        self.save_btn = tk.Button(button_frame,
                                 text="💾 SAVE CARTOON",
                                 command=self.save_image,
                                 font=('Comic Sans MS', 13, 'bold'),
                                 fg='#ffffff',
                                 bg='#d4a5c3',
                                 activeforeground='#ffffff',
                                 activebackground='#c394b3',
                                 bd=0,
                                 padx=35,
                                 pady=15,
                                 state='disabled',
                                 cursor='hand2',
                                 relief='raised')
        self.save_btn.pack(side='left', padx=10)
        
        self.status = tk.Label(self.top,
                              text="✨ Ready to create magic! ✨",
                              font=('Comic Sans MS', 11),
                              fg='#d4a5c3',
                              bg='#fef7f5')
        self.status.pack(pady=(0, 20))
        
        self.bind_hover_effects()
        
    def bind_hover_effects(self):
        def on_enter_upload(e):
            self.upload_btn.config(bg='#ff99cc', relief='sunken')
        
        def on_leave_upload(e):
            self.upload_btn.config(bg='#ffb3d9', relief='raised')
        
        def on_enter_save(e):
            if self.save_btn['state'] != 'disabled':
                self.save_btn.config(bg='#c394b3', relief='sunken')
        
        def on_leave_save(e):
            if self.save_btn['state'] != 'disabled':
                self.save_btn.config(bg='#d4a5c3', relief='raised')
        
        self.upload_btn.bind('<Enter>', on_enter_upload)
        self.upload_btn.bind('<Leave>', on_leave_upload)
        self.save_btn.bind('<Enter>', on_enter_save)
        self.save_btn.bind('<Leave>', on_leave_save)
    
    def upload(self):
        self.status.config(text="🌸 Selecting your image... 🌸", fg='#ffb3d9')
        self.top.update()
        
        ImagePath = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if ImagePath:
            self.status.config(text="✨ Creating magic... ✨", fg='#ffb3d9')
            self.top.update()
            self.cartoonify(ImagePath)
        else:
            self.status.config(text="🎀 No image selected 🎀", fg='#d4a5c3')
    
    def cartoonify(self, ImagePath):
        try:
            originalImage = cv2.imread(ImagePath)
            originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
            
            if originalImage is None:
                self.status.config(text="❌ Oops! Could not load image", fg='#ff9999')
                return
            
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
            
            edges = cv2.adaptiveThreshold(
                gray_blur,
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                9,
                8
            )
            
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            cartoonImage = cv2.bitwise_and(vibrant, edges_colored)
            
            self.cartoonified_image = cartoonImage
            
            self.display_images(originalImage, cartoonImage)
            
            self.save_btn.config(state='normal', 
                               fg='#ffffff', 
                               bg='#b8d4ff',
                               activebackground='#99c2ff',
                               activeforeground='#ffffff')
            
            self.status.config(text="💖 Ta-da! Your cartoon is ready! 💖", fg='#ffb3d9')
            
        except Exception as e:
            self.status.config(text=f"❌ Oops! {str(e)}", fg='#ff9999')
    
    def display_images(self, original, cartoon):
        self.original_image_pil = Image.fromarray(original)
        self.cartoon_image_pil = Image.fromarray(cartoon)
        
        self.update_canvas_image(self.original_canvas, self.original_image_pil)
        self.update_canvas_image(self.cartoon_canvas, self.cartoon_image_pil)
    
    def update_canvas_image(self, canvas, pil_image):
        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 500
            canvas_height = 400
        
        img_width, img_height = pil_image.size
        scale = min(canvas_width / img_width, canvas_height / img_height)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        resized = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(resized)
        
        canvas.delete("all")
        x = canvas_width // 2
        y = canvas_height // 2
        canvas.create_image(x, y, image=photo, anchor='center')
        
        canvas.image = photo
    
    def save_image(self):
        if self.cartoonified_image is not None:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), 
                          ("JPEG files", "*.jpg"),
                          ("All files", "*.*")]
            )
            
            if save_path:
                try:
                    save_image = cv2.cvtColor(self.cartoonified_image, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(save_path, save_image)
                    self.status.config(text="💝 Saved successfully! Yay! 💝", fg='#ffb3d9')
                except Exception as e:
                    self.status.config(text=f"❌ Error saving: {str(e)}", fg='#ff9999')
            else:
                self.status.config(text="🎀 Save cancelled 🎀", fg='#d4a5c3')
    
    def run(self):
        self.top.mainloop()

if __name__ == "__main__":
    app = CuteCartoonifyApp()
    app.run()