import os

def create_project_structure(base_dir):
    folders = [
        "app",
        "app/static",
        "app/templates",
        "app/utils",
        "data",
        "tests"
    ]
    files = [
        "app/__init__.py",
        "app/routes.py",
        "app/models.py",
        "app/utils/video_processing.py",
        "app/utils/audio_processing.py",
        "app/utils/transcription.py",
        "app/utils/attention_detection.py",
        "app/utils/note_generation.py",
        "app/utils/quiz_generation.py",
        "requirements.txt",
        "run.py"
    ]

    # Create folders
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")

    # Create empty files
    for file in files:
        file_path = os.path.join(base_dir, file)
        with open(file_path, "w") as f:
            f.write("")
        print(f"Created file: {file_path}")

# Set the base directory
base_directory = "personal_learning_system"
create_project_structure(base_directory)
