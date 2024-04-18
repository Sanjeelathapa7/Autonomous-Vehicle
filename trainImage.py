import cv2
import numpy as np
import os

# Function to perform bottle detection and training
def train_bottle_detector(yolo_config_path, yolo_weights_path, class_names, trainimage_path, message, text_to_speech):
    # Load YOLO model
    net = cv2.dnn.readNetFromDarknet(yolo_config_path, yolo_weights_path)
    
    # Load class names
    with open(class_names, 'r') as f:
        classes = f.read().splitlines()
    
    # Get image paths (assuming each image is labeled as "bottle")
    image_paths = [os.path.join(trainimage_path, img) for img in os.listdir(trainimage_path)][:50]  # Selecting the first 50 images
    
    # Loop over each image
    for img_path in image_paths:
        img = cv2.imread(img_path)
        height, width, _ = img.shape
        
        # Convert image to blob for YOLO input
        blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        
        # Get output layer names
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        
        # Forward pass to get predictions
        outs = net.forward(output_layers)
        
        # Process detections
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                # Filter detections with confidence threshold
                if confidence > 0.5 and classes[class_id] == 'bottle':
                    # Extract bounding box coordinates
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Draw bounding box and label
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, 'bottle', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
        # Display the image with detections
        cv2.imshow('Bottle Detection', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Inform about completion
    message.configure(text="Bottle")
    text_to_speech("Object Detection Completed")

# Example usage
train_bottle_detector("yolo_cfg/yolov3.cfg", "yolo_weights/yolov3.weights", "yolo_classes/coco.names", "train_images", "bottle", "object")
