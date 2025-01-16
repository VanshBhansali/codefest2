# CodeFest2: Attention Detection and Transcription Mapping

## Overview
CodeFest2 is a project designed to detect user attention during a lecture or video session and map inattentive timestamps to transcription segments. The system combines real-time attention detection with transcription and timestamp mapping for insightful analytics.

### Features
- **Real-Time Attention Detection**: Detects whether a user is attentive or distracted using a pre-trained deep learning model.
- **Audio Transcription**: Transcribes audio from the lecture or video.
- **Timestamp Mapping**: Maps inattentive timestamps to corresponding segments in the transcription.
- **Filtering**: Groups inattentive timestamps to avoid noise and redundant data.

---

## Directory Structure
```
codefest2/
├── PLS/
│   ├── attention_detection/
│   │   ├── test.py
│   │   ├── lecture.py
│   │   ├── main.py
│   │   ├── extra/
│   │   │   ├── trans.py
├── extracted_audio/
├── inattentive_timestamps.txt
├── attention_mapping.txt
├── README.md
├── requirements.txt
```

---

## Requirements
The project uses two separate Python virtual environments:
1. **Attention Detection Environment**
2. **Transcription Environment**

### Prerequisites
- Python 3.8 or higher
- `virtualenv`

---

## Setup and Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/VanshBhansali/codefest2.git
cd codefest2
```

### Step 2: Install Dependencies

#### Attention Detection Environment
1. Create and activate the virtual environment:
   ```bash
   virtualenv detection_env
   source detection_env/bin/activate  # For Windows: detection_env\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Transcription Environment
1. Create and activate the transcription virtual environment:
   ```bash
   virtualenv whisper_env
   source whisper_env/bin/activate  # For Windows: whisper_env\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install whisper moviepy
   ```

---

## How to Run

### Step 1: Extract Audio from MP4
Run the script to extract audio from your video file:
```bash
python PLS/attention_detection/extra/trans.py
```
This generates `extracted_audio.wav` from the input MP4 file.

### Step 2: Run Attention Detection
1. Activate the detection environment:
   ```bash
   source detection_env/bin/activate
   ```
2. Start the attention detection process:
   ```bash
   python PLS/attention_detection/main.py
   ```
This saves inattentive timestamps to `inattentive_timestamps.txt`.

### Step 3: Map Timestamps to Transcription
1. Activate the transcription environment:
   ```bash
   source whisper_env/bin/activate
   ```
2. Run the mapping script:
   ```bash
   python PLS/attention_detection/lecture.py
   ```
This generates `attention_mapping.txt` containing inattentive timestamps mapped to transcription segments.

---

## Output Files
- **`extracted_audio.wav`**: Extracted audio from the video.
- **`inattentive_timestamps.txt`**: Timestamps of detected distractions.
- **`attention_mapping.txt`**: Mapped inattentive timestamps to transcription segments.

---

## Troubleshooting
- **`ModuleNotFoundError`**: Ensure you activate the correct virtual environment before running scripts.
- **SSL Errors**: Update your Python environment to the latest version to avoid SSL certificate issues.
- **Dependencies**: Ensure all dependencies in `requirements.txt` and `whisper` are installed correctly.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing
Pull requests and contributions are welcome! Please ensure compatibility with the existing environments.

---

## Contact
For any issues or queries, contact **Vansh Bhansali** at [your-email@example.com](mailto:your-email@example.com).

---

**Happy Coding!**
