# StyleGAN2 Art Generator Web Interface

A web-based interface for generating art using StyleGAN2-ADA. This project allows you to generate artwork in different styles, including various artists, genres, and artistic styles.

## 🎨 Features

- Generate artwork using StyleGAN2-ADA
- Choose from different artists (Monet, Van Gogh, etc.)
- Select various genres (Landscape, Portrait, Abstract)
- Multiple artistic styles (Impressionism, Cubism, Abstract Expressionism)
- Adjustable parameters (seed, truncation)
- Web-based interface
- Real-time image generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Torch (CPU or CUDA)
- 8GB RAM minimum (16GB recommended)

### Getting the Model

Before starting, you'll need the WikiArt model file:

1. Download `WikiArt5.pkl` from [this link](https://archive.org/download/wikiart-stylegan2-conditional-model/WikiArt5.pkl)
2. Place it in the `app/models/` directory

### Installation

#### Windows

```bash
# Clone the repository
git clone https://github.com/yourusername/stylegan-art-generator.git
cd stylegan-art-generator

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Clone StyleGAN2-ADA repository
git clone https://github.com/NVlabs/stylegan2-ada-pytorch.git

# Create necessary directories
mkdir -p app\static\uploads
mkdir -p app\static\images

# Copy model file (if not already done)
copy path\to\your\WikiArt5.pkl app\models\
```

#### Unix/MacOS

```bash
# Clone the repository
git clone https://github.com/yourusername/stylegan-art-generator.git
cd stylegan-art-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Clone StyleGAN2-ADA repository
git clone https://github.com/NVlabs/stylegan2-ada-pytorch.git

# Create necessary directories
mkdir -p app/static/uploads
mkdir -p app/static/images

# Set permissions
chmod 755 app/static/uploads

# Copy model file (if not already done)
cp path/to/your/WikiArt5.pkl app/models/
```

### Running the Application

1. Activate the virtual environment if not already activated:

   ```bash
   # Windows
   venv\Scripts\activate

   # Unix/MacOS
   source venv/bin/activate
   ```

2. Start the Flask server:

   ```bash
   python run.py
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:8080
   ```

## 🎛️ Usage

1. Select an artist from the dropdown menu
2. Choose a genre for your artwork
3. Pick an artistic style
4. (Optional) Set a seed for reproducible results
5. Adjust the truncation value if desired
6. Click "Generate" to create your artwork

### Parameters Explained

- **Artist**: The artist's style to emulate (e.g., Monet, Van Gogh)
- **Genre**: The type of artwork to generate (e.g., Landscape, Portrait)
- **Style**: The artistic style to apply (e.g., Impressionism, Cubism)
- **Seed**: A number that determines the random generation (same seed = same image)
- **Truncation**: Controls variation vs. quality (lower = more typical, higher = more varied)

## 🛠️ Technical Details

### Directory Structure

```
stylegan-art-generator/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── stylegan_wrapper.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── uploads/
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   └── routes.py
├── stylegan2-ada-pytorch/
├── config.py
├── requirements.txt
└── run.py
```

### Configuration

You can configure the application by modifying `config.py` or setting environment variables:

```python
# config.py example
MODEL_PATH = 'path/to/your/WikiArt5.pkl'
DEBUG = True
```

Or create a `.env` file:

```bash
SECRET_KEY=your-secret-key
MODEL_PATH=/path/to/your/WikiArt5.pkl
```

## 🙏 Acknowledgments

- [StyleGAN2-ADA PyTorch](https://github.com/NVlabs/stylegan2-ada-pytorch) by NVIDIA
- Original WikiArt model training by [Justin Pinkney](https://www.justinpinkney.com/)

## ❗ Troubleshooting

### Common Issues

1. **Import Errors**:

   - Make sure StyleGAN2-ADA repository is cloned correctly
   - Check Python path includes the repository

2. **CUDA Issues**:

   - Verify CUDA toolkit version matches PyTorch version
   - CPU-only operation is supported but slower

3. **Memory Issues**:
   - Reduce batch size
   - Use CPU if GPU memory is insufficient


## 📧 Contact

Your Name - Shivam Goyal

Project Link: [https://github.com/Keshav365/Artio-Art-generator](https://github.com/Keshav365/Artio-Art-generator)
