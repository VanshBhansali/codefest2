import subprocess
import os


def run_detection_script():
    """
    Runs the `test.py` script inside the `venv` virtual environment.
    """
    print("Running the detection script in 'venv' virtual environment...")
    try:
        subprocess.run(
            ["venv/bin/python", "PLS/attention_detection/test.py"],  # Correct path for test.py
            check=True
        )
        print("Detection script completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running detection script: {e}")
        exit(1)


def run_transcription_script():
    """
    Runs the transcription mapping script in the `whisper_env` virtual environment.
    """
    print("Running the transcription mapping script in 'whisper_env' virtual environment...")
    transcription_script_path = "./PLS/attention_detection/extra/transcription_mapping.py"  # Correct path for transcription_mapping.py
    try:
        subprocess.run(
            ["whisper_env/bin/python", transcription_script_path],  # Corrected path
            check=True
        )
        print("Transcription mapping completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running transcription mapping script: {e}")
        exit(1)


if __name__ == "__main__":
    # Step 1: Run the detection script
    run_detection_script()

    # Step 2: Check if the `inattentive_timestamps.txt` file exists
    timestamps_file = "inattentive_timestamps.txt"
    if not os.path.exists(timestamps_file):
        print(f"Error: '{timestamps_file}' not found. Ensure the detection script runs correctly.")
        exit(1)

    # Step 3: Run the transcription mapping script
    run_transcription_script()
