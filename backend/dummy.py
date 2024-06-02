from flask import Flask, request, jsonify
import numpy as np
import os

app = Flask(__name__)

def recognize_food(image_path):
    return [{"label": "food1", "confidence": 0.9, "box": [100, 100, 50, 50]},
            {"label": "food2", "confidence": 0.85, "box": [200, 200, 60, 60]}]

def estimate_calories(predictions, diameter):
    plate_area = np.pi * (diameter / 2) ** 2
    caloric_info = []
    for pred in predictions:
        box = pred['box']
        box_area = (box[2] * box[3]) / 100
        height = 5 
        volume = box_area * height
        calories = volume * 100 / 100
        caloric_info.append({"label": pred['label'], "calories": calories})
    return caloric_info

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files or 'diameter' not in request.form:
        return jsonify({"error": "No file part or diameter provided"})
    
    file = request.files['file']
    diameter = float(request.form['diameter'])
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        
        food_predictions = recognize_food(file_path)
        caloric_info = estimate_calories(food_predictions, diameter)
        
        response = {
            'predictions': [{'label': info['label'], 'calories': info['calories']} for info in caloric_info],
        }
        
        return jsonify(response)

app.run(debug=True, host='127.0.0.1', port=5000)
