
import os
from pydub import AudioSegment

input_file = "extracted_audio.wav"
output_dir = "chunks/"
segment_duration = 60 * 1000  # 1 minute in milliseconds

print(f"Splitting {input_file} into chunks...")
audio = AudioSegment.from_file(input_file)
os.makedirs(output_dir, exist_ok=True)

for i, start in enumerate(range(0, len(audio), segment_duration)):
    end = start + segment_duration
    chunk = audio[start:end]
    chunk.export(f"{output_dir}/chunk_{i + 1}.wav", format="wav")
print(f"Audio split into {i + 1} chunks.")

import whisper
import os

model = whisper.load_model("base")
chunks_dir = "chunks/"
combined_transcription = []

for chunk_file in sorted(os.listdir(chunks_dir)):
    if chunk_file.endswith(".wav"):
        print(f"Transcribing {chunk_file}...")
        result = model.transcribe(os.path.join(chunks_dir, chunk_file))
        combined_transcription.append(result["text"])

full_transcription = "\n".join(combined_transcription)
print("Combined Transcription:")
print(full_transcription)
