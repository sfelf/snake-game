#!/usr/bin/env python3
"""Download the specific coiled snake image from pngaaa.com."""

import os
import requests
from PIL import Image
import io

def download_specific_snake_image():
    """Download the specific coiled snake image from the provided URL."""
    
    # Create assets directory if it doesn't exist
    assets_dir = "snake_game/assets/images"
    os.makedirs(assets_dir, exist_ok=True)
    
    # The new snake image URL
    image_url = "https://www.pngaaa.com/api-download/340536"
    
    print("🐍 Downloading new coiled snake image...")
    print(f"Source: {image_url}")
    
    try:
        # Download the image
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Load the image with PIL
        img = Image.open(io.BytesIO(response.content))
        
        # Convert to RGBA if needed (for transparency support)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create the large version for splash screen (128x128 to match current size)
        large_img = img.resize((128, 128), Image.LANCZOS)
        large_path = os.path.join(assets_dir, "perfect_coiled_snake_large.png")
        large_img.save(large_path, "PNG")
        
        # Also create a medium version (96x96) if needed
        medium_img = img.resize((96, 96), Image.LANCZOS)
        medium_path = os.path.join(assets_dir, "perfect_coiled_snake_medium.png")
        medium_img.save(medium_path, "PNG")
        
        print("✓ Downloaded and processed new coiled snake image:")
        print(f"  - Large version (128x128): perfect_coiled_snake_large.png")
        print(f"  - Medium version (96x96): perfect_coiled_snake_medium.png")
        print("🎉 New perfect coiled snake ready for splash screen!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to download snake image: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Downloading the new perfect coiled snake image...")
    print("This snake should show an even better coiled pose!\n")
    
    success = download_specific_snake_image()
    
    if success:
        print("\n✅ New perfect coiled snake image downloaded successfully!")
        print("Ready to use in the splash screen!")
    else:
        print("\n❌ Failed to download the snake image.")
        print("Please check your internet connection and try again.")
