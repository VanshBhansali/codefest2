import subprocess
import os

print("Running attention detection...")
try:
    subprocess.run(["python", "PLS/attention_detection/test.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error while running subprocess: {e}")
    print("Workflow completed.")
    exit()

# Check if inattentive timestamps were generated
timestamps_file = "PLS/attention_detection/inattentive_timestamps.txt"
if not os.path.exists(timestamps_file):
    print("No inattentive timestamps found. Skipping transcription.")
    exit()

# Run transcription mapping
print("Running transcription mapping...")
try:
    subprocess.run(["/path/to/whisper_env/bin/python", "PLS/attention_detection/lecture.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error while running transcription mapping: {e}")

print("Workflow completed.")
