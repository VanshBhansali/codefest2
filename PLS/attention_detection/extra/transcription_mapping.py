import os
import subprocess
import whisper
import json


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
        list: Transcription segments with timestamps and text.
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


def read_distraction_timestamps(file_path):
    """
    Reads distraction timestamps from a file.

    Args:
        file_path (str): Path to the file containing distraction timestamps.

    Returns:
        list: List of distraction timestamps in seconds.
    """
    try:
        with open(file_path, "r") as file:
            timestamps = [float(line.strip()) for line in file if line.strip()]
        print(f"Read {len(timestamps)} distraction timestamps from {file_path}.")
        return timestamps
    except Exception as e:
        print(f"Error reading distraction timestamps: {e}")
        return []


def map_distraction_to_transcription(distraction_timestamps, transcription_segments,
                                     output_file="distraction_analysis.json"):
    """
    Maps distraction timestamps to transcription segments and saves the result to a file.

    Args:
        distraction_timestamps (list): List of distraction timestamps in seconds.
        transcription_segments (list): List of transcription segments with timestamps and text.
        output_file (str): Path to save the distraction mapping results.
    """
    results = []

    for timestamp in distraction_timestamps:
        # Find the segment corresponding to the timestamp
        for segment in transcription_segments:
            if segment["start"] <= timestamp <= segment["end"]:
                results.append({
                    "distraction_timestamp": timestamp,
                    "transcription": segment["text"],
                    "segment_start": segment["start"],
                    "segment_end": segment["end"]
                })
                break

    # Save the results to a file
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Distraction mapping saved to: {output_file}")


if __name__ == "__main__":
    # Input video file
    video_path = "PLS/attention_detection/extra/smalltest.mp4"  # Replace with your video file path
    distraction_file = "inattentive_timestamps.txt"  # Path to file with distraction timestamps

    # Extract audio from the video
    audio_path = extract_audio(video_path)

    if audio_path:
        # Transcribe the extracted audio with timestamps
        segments = transcribe_audio_with_timestamps(audio_path)

        if segments:
            # Read distraction timestamps from the file
            distraction_timestamps = read_distraction_timestamps(distraction_file)

            if distraction_timestamps:
                # Map distractions to transcription and save results
                map_distraction_to_transcription(distraction_timestamps, segments)
