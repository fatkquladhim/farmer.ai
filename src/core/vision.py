import google.generativeai as genai
from PIL import Image
from utils.image_ops import compress_image
import io

def analyze_image(image_file):
    """
    Prepares an image for Gemini analysis.
    Auto-compresses if the image is too large.
    Returns: A PIL Image object ready for the API.
    """
    if not image_file:
        return None
        
    try:
        # Load image
        img = Image.open(image_file)
        
        # Check size (rough check), compress if needed
        # We'll just always run it through our compressor to be safe for "Low Bandwidth" simulation
        # In a real scenario, we might check file size first.
        
        compressed_buffer = compress_image(img)
        if compressed_buffer:
            return Image.open(compressed_buffer)
        else:
            return img # Fallback to original
            
    except Exception as e:
        print(f"Vision Prep Error: {e}")
        return None
