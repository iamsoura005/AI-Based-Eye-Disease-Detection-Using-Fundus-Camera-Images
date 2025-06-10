import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Create directory if it doesn't exist
static_dir = os.path.join(os.path.dirname(__file__), "static", "images")
os.makedirs(static_dir, exist_ok=True)

def generate_sample_fundus_image(width=224, height=224):
    """Generate a simple circular fundus image"""
    # Create a black background
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw a circular fundus
    center = (width // 2, height // 2)
    radius = min(width, height) // 2 - 10
    
    # Create a reddish fundus
    cv2.circle(image, center, radius, (20, 20, 180), -1)
    
    # Add some blood vessels (lines)
    for i in range(8):
        angle = i * (2 * np.pi / 8)
        end_x = int(center[0] + 0.8 * radius * np.cos(angle))
        end_y = int(center[1] + 0.8 * radius * np.sin(angle))
        thickness = np.random.randint(1, 3)
        cv2.line(image, center, (end_x, end_y), (10, 10, 120), thickness)
    
    # Add optic disc (bright spot)
    disc_center = (center[0] - radius // 3, center[1])
    cv2.circle(image, disc_center, radius // 6, (200, 200, 250), -1)
    
    # Add some random spots
    for _ in range(5):
        spot_x = np.random.randint(center[0] - radius // 2, center[0] + radius // 2)
        spot_y = np.random.randint(center[1] - radius // 2, center[1] + radius // 2)
        spot_radius = np.random.randint(2, 6)
        cv2.circle(image, (spot_x, spot_y), spot_radius, (20, 20, 220), -1)
    
    # Add a dark border
    cv2.circle(image, center, radius, (0, 0, 0), 2)
    
    return image

def generate_heatmap(image, center_offset=(0, 0)):
    """Generate a heatmap overlay for the image"""
    height, width = image.shape[:2]
    heatmap = np.zeros((height, width), dtype=np.float32)
    
    center_x = width // 2 + center_offset[0]
    center_y = height // 2 + center_offset[1]
    
    # Create a circular heatmap
    for y in range(height):
        for x in range(width):
            # Calculate distance from center
            dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            # Normalize by radius
            norm_dist = dist / (min(width, height) // 3)
            # Apply heat based on distance (closer = hotter)
            heatmap[y, x] = max(0, 1 - norm_dist)
    
    # Normalize heatmap
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Apply colormap
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Blend with original image
    alpha = 0.4
    blended = cv2.addWeighted(image, 1 - alpha, heatmap_colored, alpha, 0)
    
    return blended, heatmap_colored

def create_sample_images():
    """Create sample fundus images and heatmaps"""
    # Generate 3 different sample images
    for i in range(3):
        # Create fundus image
        fundus = generate_sample_fundus_image(400, 400)
        
        # Create heatmap with slight offset for variety
        offset_x = np.random.randint(-50, 50)
        offset_y = np.random.randint(-50, 50)
        blended, heatmap = generate_heatmap(fundus, (offset_x, offset_y))
        
        # Save original fundus image
        fundus_path = os.path.join(static_dir, f"sample_fundus_{i+1}.jpg")
        cv2.imwrite(fundus_path, fundus)
        
        # Save heatmap
        heatmap_path = os.path.join(static_dir, f"sample_heatmap_{i+1}.jpg")
        cv2.imwrite(heatmap_path, heatmap)
        
        # Create side-by-side comparison
        plt.figure(figsize=(10, 5))
        
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(fundus, cv2.COLOR_BGR2RGB))
        plt.title('Original Image')
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.imshow(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
        plt.title('Grad-CAM Visualization')
        plt.axis('off')
        
        # Save comparison
        comparison_path = os.path.join(static_dir, f"sample_comparison_{i+1}.jpg")
        plt.savefig(comparison_path, bbox_inches='tight')
        plt.close()
        
        print(f"Generated sample images {i+1}/3")

if __name__ == "__main__":
    create_sample_images()
    print(f"Sample images saved to {static_dir}") 