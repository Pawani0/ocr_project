import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
import fitz
import cv2
import io
import numpy as np

def convert_pdf_to_images(path):
    doc = fitz.open(path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        images.append(image)
    return images

def images_to_text(pil_image):
    image_array = np.array(pil_image)  # Convert PIL to NumPy
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(gray_image)
    return text
def image_to_text(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(gray_image)
    return text

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    text = ""
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            if filename.lower().endswith('.pdf'):
                images = convert_pdf_to_images(path)
                for image in images:
                    text += images_to_text(image) + " "
            else:
                text = image_to_text(image=cv2.imread(path))

            os.remove(path)
    return render_template('index.html', text=text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
