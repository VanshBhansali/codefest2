import cv2
import numpy as np
from flask import Flask, render_template, Response
from tflite_runtime.interpreter import Interpreter

app = Flask(__name__)


interpreter = Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

CLASS_LABELS = ["Attentive", "Yawning", "Bored"]


def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (224, 224))  # Resize to model's input size
    normalized_frame = resized_frame / 255.0       # Normalize to [0, 1]
    return np.expand_dims(normalized_frame.astype('float32'), axis=0)


def generate_frames():
    cap = cv2.VideoCapture(0)  
    while True:
        success, frame = cap.read()
        if not success:
            break

       
        input_data = preprocess_frame(frame)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])
        predicted_class = np.argmax(predictions)

       
        label = CLASS_LABELS[predicted_class]
        cv2.putText(frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

  
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)