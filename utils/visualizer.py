import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import os

def crop_center(img, crop_size=100):
    """Crops a square region from the center of an image."""
    h, w = img.shape[:2]
    start_x = w // 2 - crop_size // 2
    start_y = h // 2 - crop_size // 2
    return img[start_y:start_y+crop_size, start_x:start_x+crop_size]

def show_comparison(results_dict, title="Super Resolution Comparison", crop=False):
    """
    Display multiple images side by side for comparison.
    results_dict: dict of {label: image}
    """
    num_images = len(results_dict)
    plt.figure(figsize=(4 * num_images, 4))
    
    for i, (label, img) in enumerate(results_dict.items()):
        plt.subplot(1, num_images, i + 1)
        display_img = crop_center(img) if crop else img
        plt.imshow(cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB))
        plt.title(label)
        plt.axis("off")

    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.show()

def benchmark_model(sr_model, image, runs=10):
    """
    Runs super resolution multiple times and returns average inference time.
    """
    times = []
    for _ in range(runs):
        start = time.time()
        _ = sr_model.upsample(image)
        end = time.time()
        times.append(end - start)
    return np.mean(times)
