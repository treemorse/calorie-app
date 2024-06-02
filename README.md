# Calorie Counter Application

## Abstract

The Calorie Counter Application is designed to help users easily estimate the caloric content of their meals by analyzing food photographs. In today's health-conscious society, monitoring caloric intake is more important than ever. This app aims to provide a convenient and accurate tool for dietary tracking, helping users make informed decisions about their nutrition.

The application uses machine learning to recognize various food items in a photo and an algorithm to estimate their volume and weight. Users can capture or upload images, and the app will provide detailed nutritional information. This report outlines the objectives, research, system requirements, implementation details, and results of the project, providing a comprehensive overview of the development and functionality of the Calorie Counter Application.

## Table of Contents
1. [Introduction](#introduction)
    - [Objectives](#objectives)
2. [Research and Methodology](#research-and-methodology)
    - [Segmentation Model](#segmentation-model)
    - [Plate Size Identification Algorithm](#plate-size-identification-algorithm)
    - [3D Food Model Identification Algorithm](#3d-food-model-identification-algorithm)
    - [Empirical Results](#empirical-results)
3. [System Requirements](#system-requirements)
    - [Functional Requirements](#functional-requirements)
    - [Non-Functional Requirements](#non-functional-requirements)
4. [Project Implementation](#project-implementation)
    - [Mobile Application Architecture](#mobile-application-architecture)
    - [Backend System Architecture](#backend-system-architecture)
    - [System Integration](#system-integration)
    - [User Interface and Experience Design](#user-interface-and-experience-design)
5. [Conclusion](#conclusion)
6. [References](#references)

## Introduction

The Calorie Counter Application aims to provide a modern solution for accurately estimating the caloric content of meals by analyzing photographs of food. With the increasing focus on health and nutrition, there is a growing need for tools that simplify dietary tracking. Traditional methods of calorie counting are often tedious and prone to inaccuracies. This application leverages cutting-edge technology to streamline the process, making it accessible and reliable for users.

To achieve this, I developed a multiple object detection model capable of identifying various foods within a single image. I evaluated two advanced algorithms for this task: YOLO (You Only Look Once) and Single Shot MultiBox Detector (SSD). Following the identification of the food items, I estimate their volume by first determining the size of the plate they are placed on. This allows us to apply geometric modeling techniques to construct 3D representations of the food items and calculate their volumes.

Subsequently, I estimate the weight of each food item using a predefined table that maps volume to weight. Finally, I calculate the caloric content based on another table that maps food weight (per 100 grams) to calories. The application then delivers this detailed nutritional information to the user via a user-friendly interface, enhancing their ability to make informed dietary choices.

### Objectives
- Develop an effective multiple object detection model to identify various foods in an image.
- Implement an algorithm to estimate the size of the plate and the volume of each food item.
- Calculate the weight of each food item using volume-to-weight mappings.
- Determine the caloric content of each food item using weight-to-calorie mappings.
- Provide a user-friendly mobile application interface for capturing and analyzing food images.
- Deliver accurate and detailed nutritional information to users.

## Research and Methodology

### Segmentation Model: YOLO vs. SSD

**YOLO (You Only Look Once) Algorithm**

YOLO is an acronym for "You Only Look Once", a real-time object detection system. Initially developed by Joseph Redmon and further enhanced by Alexey Bochkovskiy, Chien Yao Wang, and Hong Yuan Mark Liao, YOLO has become one of the most widely used algorithms for object detection due to its speed and accuracy.

The key advantage of YOLO lies in its ability to perform real-time object detection with high precision and recall rates. YOLO operates using a single-stage detection method, meaning it only looks at the image once to make predictions, making it significantly faster than other algorithms that require multiple passes. YOLO is open-source and relatively easy to install and customize, which has contributed to its widespread adoption.

The YOLOv3 architecture consists of four main stages:

1. **Input**: This stage involves resizing the input image to a resolution that is divisible by 32, accommodating the input layer's requirements. The input image is typically a color image with three channels (RGB).

2. **Backbone**: The backbone is the core component responsible for feature extraction. YOLOv3 uses Darknet-53 as its backbone, which employs Cross Stage Partial Networks (CSP) to divide the input feature map into two parts, enhancing feature extraction.

3. **Neck**: The neck serves as an intermediary layer between the backbone and the dense prediction layer. It helps detect objects of various sizes by constructing feature pyramids through upsampling and concatenation techniques.

4. **Dense Prediction**: This stage involves predicting bounding boxes and classifying objects within those boxes. YOLOv3 divides the input image into grid cells, each containing an anchor box for predictions. Non-Max Suppression (NMS) is used to handle overlapping predictions by selecting the anchor box with the highest Intersection over Union (IoU) with the ground truth.

The performance of YOLOv3 in the study (refferenced later) demonstrated its effectiveness with an average precision of 0.94, a recall of 0.90, and an F1-score of 0.91. These metrics indicate that YOLOv3 is highly reliable for real-time food detection tasks, making it the preferred choice for our calorie estimation application[^1].

**Single Shot MultiBox Detector (SSD)**

The Single Shot MultiBox Detector (SSD) is another popular object detection model, introduced by Wei Liu and colleagues. SSD eliminates the need for a separate proposal generation stage, integrating object localization and classification into a single pass through the network. This design simplifies training and inference, making SSD both efficient and accurate.

SSD's architecture involves:

1. **Default Boxes**: SSD discretizes the output space of bounding boxes into a set of default boxes of different aspect ratios and scales at each feature map location. During prediction, the network generates scores for the presence of each object category in each default box and adjusts the boxes to better match the object shapes.

2. **Multi-scale Feature Maps**: SSD combines predictions from multiple feature maps of different resolutions. This approach allows the network to handle objects of various sizes more effectively.

3. **Loss Function**: The SSD training objective combines localization loss (measuring the accuracy of bounding box predictions) and confidence loss (measuring the accuracy of class predictions). The network matches default boxes to ground truth boxes during training, optimizing for both aspects simultaneously[^2].

SSD evaluates a small set of default boxes of different aspect ratios at each location in several feature maps with different scales. Each default box predicts both the shape offsets and the confidences for all object categories. During training, these default boxes are matched to the ground truth boxes, with matched boxes treated as positives and the rest as negatives. The final detections are produced after a non-maximum suppression step, which refines the bounding box predictions.

**Comparison and Choice of Model**

In our project, I chose to use the YOLOv3 model for food detection due to its balance of speed and accuracy. The decision was based on the following factors:

- **Speed**: YOLOv3's real-time processing capabilities (45 FPS) make it ideal for applications where quick detection is crucial.
- **Accuracy**: YOLOv3 provides high accuracy with its advanced feature extraction and multi-scale predictions, essential for detecting various food items in different contexts.
- **Implementation Ease**: YOLOv3's architecture is well-documented and has extensive support in the machine learning community, making it easier to implement and customize for our specific needs.

### Plate Size and Food Volume Estimation Algorithms

An interesting approach to constructing the spatial relationships between the objects involves using the serving container itself as the reference to link the image scale with the world coordinate system. This method uses a circular dining plate, where the diameter must be measured and the depth can be estimated or ignored for shallow plates. For bowls, both the diameter and height must be measured.

This approach requires the calculation of the camera's perspective matrix through a calibration procedure, fitting the plate boundary to an ellipse equation, and using the ellipse as the base of a quadric cone to determine the plate's position and orientation. The food plane is then shifted based on the plate depth value to obtain the geometric constraints necessary for a 3D/2D food model registration process[^3].

While this method provides a somewhat precise way to determine the position and orientation of the food plane and subsequently estimate food volume using a 3D geometric shape library, it is complex and requires extensive computation.

**Simplified Method Used in This Project**

Due to the complexity of the aforementioned method, I opted for a simpler approach to estimate the volume of food items. The steps include:

1. **User Input**: The user provides the diameter of the plate, which serves as a reference for size calculations.

2. **Image Processing**: The YOLOv3 model detects food items and provides bounding boxes around them.

3. **Volume Calculation**: I approximate the volume of each food item by assuming simple geometric shapes (e.g., cylinders, spheres) based on the bounding box dimensions and the known plate size. For instance, if a food item is approximated as a cylinder, the volume \( V \) is calculated as \( V = \pi \times (r^2) \times h \), where \( r \) is the radius and \( h \) is the height.

This simplified method allows us to quickly and effectively estimate the volume of food items with reasonable accuracy, making it suitable for our application without the need for complex calibration procedures.


## Requirements

### Functional Requirements
- **Food Detection**: The application must detect multiple food items in an image.
- **Volume Estimation**: The application must estimate the volume of each detected food item based on the provided plate diameter.
- **Calorie Calculation**: The application must calculate the calories for each detected food item using a predefined table of food items and their caloric values.
- **User Interaction**: The application must allow users to upload images and provide the plate diameter via a chat interface.
- **Response Generation**: The application must generate a response containing the detected food items, their volumes, and calorie estimations.

### Non-Functional Requirements
- **Performance**: The application should provide food detection and volume estimation results within a few seconds.
- **Usability**: The user interface should be intuitive and easy to use, with clear instructions for uploading images and entering plate diameter.

## Project Implementation

### Mobile App Architecture
The mobile app is developed using Flutter. It features a chat interface where users can upload images and provide the plate diameter. The app communicates with the backend server to get food detection, volume estimation, and caloric information.

### Backend Architecture
The backend server is built using Flask and utilizes the Darknet framework for running the YOLOv3 model. Darknet is an open-source neural network framework written in C and CUDA, making it ideal for high-performance tasks like real-time object detection[^4]. The backend processes images, runs the YOLOv3 model for food detection, and estimates the volume and calories of detected food items based on a predefined caloric table.

- **Food Detection Model**: The YOLOv3 model, configured for food detection, is loaded using OpenCV's DNN module. The model is trained using Darknet, which provides robust performance for real-time object detection tasks.
- **Size Estimation Algorithm**: A simplified algorithm estimates the volume of food items using bounding box dimensions and the provided plate diameter.
- **Calorie Calculation**: The backend uses a table to map the estimated volume of food items to their caloric values.

### Integration
The frontend (Flutter app) sends images and plate diameter to the backend server via HTTP POST requests. The backend processes the request, runs the YOLOv3 model, estimates volumes and calories, and returns the results to the frontend, which displays the information to the user.

### UI/UX
The app features a chat interface for user interaction. Users can upload images via camera or gallery and provide the plate diameter. The interface supports dark and light themes, improving usability and user experience.

## Conclusion
This project successfully implements a mobile application for detecting food items, estimating their volumes, and calculating calories from a photo. The YOLOv3 model provides accurate food detection, and a simplified volume estimation algorithm offers reasonable approximations of food volumes. Further work can be done on improving volume estimation using a model-based approach and integrating a real-time database for better user data management. Hosting the backend on a cloud platform can also enhance scalability and accessibility.

## References
[^1]: [YOLO](https://www.researchgate.net/publication/376615136_Food_Image_Detection_System_and_Calorie_Content_Estimation_Using_Yolo_to_Control_Calorie_Intake_in_the_Body)
[^2]: [SSD](https://arxiv.org/pdf/1512.02325)
[^3]: [Model-based measurement](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3819104/pdf/nihms520784.pdf)
[^4]: [Darknet](https://github.com/AlexeyAB/darknet)