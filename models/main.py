from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

model = MobileNetV2(weights='imagenet')

def recognize_food(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    return tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=5)[0]

def estimate_volume(predictions):
    volumes = {}
    for pred in predictions:
        label = pred[1]
        volume = len(label) * 10
        volumes[label] = volume
    return volumes

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        
        food_predictions = recognize_food(file_path)
        volumes = estimate_volume(food_predictions)
        
        response = {
            'predictions': [{'label': pred[1], 'probability': float(pred[2])} for pred in food_predictions],
            'volumes': volumes
        }
        
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
