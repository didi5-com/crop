"""
File handling utilities for image uploads
"""
import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app


def allowed_file(filename):
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file
    
    Returns:
        Boolean indicating if file is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def generate_unique_filename(filename):
    """
    Generate unique filename to prevent collisions
    
    Args:
        filename: Original filename
    
    Returns:
        Unique filename with UUID prefix
    """
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return secure_filename(unique_name)


def save_upload_image(file, compress=True, max_size=(1024, 1024)):
    """
    Save uploaded image with optional compression
    
    Args:
        file: FileStorage object from request
        compress: Whether to compress the image
        max_size: Maximum dimensions (width, height)
    
    Returns:
        Relative path to saved image or None if error
    """
    try:
        if not file or not allowed_file(file.filename):
            return None
        
        # Generate unique filename
        filename = generate_unique_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Open and process image
        image = Image.open(file)
        
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        
        # Compress image if requested
        if compress:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save image
        image.save(filepath, optimize=True, quality=85)
        
        # Return relative path for database storage
        return f"uploads/{filename}"
    
    except Exception as e:
        current_app.logger.error(f"Error saving image: {str(e)}")
        return None


def delete_image(image_path):
    """
    Delete image file from uploads folder
    
    Args:
        image_path: Relative path to image (e.g., 'uploads/image.jpg')
    
    Returns:
        Boolean indicating success
    """
    try:
        if not image_path:
            return False
        
        # Construct full path
        full_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            os.path.basename(image_path)
        )
        
        # Delete file if it exists
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        
        return False
    
    except Exception as e:
        current_app.logger.error(f"Error deleting image: {str(e)}")
        return False


def get_image_url(image_path):
    """
    Convert relative image path to URL
    
    Args:
        image_path: Relative path (e.g., 'uploads/image.jpg')
    
    Returns:
        URL path for static file
    """
    if not image_path:
        return '/static/images/placeholder.jpg'
    
    return f"/static/{image_path}"
