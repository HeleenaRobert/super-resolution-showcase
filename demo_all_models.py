import os
import cv2
from utils.superres_utils import load_superres_model, upscale_image
from utils.visualizer import show_comparison

# Path to input image (replace with your own)
INPUT_IMAGE_PATH = "input/car.jpg"

# Load input image
image = cv2.imread(INPUT_IMAGE_PATH)
if image is None:
    raise FileNotFoundError(f"Input image not found at {INPUT_IMAGE_PATH}")

# Resize image down to simulate low resolution
low_res = cv2.resize(image, (image.shape[1] // 4, image.shape[0] // 4), interpolation=cv2.INTER_CUBIC)

# Initialize results dictionary with bicubic baseline
results = {"Bicubic": cv2.resize(low_res, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_CUBIC)}

# List of model names to apply
model_names = ["fsrcnn", "espcn", "lapsrn", "edsr"]

# Run each model
for model_name in model_names:
    print(f"Applying {model_name.upper()}...")
    sr_model = load_superres_model(model_name)
    upscaled = upscale_image(sr_model, low_res)
    results[model_name.upper()] = upscaled

# Display results
show_comparison(results, title="Super Resolution Results", crop=False)

# Save output images
os.makedirs("output", exist_ok=True)
for name, img in results.items():
    input_name = os.path.splitext(os.path.basename(INPUT_IMAGE_PATH))[0]
    cv2.imwrite(f"output/{input_name}_{name}_output.jpg", img)

