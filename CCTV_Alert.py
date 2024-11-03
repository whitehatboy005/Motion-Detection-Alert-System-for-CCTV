import cv2
import requests
from time import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')
BOT_TOKEN = "7787875894:AAFUdd-82IZbgg33vgViV70fHBIRJDOfZlQ"
CHAT_ID = os.getenv("CHAT_ID")
roi_start_point_str = os.getenv('ROI_START_POINT')
roi_end_point_str = os.getenv('ROI_END_POINT')
ip_camera_url = os.getenv("IP_CAMERA_URL")

def send_alert(photo_path):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    photo = open(photo_path, 'rb')
    files = {'photo': photo}
    payload = {
        'chat_id': CHAT_ID,
        'caption': 'Alert! An object has entered the restricted area.'
    }
    try:
        response = requests.post(url, data=payload, files=files)
        if response.status_code == 200:
            print("Alert with photo sent successfully!")
        else:
            print(f"Failed to send alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    finally:
        photo.close()

# Initialize video capture with IP camera URL
cap = cv2.VideoCapture(ip_camera_url)

# Convert ROI start and end points from strings to tuples
roi_start_point = tuple(map(int, roi_start_point_str.split(','))) if isinstance(roi_start_point_str, str) else roi_start_point_str
roi_end_point = tuple(map(int, roi_end_point_str.split(','))) if isinstance(roi_end_point_str, str) else roi_end_point_str

# Background subtractor and detection settings
background_subtractor = cv2.createBackgroundSubtractorMOG2()
min_contour_area = 5000
persistence_threshold = 5  # Frames required for persistent detection
alert_interval = 10  # Time in seconds between alerts
object_detected_frames = 0  # Counter for frames with persistent object detection
last_alert_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from IP camera")
        break

    # Draw the ROI for visualization
    cv2.rectangle(frame, roi_start_point, roi_end_point, (0, 255, 0), 2)

    # Extract the ROI from the frame
    roi = frame[roi_start_point[1]:roi_end_point[1], roi_start_point[0]:roi_end_point[0]]

    # Apply background subtraction to detect motion in the ROI
    fg_mask = background_subtractor.apply(roi)
    _, fg_mask = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY)
    fg_mask = cv2.dilate(fg_mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    object_in_roi = False
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            object_in_roi = True
            break

    # If object is detected within the ROI, increment the counter
    if object_in_roi:
        object_detected_frames += 1
    else:
        object_detected_frames = 0  # Reset if no object is detected in the ROI

    # Trigger alert if object is persistent in ROI and enough time has passed since last alert
    current_time = time()
    if object_detected_frames >= persistence_threshold and (current_time - last_alert_time) > alert_interval:
        photo_path = 'motion_alert.jpg'
        cv2.imwrite(photo_path, frame)
        send_alert(photo_path)
        last_alert_time = current_time
        object_detected_frames = 0  # Reset after alert

    # Display the frame with the ROI
    cv2.imshow('Frame', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
