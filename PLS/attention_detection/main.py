import subprocess
import os

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Step 1: Run Attention Detection (TensorFlow)
try:
    print("Running attention detection...")
    subprocess.run(["./venv/bin/python", "PLS/attention_detection/test.py"], check=True)
except FileNotFoundError as e:
    print(f"Error running attention detection: {e}")

# Step 2: Run Whisper Transcription
try:
    print("Running transcription mapping...")
    subprocess.run(["./whisper_env/bin/python", "PLS/attention_detection/extra/lecture.py"], check=True)
except FileNotFoundError as e:
    print(f"Error running transcription mapping: {e}")
