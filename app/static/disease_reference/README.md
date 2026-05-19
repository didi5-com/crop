# Disease Reference Images

This folder contains reference images for crop diseases to help with visual identification.

## Folder Structure

```
disease_reference/
├── cassava/
│   ├── mosaic_disease.jpg
│   ├── bacterial_blight.jpg
│   ├── brown_streak.jpg
│   ├── green_mite.jpg
│   └── healthy.jpg
├── tomato/
│   ├── early_blight.jpg
│   ├── late_blight.jpg
│   ├── bacterial_spot.jpg
│   ├── leaf_mold.jpg
│   └── healthy.jpg
├── potato/
│   ├── early_blight.jpg
│   ├── late_blight.jpg
│   └── healthy.jpg
├── maize/
│   ├── common_rust.jpg
│   ├── northern_leaf_blight.jpg
│   └── healthy.jpg
└── pepper/
    ├── bacterial_spot.jpg
    └── healthy.jpg
```

## How to Add Reference Images

1. Download disease images from PlantVillage dataset or other sources
2. Rename images to match the disease names (e.g., `mosaic_disease.jpg`)
3. Place images in the appropriate crop folder
4. Images will be displayed in the detection results for visual comparison

## Image Sources

- PlantVillage Dataset: https://github.com/spMohanty/PlantVillage-Dataset
- Hugging Face PlantVillage: https://huggingface.co/datasets/mohanty/PlantVillage
- Agricultural Extension Services
- Research Publications

## Image Requirements

- Format: JPG or PNG
- Size: 500x500 pixels minimum
- Quality: Clear, well-lit images showing disease symptoms
- Focus: Close-up of affected plant parts (leaves, stems, fruits)
