import subprocess

# Define the Python paths for the two virtual environments
detection_env_python = "venv/bin/python"
whisper_env_python = "whisper_env/bin/python"

try:
    # Step 1: Run attention detection using the detection environment
    print("Running attention detection...")
    subprocess.run([detection_env_python, "PLS/attention_detection/test.py"], check=True)

    # Step 2: Check for inattentive timestamps
    inattentive_timestamps_path = "inattentive_timestamps.txt"
    try:
        with open(inattentive_timestamps_path, "r") as f:
            inattentive_timestamps = f.readlines()
    except FileNotFoundError:
        inattentive_timestamps = []

    if inattentive_timestamps:
        print("Inattentive timestamps found. Proceeding to transcription mapping...")

        # Step 3: Run Whisper transcription using the Whisper environment
        subprocess.run([whisper_env_python, "PLS/attention_detection/lecture.py"], check=True)
        print("Transcription mapping completed successfully!")
    else:
        print("No inattentive timestamps found. Skipping transcription.")

except subprocess.CalledProcessError as e:
    print(f"Error while running subprocess: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
