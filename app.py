from flask import Flask, render_template, request, jsonify
from yolov8_model import detect_objects_and_text
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    data_url = request.json['image']
    image_data = base64.b64decode(data_url.split(',')[1])
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    object_labels, extracted_text = detect_objects_and_text(img)
    return jsonify({
        'labels': object_labels,
        'text': extracted_text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
