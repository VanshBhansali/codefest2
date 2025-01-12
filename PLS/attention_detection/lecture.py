import os
import subprocess
import whisper


def extract_audio(video_file, audio_file="extracted_audio.wav"):
    """
    Extracts audio from a video file using FFmpeg.

    Args:
        video_file (str): Path to the input video file.
        audio_file (str): Path to save the extracted audio file.

    Returns:
        str: Path to the extracted audio file.
    """
    try:
        # Run FFmpeg command to extract audio
        command = [
            "ffmpeg",
            "-i", video_file,  # Input file
            "-vn",  # Disable video
            "-acodec", "pcm_s16le",  # Audio codec
            "-ar", "16000",  # Set audio sample rate to 16kHz
            "-ac", "1",  # Set number of audio channels to 1
            audio_file  # Output audio file
        ]
        subprocess.run(command, check=True)
        print(f"Audio extracted to: {audio_file}")
        return audio_file
    except subprocess.CalledProcessError as e:
        print(f"Error during audio extraction: {e}")
        return None


def transcribe_audio_with_timestamps(audio_file, model_name="base"):
    """
    Transcribes audio to text with timestamps using Whisper.

    Args:
        audio_file (str): Path to the audio file.
        model_name (str): Whisper model name (default is 'base').

    Returns:
        list: Transcription segments with text and timestamps.
    """
    try:
        # Load the Whisper model
        model = whisper.load_model(model_name)
        print(f"Using Whisper model: {model_name}")

        # Transcribe the audio with timestamps
        result = model.transcribe(audio_file)
        print("Transcription complete.")

        # Extract segments with timestamps
        segments = result["segments"]
        return segments
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


if __name__ == "__main__":
    # Input video file
    video_path = "PLS/attention_detection/extra/smalltest.mp4"  # Replace with your video file path

    # Extract audio from the video
    audio_path = extract_audio(video_path)

    if audio_path:
        # Transcribe the extracted audio with timestamps
        segments = transcribe_audio_with_timestamps(audio_path)

        if segments:
            print("\nTranscription with Timestamps:")
            for segment in segments:
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"]
                print(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}")
