# ML-Based Disease Detection Implementation

## Overview
Implemented local machine learning-based disease detection using the PlantVillage dataset to replace inaccurate API-based detection.

## Changes Made

### 1. New ML Disease Detector (`app/services/ml_disease_detector.py`)
- Uses pre-trained EfficientNetB4 model from Hugging Face
- Trained on PlantVillage dataset (54,000+ images, 38 disease classes)
- Achieves 97.66% accuracy
- Supports 14 crop species and 38 disease classes

### 2. Updated Disease Detection Pipeline (`app/services/disease_detector.py`)
- ML model is now the primary detection method
- Plant.id API serves as fallback if ML detection fails
- Maintains hybrid pipeline architecture:
  1. Image Quality Validation
  2. Crop Species Identification  
  3. **ML-Based Disease Detection** (NEW)
  4. Confidence Filtering
  5. Treatment Recommendations

### 3. Model Download Script (`download_model.py`)
- Downloads pre-trained model from Hugging Face during build
- Handles download failures gracefully
- Falls back to API if model unavailable

### 4. Updated Dependencies (`requirements.txt`)
- Added TensorFlow >= 2.15.0 for model inference
- Maintains compatibility with existing dependencies

### 5. Updated Build Script (`build.sh`)
- Downloads ML model during deployment
- Creates necessary directories
- Initializes database

## Supported Crops and Diseases

### Crops (14 species):
- Apple
- Blueberry
- Cherry
- Corn (Maize)
- Grape
- Orange
- Peach
- Pepper (Bell)
- Potato
- Raspberry
- Soybean
- Squash
- Strawberry
- Tomato

### Disease Classes (38 total):
Including but not limited to:
- Apple: Scab, Black rot, Cedar apple rust, Healthy
- Potato: Early blight, Late blight, Healthy
- Tomato: Bacterial spot, Early blight, Late blight, Leaf mold, Septoria leaf spot, Spider mites, Target spot, Yellow leaf curl virus, Mosaic virus, Healthy
- Corn: Cercospora leaf spot, Common rust, Northern leaf blight, Healthy
- And many more...

## How It Works

1. **Image Upload**: User uploads crop leaf image
2. **Quality Check**: Image validator ensures good quality
3. **ML Inference**: 
   - Image preprocessed to 224x224 pixels
   - Normalized and fed to EfficientNetB4 model
   - Model predicts disease with confidence score
4. **Result Parsing**: 
   - Extracts crop name and disease name
   - Calculates confidence percentage
   - Identifies if plant is healthy
5. **Recommendations**: Treatment recommendations generated based on disease

## Benefits

✅ **Accurate**: 97.66% accuracy vs unreliable API results
✅ **Fast**: Local inference, no API latency
✅ **Offline**: Works without internet (after model download)
✅ **Cost-effective**: No API usage fees
✅ **Comprehensive**: 38 disease classes across 14 crops
✅ **Reliable**: Consistent results, no API rate limits

## Deployment Notes

### Render Deployment:
- Model downloads automatically during build
- If download fails, system falls back to Plant.id API
- TensorFlow adds ~200MB to deployment size
- Ensure sufficient memory allocation (recommend 512MB+)

### Local Development:
```bash
# Install dependencies
pip install -r requirements.txt

# Download model
python download_model.py

# Run application
python run.py
```

## Testing

Upload various crop leaf images to test:
- Healthy leaves should be identified as "Healthy"
- Diseased leaves should show specific disease name
- Confidence scores should be displayed
- Treatment recommendations should be relevant

## Troubleshooting

**If ML detection fails:**
- System automatically falls back to Plant.id API
- Check logs for error messages
- Verify model file exists in `models/` directory
- Ensure TensorFlow is installed correctly

**If model download fails:**
- Build continues without error
- System uses API fallback
- Can manually download model later

## Future Improvements

- [ ] Add more crop species
- [ ] Fine-tune model on local crop varieties
- [ ] Implement model quantization for smaller size
- [ ] Add batch prediction support
- [ ] Cache predictions for similar images

## References

- PlantVillage Dataset: https://huggingface.co/datasets/mohanty/PlantVillage
- Pre-trained Model: https://huggingface.co/liriope/PlantDiseaseDetection
- EfficientNetB4 Architecture: https://arxiv.org/abs/1905.11946
