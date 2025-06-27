#!/usr/bin/env python3
"""Generate high-quality fruit images from system emojis for the Snake game."""

import os
from PIL import Image, ImageDraw, ImageFont
import platform

def create_emoji_images_alternative():
    """Create fruit images using a different approach that preserves emoji colors."""
    
    # Create assets directory if it doesn't exist
    assets_dir = "snake_game/assets/images"
    os.makedirs(assets_dir, exist_ok=True)
    
    # Since PIL doesn't handle color emojis well, let's create high-quality 
    # custom images that look like the emojis
    size = 64  # High resolution
    final_size = 20
    
    def create_emoji_style_apple():
        """Create an emoji-style apple."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = size // 2
        
        # Apple body - bright red like emoji
        # Create gradient effect
        for i in range(15):
            radius = 28 - i
            red_val = min(255, 240 - i * 5)
            draw.ellipse([center-radius, center+2-radius, center+radius, center+2+radius], 
                        fill=(red_val, 30, 30, 255))
        
        # Bright highlight like emoji
        draw.ellipse([center-15, center-12, center-5, center-2], fill=(255, 180, 180, 220))
        
        # Brown stem
        draw.rectangle([center-3, 8, center+3, 18], fill=(139, 69, 19, 255))
        
        # Green leaf - bright like emoji
        leaf_points = [(center+3, 12), (center+12, 8), (center+15, 15), (center+8, 20), (center+3, 18)]
        draw.polygon(leaf_points, fill=(50, 205, 50, 255))
        
        return img
    
    def create_emoji_style_pear():
        """Create an emoji-style pear."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = size // 2
        
        # Pear body - yellow-green like emoji
        # Bottom (wider part)
        for i in range(12):
            radius = 22 - i
            yellow_val = min(255, 240 - i * 8)
            green_val = min(255, 220 + i * 2)
            draw.ellipse([center-radius, center+10-radius, center+radius, center+10+radius], 
                        fill=(yellow_val, green_val, 100, 255))
        
        # Top (narrower part)
        for i in range(10):
            radius = 16 - i
            yellow_val = min(255, 230 - i * 5)
            green_val = min(255, 230 + i * 2)
            draw.ellipse([center-radius, center-8-radius, center+radius, center-8+radius], 
                        fill=(yellow_val, green_val, 120, 255))
        
        # Highlight
        draw.ellipse([center-12, center-5, center-4, center+3], fill=(255, 255, 200, 200))
        
        # Brown stem
        draw.rectangle([center-2, 6, center+2, 16], fill=(139, 69, 19, 255))
        
        return img
    
    def create_emoji_style_banana():
        """Create an emoji-style banana."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Banana shape - bright yellow like emoji
        points = [
            (10, 45), (15, 15), (25, 10), (40, 18), 
            (52, 40), (48, 54), (35, 58), (20, 50), (12, 47)
        ]
        
        # Main banana body
        draw.polygon(points, fill=(255, 255, 0, 255))
        
        # Inner lighter yellow
        inner_points = [
            (14, 43), (18, 18), (26, 14), (38, 22), 
            (48, 38), (44, 50), (33, 54), (22, 48), (16, 45)
        ]
        draw.polygon(inner_points, fill=(255, 255, 150, 255))
        
        # Brown tip like emoji
        draw.ellipse([12, 12, 22, 22], fill=(139, 69, 19, 255))
        
        # Banana ridges
        draw.line([(20, 20), (45, 45)], fill=(220, 220, 0, 255), width=3)
        draw.line([(22, 18), (47, 41)], fill=(220, 220, 0, 255), width=2)
        draw.line([(24, 22), (43, 49)], fill=(220, 220, 0, 255), width=2)
        
        return img
    
    def create_emoji_style_cherry():
        """Create emoji-style cherries."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Left cherry - bright red like emoji
        for i in range(8):
            radius = 14 - i
            red_val = min(255, 220 + i * 4)
            draw.ellipse([18-radius, 35-radius, 18+radius, 35+radius], 
                        fill=(red_val, 20, 60, 255))
        
        # Right cherry
        for i in range(8):
            radius = 14 - i
            red_val = min(255, 220 + i * 4)
            draw.ellipse([42-radius, 40-radius, 42+radius, 40+radius], 
                        fill=(red_val, 20, 60, 255))
        
        # Green stems like emoji
        draw.line([(18, 21), (30, 10)], fill=(50, 205, 50, 255), width=4)
        draw.line([(42, 26), (34, 10)], fill=(50, 205, 50, 255), width=4)
        
        # Bright highlights
        draw.ellipse([14, 31, 20, 37], fill=(255, 150, 180, 220))
        draw.ellipse([38, 36, 44, 42], fill=(255, 150, 180, 220))
        
        return img
    
    def create_emoji_style_orange():
        """Create an emoji-style orange."""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = size // 2
        
        # Orange body - bright orange like emoji
        for i in range(12):
            radius = 26 - i * 1.5
            orange_r = min(255, 255 - i * 3)
            orange_g = min(255, 165 + i * 5)
            draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                        fill=(int(orange_r), int(orange_g), 0, 255))
        
        # Orange texture - dimpled surface like emoji
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue
                x = center + i * 10
                y = center + j * 10
                if 10 <= x <= size-10 and 10 <= y <= size-10:
                    draw.ellipse([x-4, y-4, x+4, y+4], fill=(200, 120, 0, 180))
        
        # Bright highlight
        draw.ellipse([center-15, center-15, center-5, center-5], fill=(255, 220, 100, 200))
        
        # Green top like emoji
        draw.ellipse([center-8, 10, center+8, 20], fill=(50, 205, 50, 255))
        
        return img
    
    # Generate all emoji-style images
    fruits = {
        'apple': create_emoji_style_apple(),
        'pear': create_emoji_style_pear(),
        'banana': create_emoji_style_banana(),
        'cherry': create_emoji_style_cherry(),
        'orange': create_emoji_style_orange()
    }
    
    # Save images with high-quality downsampling
    for name, img in fruits.items():
        # Scale down with high-quality resampling for crisp final image
        final_img = img.resize((final_size, final_size), Image.LANCZOS)
        
        filepath = os.path.join(assets_dir, f"{name}.png")
        final_img.save(filepath, "PNG")
        print(f"✓ Created emoji-style {name}.png")
    
    print(f"\n🎨 Generated {len(fruits)} emoji-style fruit images!")
    print("Images have bright, vibrant colors like real emojis!")
    return True

if __name__ == "__main__":
    print("🍎 Generating emoji-style fruit images...")
    print("Creating vibrant, colorful images that match emoji appearance...\n")
    
    success = create_emoji_images_alternative()
    
    if success:
        print("\n✅ High-quality emoji-style fruit images ready!")
        print("Images are 20x20 pixels with full color and emoji-like appearance.")
    else:
        print("\n❌ Failed to generate fruit images.")
