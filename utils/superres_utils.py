import cv2
import os

# Supported model names mapped to their .pb files
MODEL_PATHS = {
    "fsrcnn": "models/fsrcnn/FSRCNN_x4.pb",
    "espcn": "models/espcn/ESPCN_x4.pb",
    "lapsrn": "models/lapsrn/LapSRN_x4.pb",
    "edsr": "models/edsr/EDSR_x4.pb"
}

def load_superres_model(model_name):
    """Loads a super-resolution model by name."""
    model_path = MODEL_PATHS.get(model_name.lower())
    if not model_path or not os.path.exists(model_path):
        raise FileNotFoundError(f"Model '{model_name}' not found at {model_path}")
    
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel(model_name.lower(), 4)
    return sr

def upscale_image(sr_model, image):
    """Applies super resolution to an image using the given model."""
    return sr_model.upsample(image)
