# app/models/stylegan_wrapper.py
import torch
import numpy as np
from PIL import Image
import sys
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Get the absolute path to the StyleGAN2 repository
REPO_PATH = Path(__file__).parent.parent.parent / 'stylegan2-ada-pytorch'
sys.path.insert(0, str(REPO_PATH))  # Insert at beginning of path

logger.info(f"StyleGAN2 repository path: {REPO_PATH}")
logger.info(f"Python path: {sys.path}")

# Try different import approaches
try:
    # First try the module import
    from stylegan2_ada_pytorch import legacy
    logger.info("Successfully imported from stylegan2_ada_pytorch package")
    load_network_pkl = legacy.load_network_pkl
except ImportError as e:
    logger.warning(f"Failed to import from stylegan2_ada_pytorch package: {e}")
    try:
        # Try direct import from repository
        sys.path.insert(0, str(REPO_PATH))
        import legacy
        logger.info("Successfully imported from repository directly")
        load_network_pkl = legacy.load_network_pkl
    except ImportError as e:
        logger.error(f"Failed to import legacy module: {e}")
        # One final attempt by copying legacy.py
        try:
            import shutil
            legacy_source = REPO_PATH / 'legacy.py'
            legacy_dest = Path(__file__).parent / 'legacy.py'
            shutil.copy2(legacy_source, legacy_dest)
            logger.info(f"Copied legacy.py from {legacy_source} to {legacy_dest}")
            from . import legacy
            load_network_pkl = legacy.load_network_pkl
            logger.info("Successfully imported from local copy")
        except Exception as e:
            logger.error(f"All import attempts failed: {e}")
            raise ImportError("Could not import required StyleGAN2 modules")

class StyleGANWrapper:
    def __init__(self, model_path):
        logger.info(f"Initializing StyleGANWrapper with model path: {model_path}")
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at path: {model_path}")
            raise FileNotFoundError(f"Model file not found: {model_path}")
            
        try:
            logger.info("Loading model...")
            with open(model_path, 'rb') as f:
                self.G = load_network_pkl(f)['G_ema'].to(self.device)
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}", exc_info=True)
            raise
        
        # Define style mappings
        self.artist_map = {
            'unknown': 0,
            'monet': 4,
            'van_gogh': 22
        }
        
        self.genre_map = {
            'abstract': 129,
            'landscape': 133,
            'portrait': 135
        }
        
        self.style_map = {
            'abstract_expressionism': 140,
            'impressionism': 152,
            'cubism': 147
        }
        
        logger.info("StyleGANWrapper initialized successfully")
    
    def generate_image(self, artist, genre, style, seed=None, truncation=1.0):
        """Generate an image with the specified parameters"""
        logger.info(f"Generating image with parameters: artist={artist}, genre={genre}, style={style}, seed={seed}, truncation={truncation}")
        
        if seed is None:
            seed = np.random.randint(0, 100000)
        logger.debug(f"Using seed: {seed}")
        
        # Set random seed
        torch.manual_seed(seed)
        np.random.seed(seed)
        
        try:
            # Generate latent vector
            logger.debug("Generating latent vector...")
            z = torch.randn(1, self.G.z_dim, device=self.device)
            logger.debug(f"Latent vector shape: {z.shape}")
            
            # Create labels tensor
            logger.debug("Creating labels tensor...")
            labels = torch.zeros((1, self.G.c_dim), device=self.device)
            labels[0, self.artist_map[artist]] = 1
            labels[0, self.genre_map[genre]] = 1
            labels[0, self.style_map[style]] = 1
            logger.debug(f"Labels tensor shape: {labels.shape}")
            
            # Generate image
            logger.info("Starting model inference...")
            with torch.no_grad():
                logger.debug("Running model forward pass...")
                img = self.G(z, labels, truncation_psi=truncation)
                logger.debug(f"Raw output shape: {img.shape}")
                
                logger.debug("Processing output...")
                img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
                logger.debug("Converted to uint8")
                
                img = img[0].cpu().numpy()
                logger.debug(f"Final numpy array shape: {img.shape}")
            
            logger.info("Image generation completed successfully")
            pil_image = Image.fromarray(img)
            logger.debug(f"PIL Image size: {pil_image.size}")
            
            return pil_image
            
        except Exception as e:
            logger.error(f"Error during image generation: {str(e)}", exc_info=True)
            raise