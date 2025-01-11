import whisper
import subprocess
import os

# Step 1: Extract audio from video using FFmpeg
def extract_audio(video_file, output_audio_file):
    command = [
        "ffmpeg",  # Ensure FFmpeg is installed
        "-i", video_file,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio_file,
    ]
    subprocess.run(command, check=True)
    print(f"Audio extracted to {output_audio_file}")

# Step 2: Transcribe audio using Whisper
def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

# Step 3: Segment transcription into time-based chunks
def segment_transcription(transcription, lecture_duration, segment_duration=60):
    words = transcription.split()
    words_per_segment = len(words) // (lecture_duration // segment_duration)

    segments = {}
    for i in range(0, len(words), words_per_segment):
        start_time = (i // words_per_segment) * segment_duration
        end_time = start_time + segment_duration
        segments[f"{start_time}-{end_time}"] = " ".join(words[i:i + words_per_segment])

    return segments

# Step 4: Map inattentive timestamps to transcription segments
def map_inattentive_timestamps(timestamps, segments):
    mapped_segments = []
    for timestamp in timestamps:
        for time_range, segment in segments.items():
            start, end = map(int, time_range.split("-"))
            if start <= timestamp < end:
                mapped_segments.append((timestamp, segment))
                break
    return mapped_segments

# Main function to execute the workflow
def main():
    video_file = "PLS/attention_detection/extra/smalltest.mp4"  # Replace with your video file
    audio_file = "extracted_audio.wav"
    inattentive_file = "inattentive_timestamps.txt"

    # Extract audio
    extract_audio(video_file, audio_file)

    # Transcribe audio
    transcription = transcribe_audio(audio_file)
    print("Transcription completed!")

    # Segment transcription
    lecture_duration = 1200  # Example: 20-minute lecture (in seconds)
    segments = segment_transcription(transcription, lecture_duration)

    # Load inattentive timestamps
    with open(inattentive_file, "r") as f:
        inattentive_timestamps = [float(line.strip()) for line in f]

    # Map timestamps to segments
    mapped_segments = map_inattentive_timestamps(inattentive_timestamps, segments)

    # Save results
    with open("attention_mapping.txt", "w") as f:
        for timestamp, segment in mapped_segments:
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            f.write(f"At {minutes}:{seconds:02d}, inattentive during: {segment}\n")

    print("Attention mapping saved to attention_mapping.txt")

if __name__ == "__main__":
    main()
