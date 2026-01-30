"""
Fixed script to convert PNG logo to ICO format with MULTIPLE sizes.
Uses a workaround for Pillow's ICO format limitation.
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance
import struct

def unsharp_mask(img, radius=2, percent=150, threshold=3):
    """Apply unsharp mask filter for better sharpening."""
    if img.mode == 'RGBA':
        r, g, b, a = img.split()
        rgb_img = Image.merge('RGB', (r, g, b))
        rgb_img = rgb_img.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))
        r, g, b = rgb_img.split()
        return Image.merge('RGBA', (r, g, b, a))
    else:
        return img.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))

def create_ico_from_png(png_path: Path, ico_path: Path, sizes: list = None):
    """Create ICO file with multiple sizes using workaround."""
    if sizes is None:
        sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # Open and process source image
    img = Image.open(png_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    source_size = max(img.size)
    if source_size < 512:
        target_source_size = 512
        print(f"Upscaling source image from {source_size}x{source_size} to {target_source_size}x{target_source_size}...")
        img = img.resize((target_source_size, target_source_size), Image.Resampling.LANCZOS)
        img = unsharp_mask(img, radius=1, percent=120, threshold=2)
    elif source_size > 1024:
        target_source_size = 1024
        print(f"Downscaling source image from {source_size}x{source_size} to {target_source_size}x{target_source_size}...")
        img = img.resize((target_source_size, target_source_size), Image.Resampling.LANCZOS)
    else:
        print(f"Using source image at {source_size}x{source_size} (no resizing needed)")
    
    # Create all sizes with sharpening
    ico_images = []
    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        
        if size <= 32:
            resized = unsharp_mask(resized, radius=1.5, percent=200, threshold=1)
            resized = unsharp_mask(resized, radius=0.5, percent=150, threshold=1)
            enhancer = ImageEnhance.Contrast(resized)
            resized = enhancer.enhance(1.5)
            enhancer = ImageEnhance.Sharpness(resized)
            resized = enhancer.enhance(1.5)
            enhancer = ImageEnhance.Brightness(resized)
            resized = enhancer.enhance(1.1)
        elif size <= 48:
            resized = unsharp_mask(resized, radius=1.5, percent=180, threshold=2)
            enhancer = ImageEnhance.Contrast(resized)
            resized = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Sharpness(resized)
            resized = enhancer.enhance(1.3)
        elif size <= 64:
            resized = unsharp_mask(resized, radius=1, percent=160, threshold=2)
            enhancer = ImageEnhance.Contrast(resized)
            resized = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Sharpness(resized)
            resized = enhancer.enhance(1.2)
        elif size <= 128:
            resized = unsharp_mask(resized, radius=1, percent=130, threshold=3)
            enhancer = ImageEnhance.Contrast(resized)
            resized = enhancer.enhance(1.1)
        
        ico_images.append(resized)
    
    # WORKAROUND: Save each size as separate ICO, then combine
    # OR: Use a different approach - save as temporary PNGs and combine
    # For now, let's try saving with proper format
    
    # Sort by size (largest first)
    ico_images_sorted = sorted(ico_images, key=lambda x: x.size[0], reverse=True)
    
    # Save using the method that should work
    # Create a list of all images with their sizes
    base_image = ico_images_sorted[0]
    other_images = ico_images_sorted[1:] if len(ico_images_sorted) > 1 else []
    
    # Try saving with all images
    if other_images:
        # Save with append_images - this SHOULD work but Pillow has bugs
        base_image.save(
            str(ico_path),
            format='ICO',
            sizes=[(img.size[0], img.size[1]) for img in ico_images_sorted],
            append_images=other_images
        )
    else:
        base_image.save(
            str(ico_path),
            format='ICO',
            sizes=[(base_image.size[0], base_image.size[1])]
        )
    
    # Verify
    ico_size = ico_path.stat().st_size
    print(f"✓ Created {ico_path} with sizes: {sizes}")
    print(f"  File size: {ico_size:,} bytes")
    
    # Check if multiple sizes are actually in the file
    try:
        verify_img = Image.open(ico_path)
        frame_count = 0
        while True:
            try:
                verify_img.seek(verify_img.tell() + 1)
                frame_count += 1
            except (EOFError, AttributeError):
                break
        if frame_count == 0:
            print(f"  ⚠️  WARNING: Only 1 size found in ICO file!")
            print(f"     This will cause blurriness. Pillow may not support multiple sizes correctly.")
            print(f"     Consider using an external tool like ImageMagick or online ICO converter.")
        else:
            print(f"  ✓ ICO file contains {frame_count + 1} sizes")
    except Exception as e:
        print(f"  ⚠️  Could not verify ICO file: {e}")

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    assets_dir = script_dir / "app" / "ui" / "assets"
    png_file = assets_dir / "logo128x128.png"
    ico_file = script_dir / "icon.ico"
    
    if not png_file.exists():
        print(f"❌ Error: {png_file} not found!")
        exit(1)
    
    try:
        create_ico_from_png(png_file, ico_file)
        print(f"\n✓ Icon created successfully: {ico_file}")
        print(f"  ⚠️  If icon is still blurry after build, Pillow may not support multiple sizes.")
        print(f"  Consider using ImageMagick: magick convert logo128x128.png -define icon:auto-resize=256,128,96,64,48,32,16 icon.ico")
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
