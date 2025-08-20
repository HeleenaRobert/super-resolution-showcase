import os
import cv2
from utils.superres_utils import load_superres_model, upscale_image
from utils.visualizer import show_comparison

# Define your test image pair
LOW_RES_IMAGE = "input/bike-200.png"
GROUND_TRUTH_IMAGE = "ground_truth/bike-800.png"

# Load images
low_res = cv2.imread(LOW_RES_IMAGE)
gt = cv2.imread(GROUND_TRUTH_IMAGE)

if low_res is None or gt is None:
    raise FileNotFoundError("One of the images could not be loaded.")

# Resize low-res back to high-res dimensions using bicubic as baseline
results = {
    "Ground Truth": gt,
    "Bicubic": cv2.resize(low_res, (gt.shape[1], gt.shape[0]), interpolation=cv2.INTER_CUBIC)
}

# Run all models
model_names = ["fsrcnn", "espcn", "lapsrn", "edsr"]
for model_name in model_names:
    print(f"Running {model_name.upper()}...")
    sr = load_superres_model(model_name)
    output = upscale_image(sr, low_res)
    results[model_name.upper()] = output

# Show cropped comparison of all
show_comparison(results, title="Super Resolution vs Ground Truth", crop=False)

# Save output images
os.makedirs("output", exist_ok=True)
for name, img in results.items():
    cv2.imwrite(f"output/{name}_quality.jpg", img)
