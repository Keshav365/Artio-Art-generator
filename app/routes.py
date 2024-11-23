import os
from flask import Blueprint, render_template, request, jsonify, current_app
from app.models.stylegan_wrapper import StyleGANWrapper
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)
stylegan = None

def init_stylegan():
    global stylegan
    logger.info("Initializing StyleGAN...")
    try:
        model_path = current_app.config['MODEL_PATH']
        logger.info(f"Loading model from: {model_path}")
        stylegan = StyleGANWrapper(model_path)
        logger.info("StyleGAN initialized successfully!")
    except Exception as e:
        logger.error(f"Error initializing StyleGAN: {str(e)}")
        raise

@main.before_app_request
def before_request():
    global stylegan
    if stylegan is None:
        init_stylegan()

@main.route('/')
def index():
    logger.debug("Rendering index page")
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate():
    logger.info("Generate endpoint called")
    try:
        data = request.get_json()
        logger.debug(f"Received data: {data}")
        
        artist = data.get('artist', 'monet')
        genre = data.get('genre', 'landscape')
        style = data.get('style', 'impressionism')
        seed = data.get('seed', None)
        truncation = float(data.get('truncation', 1.0))
        
        logger.info(f"Generating image with: artist={artist}, genre={genre}, style={style}, seed={seed}, truncation={truncation}")
        
        # Generate image
        image = stylegan.generate_image(artist, genre, style, seed, truncation)
        
        # Save image
        filename = f"generated_{uuid.uuid4()}.png"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        logger.info(f"Saving image to: {save_path}")
        image.save(save_path)
        
        result = {
            'status': 'success',
            'image_url': f"/static/uploads/{filename}",
            'seed': seed
        }
        logger.info("Image generated and saved successfully")
        logger.debug(f"Returning result: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Optional: Add error handler
@main.errorhandler(Exception)
def handle_error(error):
    print(f"Error: {str(error)}")  # Add debugging
    response = {
        'status': 'error',
        'message': str(error)
    }
    return jsonify(response), 500
    
@main.route('/history')
def history():
    images = os.listdir(current_app.config['UPLOAD_FOLDER'])
    images = [img for img in images if img.startswith('generated_')]
    return render_template('history.html', images=images)

# @main.route('/download/<filename>')
# def download(filename):
#     return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# @main.route('/mix', methods=['POST'])
# def mix_styles():
#     data = request.get_json()
#     seed1 = data.get('seed1')
#     seed2 = data.get('seed2')
#     mixing_ratio = data.get('ratio', 0.5)
#     # ... implement style mixing logic ...

# @main.route('/batch', methods=['POST'])
# def batch_generate():
#     data = request.get_json()
#     num_images = data.get('num_images', 4)
#     # ... implement batch generation logic ...