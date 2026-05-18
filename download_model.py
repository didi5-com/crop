"""
Download pre-trained PlantVillage model
"""
import os
import requests
from pathlib import Path

def download_model():
    """Download the pre-trained model from Hugging Face"""
    
    model_dir = Path('models')
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = model_dir / 'plant_disease_model.h5'
    
    # Check if model already exists
    if model_path.exists():
        print(f"✓ Model already exists at {model_path}")
        return True
    
    print("Downloading PlantVillage disease detection model...")
    print("This may take a few minutes...")
    
    # Model URL - using a lightweight model for Render
    # Note: Replace with actual model URL when available
    model_url = "https://huggingface.co/liriope/PlantDiseaseDetection/resolve/main/plant_disease_efficientnetb4.h5"
    
    try:
        response = requests.get(model_url, stream=True, timeout=600)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rDownloading: {percent:.1f}%", end='')
        
        print(f"\n✓ Model downloaded successfully to {model_path}")
        print(f"Model size: {model_path.stat().st_size / (1024*1024):.2f} MB")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error downloading model: {e}")
        print("\nNote: Model download failed. The system will use API fallback.")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    download_model()
