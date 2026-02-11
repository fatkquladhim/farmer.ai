from PIL import Image
import io

def compress_image(image_bytes, max_size=(1024, 1024), quality=65):
    """
    Resizes and compresses an image for low-bandwidth scenarios.
    Returns: BytesIO object of the compressed image.
    """
    try:
        if isinstance(image_bytes, bytes):
            img = Image.open(io.BytesIO(image_bytes))
        else:
            # Assume it's already a PIL Image or similar
            img = image_bytes
            
        # Convert to RGB if RGBA (JPEG doesn't support transparency)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            
        # Resize if larger than max_size
        img.thumbnail(max_size)
        
        # Save to buffer with compression
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)
        
        return buffer
    except Exception as e:
        print(f"Error compressing image: {e}")
        return None
