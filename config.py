import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

class Config:
    # Base directory of the project
    BASE_DIR = Path(__file__).parent
    
    # Debug mode
    DEBUG = True
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-testing'
    
    # Model path - update this to your actual model path
    MODEL_PATH = os.environ.get('MODEL_PATH') or str(BASE_DIR / 'WikiArt5.pkl')
    
    # Upload folder for generated images
    UPLOAD_FOLDER = str(BASE_DIR / 'app' / 'static' / 'uploads')
    
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Development specific settings
    PROPAGATE_EXCEPTIONS = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    def __init__(self):
        logging.info(f"Base directory: {self.BASE_DIR}")
        logging.info(f"Model path: {self.MODEL_PATH}")
        logging.info(f"Upload folder: {self.UPLOAD_FOLDER}")
        
        # Verify model file exists
        if not os.path.exists(self.MODEL_PATH):
            logging.error(f"Model file not found at: {self.MODEL_PATH}")
        else:
            logging.info("Model file found")