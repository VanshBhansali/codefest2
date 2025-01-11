import whisper

# Load transcription from Whisper
def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

# Map timestamps to transcription segments
def segment_transcription(transcription, inattentive_timestamps):
    segments = transcription.split(". ")  # Split transcription by sentences
    segment_duration = len(transcription) // len(segments)  # Approx. duration per segment

    mapped = []
    for timestamp in inattentive_timestamps:
        index = int(timestamp // segment_duration)
        if index < len(segments):
            mapped.append((timestamp, segments[index]))
    return mapped

# Main function
if __name__ == "__main__":
    import sys

    # Load inattentive timestamps
    with open("inattentive_timestamps.txt", "r") as f:
        inattentive_timestamps = [float(line.strip()) for line in f.readlines()]

    # Transcribe the audio
    audio_file = "extracted_audio.wav"
    transcription = transcribe_audio(audio_file)

    # Map inattentive timestamps to segments
    mapped_segments = segment_transcription(transcription, inattentive_timestamps)

    # Print results
    for timestamp, segment in mapped_segments:
        minutes = int(timestamp // 60)
        seconds = int(timestamp % 60)
        print(f"At {minutes}:{seconds:02d}, the person was inattentive during: {segment}")
