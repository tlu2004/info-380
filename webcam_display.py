import cv2
from ui_elements import draw_ui_elements  # Import the new function

# Open a connection to the default camera (0 is usually the default camera index)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

while True:
    # Capture frame-by-frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = draw_ui_elements(frame)  # Add UI overlays     
    
    # Display the resulting frame in a window called "Webcam"
    cv2.imshow('Webcam', frame)

    # Wait for 1 ms and cpython webcam_display.pyheck if 'q' key is pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()