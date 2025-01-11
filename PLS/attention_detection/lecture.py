import whisper
import os

# Step 1: Transcribe the lecture
def transcribe_audio(audio_file):
    """
    Transcribes audio using Whisper.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

# Step 2: Segment transcription into time chunks
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
        segment_text = " ".join(words[i * words_per_segment : (i + 1) * words_per_segment])
        segments[f"{start_time}-{end_time}"] = segment_text

    # Handle leftover words for the last segment
    if len(words) % words_per_segment != 0:
        segments[f"{end_time}-{lecture_duration}"] = " ".join(words[end_time * words_per_segment :])

    # Debug: Print transcription segments
    print("\nTranscription Segments:")
    for time_range, text in segments.items():
        print(f"{time_range}: {text}\n")

    return segments

# Step 3: Filter inattentive timestamps
def filter_inattentive_timestamps(timestamps, min_gap=5):
    """
    Filters inattentive timestamps to group timestamps that are too close.
    Keeps only timestamps separated by at least `min_gap` seconds.
    """
    filtered = []
    for ts in timestamps:
        if not filtered or ts - filtered[-1] >= min_gap:
            filtered.append(ts)
    return filtered

# Step 4: Map inattentive timestamps to transcription segments
def map_inattentive_timestamps(timestamps, segments):
    """
    Maps inattentive timestamps to transcription segments.
    """
    mapped_segments = []
    print("\nMapping Inattentive Timestamps to Segments:")
    for timestamp in timestamps:
        for time_range, segment in segments.items():
            start, end = map(int, time_range.split("-"))
            if start <= timestamp < end:
                mapped_segments.append((timestamp, segment))
                print(f"Timestamp {timestamp:.2f} mapped to: {time_range} -> {segment}")
                break
    return mapped_segments

# Main function
def main():
    audio_file = "extracted_audio.wav"
    timestamps_file = "inattentive_timestamps.txt"
    output_file = "attention_mapping.txt"
    lecture_duration = 1200  # Example: 20 minutes in seconds

    # Step 1: Check if timestamps exist
    if not os.path.exists(timestamps_file):
        print(f"Error: {timestamps_file} not found. Run test.py first.")
        return

    # Step 2: Transcribe the audio
    transcription = transcribe_audio(audio_file)
    print("\nTranscription completed.")

    # Step 3: Segment the transcription
    transcription_segments = segment_transcription(transcription, lecture_duration)

    # Step 4: Load inattentive timestamps and filter them
    with open(timestamps_file, "r") as f:
        inattentive_timestamps = [float(line.strip()) for line in f]
    filtered_timestamps = filter_inattentive_timestamps(inattentive_timestamps)

    # Step 5: Map timestamps to segments
    mapped_segments = map_inattentive_timestamps(filtered_timestamps, transcription_segments)

    # Step 6: Save the mapping
    with open(output_file, "w") as f:
        for timestamp, segment in mapped_segments:
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            f.write(f"At {minutes}:{seconds:02d}, inattentive during: {segment}\n")

    print(f"\nAttention mapping saved to {output_file}")

if __name__ == "__main__":
    main()
