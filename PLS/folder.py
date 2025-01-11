import os

def create_project_structure(base_dir):
    # Define folders and files to be created
    folders = [
        "static",
        "templates"
    ]
    files = [
        "app.py",
        "requirements.txt",
        "templates/index.html"
    ]

    # Create base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Create folders
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")

    # Create files
    for file in files:
        file_path = os.path.join(base_dir, file)
        with open(file_path, "w") as f:
            f.write("")  # Create an empty file
        print(f"Created file: {file_path}")

# Set the base directory for your project
base_directory = "attention_detection_web"
create_project_structure(base_directory)

print("Project structure created successfully!")