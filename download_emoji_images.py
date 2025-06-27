#!/usr/bin/env python3
"""Download high-quality emoji images from online sources for the Snake game."""

import os
import requests
from PIL import Image
import io

def download_twemoji_images():
    """Download high-quality emoji images from Twitter's Twemoji library."""
    
    # Create assets directory if it doesn't exist
    assets_dir = "snake_game/assets/images"
    os.makedirs(assets_dir, exist_ok=True)
    
    # Twemoji SVG URLs (these are high-quality vector images)
    # Twitter's Twemoji is open source and free to use
    twemoji_base_url = "https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/"
    
    # Unicode codepoints for our fruit emojis
    fruit_emojis = {
        'apple': '1f34e',      # 🍎
        'pear': '1f350',       # 🍐
        'banana': '1f34c',     # 🍌
        'cherry': '1f352',     # 🍒
        'orange': '1f34a'      # 🍊
    }
    
    print("🍎 Downloading high-quality emoji images from Twemoji...")
    
    downloaded_count = 0
    
    for fruit_name, unicode_code in fruit_emojis.items():
        try:
            # Download SVG from Twemoji
            svg_url = f"{twemoji_base_url}{unicode_code}.svg"
            print(f"Downloading {fruit_name} emoji from {svg_url}")
            
            response = requests.get(svg_url, timeout=10)
            response.raise_for_status()
            
            # Save SVG temporarily
            svg_path = os.path.join(assets_dir, f"{fruit_name}.svg")
            with open(svg_path, 'wb') as f:
                f.write(response.content)
            
            # Convert SVG to high-quality PNG using cairosvg if available
            try:
                import cairosvg
                
                # Convert to high-res PNG (64x64 for crisp quality)
                png_data = cairosvg.svg2png(
                    url=svg_path,
                    output_width=64,
                    output_height=64
                )
                
                # Load with PIL and resize to game size with high quality
                img = Image.open(io.BytesIO(png_data))
                final_img = img.resize((20, 20), Image.LANCZOS)
                
                # Save final image
                png_path = os.path.join(assets_dir, f"{fruit_name}.png")
                final_img.save(png_path, "PNG")
                
                # Clean up SVG
                os.remove(svg_path)
                
                print(f"✓ Created high-quality {fruit_name}.png from Twemoji")
                downloaded_count += 1
                
            except ImportError:
                print(f"⚠️  cairosvg not available, keeping SVG for {fruit_name}")
                # Keep the SVG file for manual conversion
                
        except Exception as e:
            print(f"❌ Failed to download {fruit_name}: {e}")
    
    if downloaded_count > 0:
        print(f"\n🎉 Successfully downloaded {downloaded_count} high-quality emoji images!")
        return True
    else:
        print("\n⚠️  Could not download Twemoji images, trying alternative sources...")
        return download_alternative_emoji_images()

def download_alternative_emoji_images():
    """Try alternative sources for high-quality emoji images."""
    
    assets_dir = "snake_game/assets/images"
    
    # Alternative: Use Noto Emoji from Google
    noto_base_url = "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/"
    
    # Unicode filenames for Noto Emoji
    fruit_emojis = {
        'apple': 'emoji_u1f34e',      # 🍎
        'pear': 'emoji_u1f350',       # 🍐
        'banana': 'emoji_u1f34c',     # 🍌
        'cherry': 'emoji_u1f352',     # 🍒
        'orange': 'emoji_u1f34a'      # 🍊
    }
    
    print("Trying Google Noto Emoji images...")
    
    downloaded_count = 0
    
    for fruit_name, filename in fruit_emojis.items():
        try:
            # Download PNG from Noto Emoji (128x128 high quality)
            png_url = f"{noto_base_url}{filename}.png"
            print(f"Downloading {fruit_name} from Noto Emoji...")
            
            response = requests.get(png_url, timeout=10)
            response.raise_for_status()
            
            # Load and resize with high quality
            img = Image.open(io.BytesIO(response.content))
            final_img = img.resize((20, 20), Image.LANCZOS)
            
            # Save final image
            png_path = os.path.join(assets_dir, f"{fruit_name}.png")
            final_img.save(png_path, "PNG")
            
            print(f"✓ Created high-quality {fruit_name}.png from Noto Emoji")
            downloaded_count += 1
            
        except Exception as e:
            print(f"❌ Failed to download {fruit_name} from Noto: {e}")
    
    if downloaded_count > 0:
        print(f"\n🎉 Successfully downloaded {downloaded_count} high-quality emoji images from Noto!")
        return True
    else:
        print("\n❌ Could not download from any online source")
        return False

def install_cairosvg():
    """Install cairosvg for SVG to PNG conversion."""
    try:
        import subprocess
        import sys
        
        print("Installing cairosvg for high-quality SVG conversion...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cairosvg"])
        print("✓ cairosvg installed successfully")
        return True
    except Exception as e:
        print(f"Could not install cairosvg: {e}")
        return False

if __name__ == "__main__":
    print("🍎 Downloading high-quality emoji images for Snake Game...")
    print("Using professional emoji libraries for maximum quality...\n")
    
    # Try to install cairosvg first for SVG conversion
    try:
        import cairosvg
        print("✓ cairosvg is available for SVG conversion")
    except ImportError:
        print("Installing cairosvg for better quality...")
        install_cairosvg()
    
    success = download_twemoji_images()
    
    if success:
        print("\n✅ High-quality emoji images ready for the game!")
        print("Images are now the same quality as system emojis!")
    else:
        print("\n❌ Failed to download high-quality emoji images.")
        print("You may need to check your internet connection or try again later.")
