from flask import Flask, request, send_file, jsonify, render_template
from PIL import Image
import io

app = Flask(__name__)

ALLOWED_FORMATS = ['jpg', 'jpeg', 'png', 'webp', 'tiff', 'bmp']

# 🔹 Homepage route (THIS FIXES 404)
@app.route('/')
def home():
    return render_template('index.html')

# 🔹 Image conversion route
@app.route('/convert', methods=['POST'])
def convert_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        target_format = request.form.get('format')

        if not target_format:
            return jsonify({'error': 'No format selected'}), 400

        target_format = target_format.lower()

        if target_format not in ALLOWED_FORMATS:
            return jsonify({'error': 'Unsupported format'}), 400

        img = Image.open(file)

        # Fix transparency issue for JPG/JPEG
        if target_format in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')

        img_bytes = io.BytesIO()
        img.save(img_bytes, format=target_format.upper())
        img_bytes.seek(0)

        return send_file(
            img_bytes,
            as_attachment=True,
            download_name=f'converted.{target_format}',
            mimetype=f'image/{target_format}'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
