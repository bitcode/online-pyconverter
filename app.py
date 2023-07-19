from flask import Flask, request, send_from_directory, render_template
import os
import pyheif
from PIL import Image
from pyheif.error import HeifError
import tempfile

app = Flask(__name__)

def convert_heic_to_jpeg(heic_path, jpeg_path):
    try:
        heif_file = pyheif.read(heic_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(jpeg_path, format="JPEG")
        return True
    except HeifError as e:
        print(f"Failed to convert {heic_path} due to error: {str(e)}")
        return False

@app.route('/', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    if file:
        temp_dir = tempfile.mkdtemp()
        heic_path = os.path.join(temp_dir, file.filename)
        base_name = os.path.splitext(file.filename)[0]
        jpeg_path = os.path.join(temp_dir, f"{base_name}.jpg")
        file.save(heic_path)
        success = convert_heic_to_jpeg(heic_path, jpeg_path)
        if success:
            return send_from_directory(temp_dir, f"{base_name}.jpg", as_attachment=True)
        else:
            return {"error": "Failed to convert file."}, 400
    else:
        return {"error": "No file provided."}, 400

if __name__ == "__main__":
    app.run(debug=True)
