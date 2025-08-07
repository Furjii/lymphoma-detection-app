from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import uuid
from predict import LymphomaDetector
import time
from PIL import Image

# ===== Tambahan: Cek dan unduh model jika belum ada =====
MODEL_PATH = 'model/model0.h5'
if not os.path.exists(MODEL_PATH):
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    import gdown
    # Ganti URL berikut dengan link share Google Drive model kamu
    gdown.download('https://drive.google.com/file/d/1AL8MzQPdFW6aMxKZyR9l6lCxVfXx9RS9/view?usp=sharing', MODEL_PATH, quiet=False)

# ========================================================

app = Flask(__name__)
app.secret_key = 'lymphoma_detection_secret_key'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif'}  # Added 'tif' to the allowed extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Initialize the model with your model1.h5 file
detector = LymphomaDetector(model_path=MODEL_PATH, labels=['CLL', 'FL', 'MCL'])

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Create a unique filename to avoid overwriting
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        
        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if file.filename.lower().endswith('.tif'):
            img = Image.open(file)
            # Perbarui nama file agar ekstensi sesuai dengan gambar yang disimpan
            filename = filename.rsplit('.', 1)[0] + '.png'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(file_path)
        else:
            file.save(file_path)
            print(f"File saved at: {file_path}")
            print(f"Sent to HTML as filename: {filename}")

        # Resize the image to 224x224
        try:
            # Perform prediction
            prediction, confidence = detector.predict(file_path)
            
            confidence = min(max(confidence, 1), 100)
            
            # Get the timestamp for display
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Render results
            return render_template('result.html', 
                                filename=filename,
                                original=file.filename,
                                prediction=prediction, 
                                confidence=round(confidence, 2),
                                timestamp=timestamp)
        except Exception as e:
            flash(f'Error processing image: {str(e)}')
            # Delete the file if there's an error
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('index'))
    
    flash('Invalid file type. Please upload an image (png, jpg, jpeg, tif).')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create static/img directory for placeholder image
    os.makedirs('static/img', exist_ok=True)
    
    app.run(debug=True)
