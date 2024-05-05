
# import cv2
# from transformers import YolosImageProcessor, YolosForObjectDetection
# from PIL import Image
# import torch

# # Set device to CPU
# # device = torch.device('cpu')

# # Load the model and the processor
# model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
# image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

# # Initialize the external webcam (change the index to 1 or higher if needed)
# cap = cv2.VideoCapture(1)

# try:
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Convert the image from BGR color (which OpenCV uses) to RGB color
#         rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         pil_image = Image.fromarray(rgb_image)

#         # Process image
#         inputs = image_processor(images=pil_image, return_tensors="pt")
#         outputs = model(**inputs)

#         # Get predictions
#         target_sizes = torch.tensor([pil_image.size[::-1]])
#         results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

#         # Draw bounding boxes and labels on the original frame
#         for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
#             box = [int(i) for i in box.tolist()]
#             cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
#             cv2.putText(frame, f"{model.config.id2label[label.item()]}: {round(score.item(), 2)}",
#                         (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         # Display the resulting frame
#         cv2.imshow('Frame', frame)

#         # Press 'q' to quit
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
# finally:
#     # When everything done, release the capture
#     cap.release()
#     cv2.destroyAllWindows()


import cv2
from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
import torch
import serial
import time
import keyboard

# Initialize serial port for Arduino
ser = serial.Serial('COM4', 9600, timeout=1)

def send_command(command):
    ser.write(command.encode())

# Load the model and the processor
model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

# Initialize the external webcam
cap = cv2.VideoCapture(1)

try:
    while True:
        # Handle RC car control
        if keyboard.is_pressed('w'):
            send_command('F')
            print("Moving forward")
        elif keyboard.is_pressed('s'):
            send_command('B')
            print("Moving backward")
        elif keyboard.is_pressed('a'):
            send_command('L')
            print("Turning left")
        elif keyboard.is_pressed('d'):
            send_command('R')
            print("Turning right")
        elif keyboard.is_pressed('x'):
            send_command('S')
            print("Neutral")
            

        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            continue

        # Object detection process
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        inputs = image_processor(images=pil_image, return_tensors="pt")
        outputs = model(**inputs)
        target_sizes = torch.tensor([pil_image.size[::-1]])
        results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        stop = False  # Flag to stop the car if condition is met

        # Analyze detections and draw bounding boxes
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [int(i) for i in box.tolist()]
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(frame, f"{model.config.id2label[label.item()]}: {round(score.item(), 2)}",
                        (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # Define your stopping condition (example: if a 'person' is detected)
            if model.config.id2label[label.item()] == 'person' and score > 0.9:
                stop = True

        # Check if stop condition is met
        if stop:
            send_command('S')
            print("Stopping due to detection")

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
