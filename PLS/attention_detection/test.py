import os
import subprocess
import whisper


def extract_audio(video_file, output_audio_file):
    """
    Extracts audio from a video file using FFmpeg.

    Args:
        video_file (str): Path to the video file.
        output_audio_file (str): Path to save the extracted audio file.
    """
    try:
        # Use FFmpeg to extract audio
        command = [
            "ffmpeg",
            "-i", video_file,  # Input video file
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # Audio codec
            "-ar", "16000",  # Sampling rate
            "-ac", "1",  # Channels
            output_audio_file  # Output audio file
        ]
        subprocess.run(command, check=True)
        print(f"Audio extracted to {output_audio_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")


def transcribe_audio(audio_file):
    """
    Transcribes audio into text using Whisper.

    Args:
        audio_file (str): Path to the audio file to transcribe.

    Returns:
        str: Transcribed text.
    """
    try:
        # Load Whisper model
        model = whisper.load_model("base")  # You can use 'tiny', 'small', 'medium', or 'large'
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""


def main():
    # File paths
    video_file = "lecture_video.mp4"  # Replace with your video file path
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
