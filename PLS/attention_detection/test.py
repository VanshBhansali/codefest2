import cv2
from tensorflow.keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import time  # To track timestamps for inattentiveness

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the pre-trained model
model = load_model("keras_Model.h5", compile=False)

# Load the labels (e.g., "Attentive", "Distracted")
class_names = open("labels.txt", "r").readlines()

# Initialize the webcam
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Use macOS-specific backend

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Define the target image size for the model
size = (224, 224)

print("Press 'q' to exit the real-time prediction.")

# Track inattentive timestamps
inattentive_timestamps = []

# Start time for tracking lecture duration
start_time = time.time()

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert the frame to RGB (OpenCV uses BGR by default)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to a PIL Image
    image = Image.fromarray(rgb_frame)

    # Resize and crop the image to fit the model input size
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Create a batch of one image
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Predict using the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # Log inattentive timestamps
    current_time = time.time() - start_time  # Time elapsed since the lecture started
    if class_name.lower() == "distracted":  # Replace with your model's class label for "Distracted"
        inattentive_timestamps.append(current_time)

    # Display the prediction and confidence score
    text = f"Class: {class_name} | Confidence: {confidence_score:.2f}"
    print(text)

    # Display the frame with prediction
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Real-Time Prediction", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Save inattentive timestamps to a file
with open("inattentive_timestamps.txt", "w") as f:
    for ts in inattentive_timestamps:
        f.write(f"{ts}\n")

print("\nInattentive timestamps saved to inattentive_timestamps.txt")
