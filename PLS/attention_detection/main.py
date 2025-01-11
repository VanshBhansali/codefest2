import subprocess

try:
    # Run attention detection in the main environment
    print("Running attention detection...")
    subprocess.run(["python", "PLS/attention_detection/test.py"], check=True)

    # Run transcription mapping in the Whisper environment
    print("Running transcription mapping...")
    subprocess.run(["/path/to/whisper_env/bin/python", "PLS/attention_detection/lecture.py"], check=True)

    print("End-to-end workflow completed successfully!")

except KeyboardInterrupt:
    print("\nScript interrupted by user (Ctrl+C). Exiting gracefully...")

except subprocess.CalledProcessError as e:
    print(f"Error while running subprocess: {e}")

finally:
    print("Cleanup completed. Goodbye!")
