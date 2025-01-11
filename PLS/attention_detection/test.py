import cv2
from tensorflow.keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import time  # To track timestamps for inattentiveness
import os  # For debugging file save location

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the pre-trained model
model = load_model("keras_Model.h5", compile=False)

# Load the labels (e.g., "0 attentive", "1 distracted")
class_names = [line.strip() for line in open("labels.txt", "r").readlines()]

# Initialize the webcam
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Use macOS-specific backend

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Define the target image size for the model
size = (224, 224)

print("Press 'q' to exit the real-time prediction, or use Ctrl+C to stop the script.")

# Track inattentive timestamps
inattentive_timestamps = []

# Start time for tracking lecture duration
start_time = time.time()

try:
    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image.")
            break

        # Preprocess the frame (resize, normalize, etc.)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # Predict using the model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index].split()[1]  # Extract the label (e.g., "attentive", "distracted")
        confidence_score = prediction[0][index]

        # Log inattentive timestamps for "distracted"
        current_time = time.time() - start_time
        print(f"Predicted class: {class_name} | Confidence: {confidence_score:.2f}")
        if class_name.lower() == "distracted":  # Check for "distracted"
            inattentive_timestamps.append(current_time)
            print(f"Inattentive timestamp logged: {current_time:.2f} seconds")

        # Display the frame and prediction
        text = f"Class: {class_name} | Confidence: {confidence_score:.2f}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Real-Time Prediction", frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nScript interrupted by user (Ctrl+C). Cleaning up...")

finally:
    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Debugging: Print the save location and contents of inattentive_timestamps
    print(f"Current working directory: {os.getcwd()}")
    print(f"Inattentive timestamps: {inattentive_timestamps}")

    # Save inattentive timestamps to a file
    output_file = "inattentive_timestamps.txt"
    with open(output_file, "w") as f:
        for ts in inattentive_timestamps:
            f.write(f"{ts:.2f}\n")

    print(f"Inattentive timestamps saved to {output_file}")
