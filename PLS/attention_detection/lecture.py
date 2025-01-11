import os
import subprocess
import whisper
import ssl

# Disable SSL verification temporarily
ssl._create_default_https_context = ssl._create_unverified_context


def extract_audio(video_file, output_audio_file):
    try:
        command = [
            "/opt/homebrew/bin/ffmpeg",  # Replace with the output of `which ffmpeg`
            "-i", video_file,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            output_audio_file
        ]

        subprocess.run(command, check=True)
        print(f"Audio extracted to {output_audio_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")


def transcribe_audio(audio_file):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""


def main():
    # Update paths as needed
    video_file = "PLS/attention_detection/extra/smalltest.mp4"  # Replace with the actual file path
    output_audio_file = "extracted_audio.wav"

    # Extract audio from the video file
    extract_audio(video_file, output_audio_file)

    # Transcribe the extracted audio
    print("Starting transcription...")
    transcription = transcribe_audio(output_audio_file)

    # Save the transcription to a file
    output_transcription_file = "transcription.txt"
    with open(output_transcription_file, "w") as f:
        f.write(transcription)
    print(f"Transcription saved to {output_transcription_file}")


if __name__ == "__main__":
    main()
