"""
Comprehensive Crop Disease Database
Contains detailed information about diseases for major edible crops
"""

CROP_DISEASES = {
    # CASSAVA DISEASES
    'cassava': {
        'mosaic_disease': {
            'name': 'Cassava Mosaic Disease (CMD)',
            'symptoms': 'Yellow and white patches on leaves | Leaf distortion and curling | Stunted plant growth | Reduced tuber size',
            'causes': 'Caused by Cassava Mosaic Virus transmitted by whiteflies | Spreads through infected cuttings',
            'treatment': 'Remove and destroy infected plants | Use virus-free planting material | Control whitefly population with neem oil | Apply insecticides (imidacloprid)',
            'prevention': 'Plant resistant varieties | Use certified disease-free cuttings | Remove infected plants immediately | Control whitefly vectors',
            'fertilizers': 'NPK 15-15-15 | Organic compost | Potassium sulfate for disease resistance',
            'severity': 'high',
            'reference_image': 'cassava_mosaic.jpg'
        },
        'bacterial_blight': {
            'name': 'Cassava Bacterial Blight (CBB)',
            'symptoms': 'Water-soaked angular leaf spots | Wilting of leaves | Stem cankers | Gum exudation from stems',
            'causes': 'Caused by Xanthomonas axonopodis bacteria | Spreads through rain splash and infected tools',
            'treatment': 'Remove infected plants | Apply copper-based bactericides | Improve field drainage | Use clean cutting tools',
            'prevention': 'Use disease-free planting material | Avoid planting in waterlogged areas | Practice crop rotation | Disinfect tools between plants',
            'fertilizers': 'Balanced NPK 10-10-10 | Calcium supplements | Avoid excess nitrogen',
            'severity': 'high',
            'reference_image': 'cassava_bacterial_blight.jpg'
        },
        'brown_streak': {
            'name': 'Cassava Brown Streak Disease (CBSD)',
            'symptoms': 'Brown streaks on stems | Yellow chlorotic blotches on leaves | Brown necrotic lesions in tubers | Root rot',
            'causes': 'Caused by Cassava Brown Streak Virus transmitted by whiteflies',
            'treatment': 'No cure available | Remove infected plants | Control whitefly population | Harvest early if infected',
            'prevention': 'Plant resistant varieties | Use virus-free cuttings | Control whiteflies | Remove infected plants',
            'fertilizers': 'NPK 15-15-15 | Potassium-rich fertilizer | Organic matter',
            'severity': 'very_high',
            'reference_image': 'cassava_brown_streak.jpg'
        },
        'green_mite': {
            'name': 'Cassava Green Mite Damage',
            'symptoms': 'Yellow spots on leaves | Leaf curling and distortion | Stunted growth | Leaf drop in severe cases',
            'causes': 'Infestation by cassava green mites (Mononychellus tanajoa) | Thrives in hot dry conditions',
            'treatment': 'Apply acaricides (abamectin) | Use neem oil spray | Introduce natural predators | Increase humidity',
            'prevention': 'Regular monitoring | Maintain field hygiene | Plant resistant varieties | Biological control with predatory mites',
            'fertilizers': 'Balanced NPK | Foliar spray with micronutrients | Organic compost',
            'severity': 'medium',
            'reference_image': 'cassava_green_mite.jpg'
        },
        'healthy': {
            'name': 'Healthy Cassava',
            'symptoms': 'Dark green healthy leaves | Normal growth pattern | No spots or discoloration | Vigorous plant',
            'causes': 'N/A - Plant is healthy',
            'treatment': 'No treatment needed | Continue good agricultural practices',
            'prevention': 'Maintain proper spacing | Regular weeding | Adequate watering | Balanced fertilization',
            'fertilizers': 'NPK 15-15-15 at planting | Organic compost | Potassium for tuber development',
            'severity': 'none',
            'reference_image': 'cassava_healthy.jpg'
        }
    },
    
    # TOMATO DISEASES
    'tomato': {
        'early_blight': {
            'name': 'Tomato Early Blight',
            'symptoms': 'Dark brown spots with concentric rings (target-like) on older leaves | Yellowing around spots | Leaf drop | Stem lesions',
            'causes': 'Fungal infection by Alternaria solani | Favored by warm humid weather | Spreads through water splash',
            'treatment': 'Remove infected leaves | Apply fungicide (chlorothalonil, mancozeb) | Improve air circulation | Mulch to prevent soil splash',
            'prevention': 'Crop rotation (3-4 years) | Proper plant spacing | Drip irrigation | Remove plant debris | Use resistant varieties',
            'fertilizers': 'Balanced NPK 10-10-10 | Calcium supplements | Avoid excess nitrogen | Potassium for disease resistance',
            'severity': 'medium',
            'reference_image': 'tomato_early_blight.jpg'
        },
        'late_blight': {
            'name': 'Tomato Late Blight',
            'symptoms': 'Water-soaked spots on leaves | White mold on leaf undersides | Rapid plant death | Brown lesions on fruits',
            'causes': 'Phytophthora infestans fungus | Spreads rapidly in cool wet conditions | Can destroy entire crop quickly',
            'treatment': 'Remove infected plants immediately | Apply fungicide (copper, chlorothalonil) | Improve drainage | Increase spacing',
            'prevention': 'Plant resistant varieties | Avoid overhead watering | Good air circulation | Remove volunteer plants | Destroy infected debris',
            'fertilizers': 'Potassium-rich fertilizer | Copper fungicide | Reduce nitrogen | Calcium supplements',
            'severity': 'very_high',
            'reference_image': 'tomato_late_blight.jpg'
        },
        'bacterial_spot': {
            'name': 'Tomato Bacterial Spot',
            'symptoms': 'Small dark spots on leaves | Yellow halos around spots | Fruit lesions | Defoliation in severe cases',
            'causes': 'Xanthomonas bacteria | Spreads through water, tools, and hands | Thrives in warm wet conditions',
            'treatment': 'Apply copper-based bactericides | Remove infected plants | Avoid working with wet plants | Improve air flow',
            'prevention': 'Use disease-free seeds | Crop rotation | Drip irrigation | Disinfect tools | Avoid overhead watering',
            'fertilizers': 'Balanced NPK | Calcium for cell wall strength | Avoid excess nitrogen',
            'severity': 'medium',
            'reference_image': 'tomato_bacterial_spot.jpg'
        },
        'leaf_mold': {
            'name': 'Tomato Leaf Mold',
            'symptoms': 'Yellow spots on upper leaf surface | Olive-green to brown mold on undersides | Leaf curling | Defoliation',
            'causes': 'Passalora fulva fungus | Thrives in high humidity (above 85%) | Common in greenhouses',
            'treatment': 'Reduce humidity | Improve ventilation | Apply fungicide (chlorothalonil) | Remove infected leaves',
            'prevention': 'Maintain humidity below 85% | Good air circulation | Resistant varieties | Proper spacing',
            'fertilizers': 'Balanced NPK | Potassium for disease resistance | Avoid excess nitrogen',
            'severity': 'medium',
            'reference_image': 'tomato_leaf_mold.jpg'
        },
        'healthy': {
            'name': 'Healthy Tomato',
            'symptoms': 'Dark green leaves | Vigorous growth | No spots or discoloration | Good fruit set',
            'causes': 'N/A - Plant is healthy',
            'treatment': 'No treatment needed | Continue current care practices',
            'prevention': 'Proper watering | Balanced fertilization | Good air circulation | Regular monitoring',
            'fertilizers': 'NPK 5-10-10 for fruiting | Calcium for blossom end rot prevention | Magnesium supplements',
            'severity': 'none',
            'reference_image': 'tomato_healthy.jpg'
        }
    },
    
    # POTATO DISEASES
    'potato': {
        'early_blight': {
            'name': 'Potato Early Blight',
            'symptoms': 'Dark brown spots with concentric rings on leaves | Lower leaves affected first | Tuber lesions | Reduced yield',
            'causes': 'Alternaria solani fungus | Warm humid conditions | Stressed plants more susceptible',
            'treatment': 'Apply fungicide (mancozeb, chlorothalonil) | Remove infected foliage | Improve plant nutrition | Mulch soil',
            'prevention': 'Crop rotation | Certified seed potatoes | Proper spacing | Balanced fertilization | Remove plant debris',
            'fertilizers': 'NPK 10-10-20 | Potassium for disease resistance | Avoid excess nitrogen | Calcium supplements',
            'severity': 'medium',
            'reference_image': 'potato_early_blight.jpg'
        },
        'late_blight': {
            'name': 'Potato Late Blight',
            'symptoms': 'Water-soaked lesions on leaves | White mold on undersides | Rapid plant collapse | Tuber rot',
            'causes': 'Phytophthora infestans | Cool wet weather | Can destroy crop in days | Spreads via wind and water',
            'treatment': 'Destroy infected plants | Apply fungicide immediately | Hill soil around plants | Harvest early if needed',
            'prevention': 'Plant certified seed | Resistant varieties | Avoid overhead irrigation | Good drainage | Remove cull piles',
            'fertilizers': 'Potassium sulfate | Copper fungicide | Balanced NPK | Avoid excess nitrogen',
            'severity': 'very_high',
            'reference_image': 'potato_late_blight.jpg'
        },
        'healthy': {
            'name': 'Healthy Potato',
            'symptoms': 'Dark green foliage | Vigorous growth | No lesions or spots | Good tuber development',
            'causes': 'N/A - Plant is healthy',
            'treatment': 'No treatment needed | Maintain good practices',
            'prevention': 'Proper hilling | Adequate watering | Balanced nutrition | Crop rotation',
            'fertilizers': 'NPK 10-10-20 | Potassium for tuber quality | Organic compost | Sulfur',
            'severity': 'none',
            'reference_image': 'potato_healthy.jpg'
        }
    },
    
    # MAIZE/CORN DISEASES
    'maize': {
        'common_rust': {
            'name': 'Maize Common Rust',
            'symptoms': 'Orange-red pustules on leaves | Pustules on both leaf surfaces | Reduced photosynthesis | Premature leaf death',
            'causes': 'Puccinia sorghi fungus | Spreads via wind | Favored by cool humid weather',
            'treatment': 'Apply fungicide (azoxystrobin) | Remove infected leaves | Plant resistant hybrids',
            'prevention': 'Resistant varieties | Proper spacing | Balanced fertilization | Early planting',
            'fertilizers': 'NPK 15-15-15 | Zinc supplements | Potassium for disease resistance',
            'severity': 'medium',
            'reference_image': 'maize_common_rust.jpg'
        },
        'northern_leaf_blight': {
            'name': 'Northern Corn Leaf Blight',
            'symptoms': 'Long gray-green lesions on leaves | Lesions turn tan with age | Reduced photosynthesis | Yield loss',
            'causes': 'Exserohilum turcicum fungus | Moderate temperatures | High humidity | Spreads via wind',
            'treatment': 'Apply fungicide | Remove crop residue | Use resistant hybrids | Crop rotation',
            'prevention': 'Resistant varieties | Tillage to bury residue | Crop rotation | Balanced nutrition',
            'fertilizers': 'Balanced NPK | Potassium for resistance | Avoid excess nitrogen',
            'severity': 'medium',
            'reference_image': 'maize_northern_blight.jpg'
        },
        'healthy': {
            'name': 'Healthy Maize',
            'symptoms': 'Dark green leaves | Vigorous growth | No lesions | Good ear development',
            'causes': 'N/A - Plant is healthy',
            'treatment': 'No treatment needed | Continue good practices',
            'prevention': 'Adequate spacing | Proper fertilization | Weed control | Adequate water',
            'fertilizers': 'NPK 15-15-15 | Nitrogen for vegetative growth | Phosphorus for root development',
            'severity': 'none',
            'reference_image': 'maize_healthy.jpg'
        }
    },
    
    # PEPPER DISEASES
    'pepper': {
        'bacterial_spot': {
            'name': 'Pepper Bacterial Spot',
            'symptoms': 'Small dark spots on leaves | Yellow halos | Fruit lesions | Defoliation',
            'causes': 'Xanthomonas bacteria | Warm wet conditions | Spreads through water and tools',
            'treatment': 'Copper-based bactericides | Remove infected plants | Avoid overhead watering | Improve drainage',
            'prevention': 'Disease-free seeds | Crop rotation | Drip irrigation | Disinfect tools | Resistant varieties',
            'fertilizers': 'Balanced NPK 10-10-10 | Calcium for cell strength | Avoid excess nitrogen',
            'severity': 'medium',
            'reference_image': 'pepper_bacterial_spot.jpg'
        },
        'healthy': {
            'name': 'Healthy Pepper',
            'symptoms': 'Dark green leaves | Vigorous growth | Good fruit set | No spots or lesions',
            'causes': 'N/A - Plant is healthy',
            'treatment': 'No treatment needed | Maintain current practices',
            'prevention': 'Proper watering | Balanced fertilization | Good air circulation | Pest control',
            'fertilizers': 'NPK 5-10-10 for fruiting | Calcium and magnesium | Micronutrients',
            'severity': 'none',
            'reference_image': 'pepper_healthy.jpg'
        }
    }
}


def get_disease_info(crop_name, disease_name):
    """Get detailed information about a specific disease"""
    crop_name = crop_name.lower().replace(' ', '_')
    disease_name = disease_name.lower().replace(' ', '_')
    
    if crop_name in CROP_DISEASES:
        if disease_name in CROP_DISEASES[crop_name]:
            return CROP_DISEASES[crop_name][disease_name]
    
    return None


def get_all_crops():
    """Get list of all supported crops"""
    return list(CROP_DISEASES.keys())


def get_crop_diseases(crop_name):
    """Get all diseases for a specific crop"""
    crop_name = crop_name.lower().replace(' ', '_')
    if crop_name in CROP_DISEASES:
        return CROP_DISEASES[crop_name]
    return {}
