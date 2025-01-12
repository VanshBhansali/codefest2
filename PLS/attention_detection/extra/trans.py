import whisper
import os
import subprocess
from pydub import AudioSegment


def transcribe_audio(audio_file):
    """
    Transcribes audio using Whisper.
    """
    print(f"Starting transcription for: {audio_file}")

    # Load the Whisper model
    model = whisper.load_model("base")  # Use 'small', 'medium', or 'large' if needed

    # Perform transcription
    try:
        result = model.transcribe(audio_file)
        print("Transcription completed.")
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""


def convert_to_wav(input_file, output_file="converted_audio.wav"):
    """
    Converts an audio file to WAV format using pydub.
    """
    print(f"Converting {input_file} to {output_file}...")
    try:
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="wav")
        print(f"Conversion to WAV completed: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None


def segment_transcription(transcription, lecture_duration, segment_duration=60):
    """
    Segments the transcription into time-based chunks.
    """
    words = transcription.split()
    total_segments = lecture_duration // segment_duration
    words_per_segment = len(words) // total_segments if total_segments > 0 else len(words)

    segments = {}
    for i in range(total_segments):
        start_time = i * segment_duration
        end_time = start_time + segment_duration
        segment_text = " ".join(words[i * words_per_segment: (i + 1) * words_per_segment])
        segments[f"{start_time}-{end_time}"] = segment_text

    if len(words) % words_per_segment != 0:
        segments[f"{end_time}-{lecture_duration}"] = " ".join(words[end_time * words_per_segment:])

    return segments


def main():
    audio_file = "PLS/attention_detection/extra/smalltest.mp4"  # Replace with your input audio file
    wav_file = "converted_audio.wav"
    timestamps_file = "inattentive_timestamps.txt"
    output_file = "attention_mapping.txt"
    lecture_duration = 1200  # Example: 20 minutes in seconds

    # Step 1: Convert audio to WAV if needed
    if not audio_file.endswith(".wav"):
        wav_file = convert_to_wav(audio_file)
        if not wav_file:
            print("Error: Audio conversion failed.")
            return

    # Step 2: Check if timestamps exist
    if not os.path.exists(timestamps_file):
        print(f"Error: {timestamps_file} not found. Run test.py first.")
        return

    # Step 3: Transcribe the audio
    transcription = transcribe_audio(wav_file)
    if not transcription:
        print("Error: Transcription failed.")
        return

    # Step 4: Segment the transcription
    transcription_segments = segment_transcription(transcription, lecture_duration)

    # Step 5: Load inattentive timestamps
    with open(timestamps_file, "r") as f:
        inattentive_timestamps = [float(line.strip()) for line in f]

    # Step 6: Map timestamps to segments
    mapped_segments = []
    for timestamp in inattentive_timestamps:
        for time_range, segment in transcription_segments.items():
            start, end = map(int, time_range.split("-"))
            if start <= timestamp < end:
                mapped_segments.append((timestamp, segment))
                break

    # Step 7: Save the mapping
    with open(output_file, "w") as f:
        for timestamp, segment in mapped_segments:
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            f.write(f"At {minutes}:{seconds:02d}, inattentive during: {segment}\n")

    print(f"Attention mapping saved to {output_file}")


if __name__ == "__main__":
    main()
