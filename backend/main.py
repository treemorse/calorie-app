from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
import pandas as pd

app = Flask(__name__)

net = cv2.dnn.readNet("yolov3_custom_final.weights", "cfg/yolov3_custom.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

caloric_table = {}
caloric_info_path = "data/calorie_infos.csv"

def load_caloric_info():
    global caloric_table
    df = pd.read_csv(caloric_info_path)
    for index, row in df.iterrows():
        food_name = row[1]
        calories_per_100g = row[3]
        caloric_table[food_name] = calories_per_100g

load_caloric_info()

def recognize_food(image_path):
    img = cv2.imread(image_path)
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    results = []
    for i in range(len(boxes)):
        if i in indexes:
            box = boxes[i]
            label = "food"
            results.append({"label": label, "confidence": confidences[i], "box": box})
    return results

def estimate_calories(predictions, diameter):
    plate_area = np.pi * (diameter / 2) ** 2
    caloric_info = []
    for pred in predictions:
        label = pred['label']
        box = pred['box']
        box_area = (box[2] * box[3]) / 100
        height = 5
        volume = box_area * height
        grams = volume * 1
        calories_per_100g = caloric_table.get(label, 0)
        calories = (grams / 100) * calories_per_100g
        caloric_info.append({"label": label, "calories": calories})
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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
