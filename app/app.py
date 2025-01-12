import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key

# Define upload folder
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Global variable to control real-time detection
real_time_detection_active = False


@app.route("/", methods=["GET"])
def index():
    """
    Home page for starting real-time attentiveness detection.
    """
    return render_template("index.html")


@app.route("/start_detection", methods=["POST"])
def start_detection():
    """
    Start real-time detection using the webcam.
    """
    global real_time_detection_active
    real_time_detection_active = True
    flash("Real-time detection started. Press 'Stop' when done.")
    return render_template("detection.html")


@app.route("/stop_detection", methods=["POST"])
def stop_detection():
    """
    Stop real-time detection and move to the lecture upload page.
    """
    global real_time_detection_active
    real_time_detection_active = False  # Stop the video feed loop

    # Run the detection script to process real-time data
    try:
        subprocess.run(
            ["venv/bin/python", "PLS/attention_detection/test.py"],
            check=True,
        )
        flash("Real-time detection completed. Please upload the lecture video.")
        return redirect(url_for("upload_lecture"))
    except subprocess.CalledProcessError as e:
        flash(f"Error during detection: {e}")
        return redirect(url_for("index"))


@app.route("/upload_lecture", methods=["GET", "POST"])
def upload_lecture():
    """
    Upload a lecture video for transcription after stopping real-time detection.
    """
    if request.method == "POST":
        # Check if a lecture video is uploaded
        if "lecture_video" not in request.files or request.files["lecture_video"].filename == "":
            flash("Please upload a lecture video.")
            return redirect(request.url)

        # Save the lecture video
        lecture_video = request.files["lecture_video"]
        lecture_video_path = os.path.join(app.config["UPLOAD_FOLDER"], "lecture_" + lecture_video.filename)
        lecture_video.save(lecture_video_path)

        # Run the transcription mapping script
        try:
            subprocess.run(
                [
                    "whisper_env/bin/python",
                    "PLS/attention_detection/extra/transcription_mapping.py",
                ],
                check=True,
            )
            flash("Lecture video processed successfully!")
            return redirect(url_for("results"))
        except subprocess.CalledProcessError as e:
            flash(f"Error during processing: {e}")
            return redirect(request.url)

    return render_template("upload_lecture.html")


@app.route("/results", methods=["GET"])
def results():
    """
    Results page to display the processed transcription.
    """
    transcription_path = "distraction_analysis.json"
    if not os.path.exists(transcription_path):
        flash("No results found. Please process the lecture video first.")
        return redirect(url_for("index"))

    return render_template("results.html", transcription_file=transcription_path)


@app.route("/convert_to_pdf", methods=["GET"])
def convert_to_pdf():
    """
    Converts the distraction_analysis.json file into a PDF.
    """
    json_file = "distraction_analysis.json"
    pdf_file = "distraction_analysis.pdf"

    if not os.path.exists(json_file):
        flash("JSON file not found. Please process a video first.")
        return redirect(url_for("results"))

    try:
        # Load JSON data
        with open(json_file, "r") as file:
            data = json.load(file)

        # Create a PDF
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Add title
        c.drawString(100, 750, "Distraction Analysis Report")
        c.drawString(100, 735, "-" * 50)

        # Add JSON data to the PDF
        y_position = 700  # Start position for content
        for entry in data:
            timestamp = entry.get("distraction_timestamp", "N/A")
            transcription = entry.get("transcription", "N/A")
            segment_start = entry.get("segment_start", "N/A")
            segment_end = entry.get("segment_end", "N/A")

            text = f"Timestamp: {timestamp:.2f}s\n"
            text += f"  - Transcription: {transcription}\n"
            text += f"  - Segment: {segment_start:.2f}s to {segment_end:.2f}s\n"

            # Add text to PDF, handle page overflow
            for line in text.split("\n"):
                c.drawString(100, y_position, line)
                y_position -= 15
                if y_position < 50:  # Create a new page if space runs out
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = 750

        c.save()
        flash("PDF successfully generated!")
        return send_file(pdf_file, as_attachment=True)
    except Exception as e:
        flash(f"Error while creating PDF: {e}")
        return redirect(url_for("results"))


@app.route("/download/<filename>")
def download(filename):
    """
    Endpoint to download the results file.
    """
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash(f"File {filename} not found.")
        return redirect(url_for("results"))


@app.route("/video_feed")
def video_feed():
    """
    Video feed for real-time attentiveness detection.
    """
    return Response(generate_video_feed(), mimetype="multipart/x-mixed-replace; boundary=frame")


def generate_video_feed():
    """
    Generate frames for the real-time attentiveness detection feed.
    """
    import cv2

    global real_time_detection_active
    print("Starting video feed...")  # Debugging

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        flash("Error: Could not access webcam.")
        return

    while real_time_detection_active:  # Continue only if the flag is True
        ret, frame = cap.read()
        if not ret:
            break

        # Placeholder: Run attentiveness detection model here and annotate the frame
        text = "Real-Time Detection Active"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame for live streaming
        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    print("Exiting video feed...")  # Debugging
    cap.release()


if __name__ == "__main__":
    app.run(debug=True)
