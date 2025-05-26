import cv2
import numpy as np

def draw_ui_elements(frame):
    height, width = frame.shape[:2]

    # Define upper right rectangle coordinates
    rect_width, rect_height = 200, 100
    top_left = (width - rect_width - 10, 10)
    bottom_right = (width - 10, 10 + rect_height)

    # Create overlay and blend it with the frame
    overlay = frame.copy()
    cv2.rectangle(overlay, top_left, bottom_right, (153, 153, 153), -1)  # Gray rectangle
    cv2.rectangle(overlay, top_left, bottom_right, (0, 0, 0), 2)  # Black border

    alpha = 0.5  # 50% opacity
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    # Draw text instructions
    text = "Press 'q' to quit"
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (10, height - 20), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    return frame
