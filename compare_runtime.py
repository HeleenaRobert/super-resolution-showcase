import os
import cv2
import matplotlib.pyplot as plt
from utils.superres_utils import load_superres_model
from utils.visualizer import benchmark_model

# Path to input image (low-res version)
INPUT_IMAGE_PATH = "input/kitten-200.png"

# Load and validate input
image = cv2.imread(INPUT_IMAGE_PATH)
if image is None:
    raise FileNotFoundError(f"Input image not found at {INPUT_IMAGE_PATH}")

# Model list
model_names = ["fsrcnn", "espcn", "lapsrn", "edsr"]
timings = {}

# Benchmark each model
print("Benchmarking model speeds...")
for model_name in model_names:
    print(f"Running {model_name.upper()}...")
    sr = load_superres_model(model_name)
    avg_time = benchmark_model(sr, image, runs=10)
    timings[model_name.upper()] = avg_time

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(timings.keys(), timings.values(), color='orchid')
plt.title("Average Inference Time (10 runs)")
plt.ylabel("Time (seconds)")
plt.xlabel("Model")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("output/model_runtime_comparison.png")  # Save the plot as an image
plt.show()
