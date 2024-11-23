# run.py
import os
import sys
from pathlib import Path

# Add the StyleGAN2 repository to Python path
REPO_PATH = Path(__file__).parent / 'stylegan2-ada-pytorch'
if REPO_PATH.exists():
    sys.path.append(str(REPO_PATH))
else:
    print("Warning: StyleGAN2 repository not found. Cloning it now...")
    os.system('git clone https://github.com/NVlabs/stylegan2-ada-pytorch.git')
    sys.path.append(str(REPO_PATH))

# Create necessary directories
UPLOAD_DIR = Path(__file__).parent / 'app' / 'static' / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting server...")
    print(f"StyleGAN2 path: {REPO_PATH}")
    print(f"Upload directory: {UPLOAD_DIR}")
    app.run(debug=True, port=8080)