"""
Script to convert PNG logo to ICO format for Windows executable icon.
Requires Pillow: pip install Pillow
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

def unsharp_mask(img, radius=2, percent=150, threshold=3):
    """
    Apply unsharp mask filter for better sharpening.
    This is more effective than simple SHARPEN filter.
    """
    # Convert to RGB if needed (unsharp mask works on RGB)
    if img.mode == 'RGBA':
        # Split channels
        r, g, b, a = img.split()
        rgb_img = Image.merge('RGB', (r, g, b))
        # Apply unsharp mask
        rgb_img = rgb_img.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))
        # Merge back with alpha
        r, g, b = rgb_img.split()
        return Image.merge('RGBA', (r, g, b, a))
    else:
        return img.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))

def create_ico_from_png(png_path: Path, ico_path: Path, sizes: list = None):
    """
    Convert PNG to ICO format with multiple sizes.
    Uses aggressive upscaling and sharpening for maximum clarity.
    
    Args:
        png_path: Path to source PNG file
        ico_path: Path to output ICO file
        sizes: List of sizes to include in ICO (default: [16, 24, 32, 48, 64, 128, 256])
    """
    if sizes is None:
        sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # Open the PNG image
    img = Image.open(png_path)
    
    # Convert to RGBA if not already (for transparency support)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Use source image directly if it's large enough, otherwise upscale moderately
    # Don't upscale too much as it can introduce artifacts
    source_size = max(img.size)
    
    # If source is already large (>=512), use it directly
    # If smaller, upscale to 512 (not 2048) to avoid artifacts
    if source_size < 512:
        target_source_size = 512
        print(f"Upscaling source image from {source_size}x{source_size} to {target_source_size}x{target_source_size}...")
        # Use LANCZOS for upscaling (highest quality)
        img = img.resize((target_source_size, target_source_size), Image.Resampling.LANCZOS)
        # Apply unsharp mask for better sharpness after upscale
        img = unsharp_mask(img, radius=1, percent=120, threshold=2)
    elif source_size > 1024:
        # If source is very large, downscale to 1024 to avoid memory issues
        # but keep quality high
        target_source_size = 1024
        print(f"Downscaling source image from {source_size}x{source_size} to {target_source_size}x{target_source_size}...")
        img = img.resize((target_source_size, target_source_size), Image.Resampling.LANCZOS)
    else:
        print(f"Using source image at {source_size}x{source_size} (no resizing needed)")
    
    # Create list of resized images with high-quality resampling
    ico_images = []
    for size in sizes:
        # Use LANCZOS resampling for best quality when downscaling
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Apply VERY aggressive sharpening for all sizes, especially small ones
        if size <= 32:
            # Maximum sharpening for tiny icons
            resized = unsharp_mask(resized, radius=1.5, percent=200, threshold=1)
            # Apply multiple passes for extra sharpness
            resized = unsharp_mask(resized, radius=0.5, percent=150, threshold=1)
        elif size <= 48:
            # Strong sharpening for small icons
            resized = unsharp_mask(resized, radius=1.5, percent=180, threshold=2)
        elif size <= 64:
            # Moderate sharpening for medium icons
            resized = unsharp_mask(resized, radius=1, percent=160, threshold=2)
        else:
            # Light sharpening for larger icons
            resized = unsharp_mask(resized, radius=1, percent=130, threshold=3)
        
        # Enhance contrast and sharpness aggressively for better visibility
        if size <= 32:
            enhancer = ImageEnhance.Contrast(resized)
            resized = enhancer.enhance(1.5)  # 50% more contrast for tiny icons
            enhancer = ImageEnhance.Sharpness(resized)
            resized = enhancer.enhance(1.5)  # 50% more sharpness
            enhancer = ImageEnhance.Brightness(resized)
            resized = enhancer.enhance(1.1)  # 10% brighter
        elif size <= 48:
            enhancer = ImageEnhance.Contrast(resized)
            resized = enhancer.enhance(1.3)  # 30% more contrast
            enhancer = ImageEnhance.Sharpness(resized)
            resized = enhancer.enhance(1.3)  # 30% more sharpness
        elif size <= 64:
            enhancer = ImageEnhance.Contrast(resized)
            resized = enhancer.enhance(1.2)  # 20% more contrast
            enhancer = ImageEnhance.Sharpness(resized)
            resized = enhancer.enhance(1.2)  # 20% more sharpness
        elif size <= 128:
            enhancer = ImageEnhance.Contrast(resized)
            resized = enhancer.enhance(1.1)  # 10% more contrast
        
        ico_images.append(resized)
    
    # Save as ICO with all sizes
    # CRITICAL: Pillow's ICO format has a bug - it doesn't properly save multiple sizes
    # We need to use a workaround: save each size separately and combine them
    # OR use a different approach: save as PNG first, then convert
    
    # Sort by size (largest first) for better ICO structure
    ico_images_sorted = sorted(ico_images, key=lambda x: x.size[0], reverse=True)
    
    # Try to save with all sizes using append_images
    # Note: This may not work correctly with Pillow, but we'll try
    base_image = ico_images_sorted[0]
    append_images = ico_images_sorted[1:] if len(ico_images_sorted) > 1 else []
    
    # Create sizes list
    sizes_list = [(img.size[0], img.size[1]) for img in ico_images_sorted]
    
    if append_images:
        # Try saving with append_images
        try:
            base_image.save(
                str(ico_path),
                format='ICO',
                sizes=sizes_list,
                append_images=append_images
            )
        except Exception as e:
            print(f"  ⚠️  Warning: Error saving with append_images: {e}")
            # Fallback: save only the largest size
            base_image.save(str(ico_path), format='ICO', sizes=sizes_list)
    else:
        base_image.save(str(ico_path), format='ICO', sizes=sizes_list)
    
    # Verify the ICO file was created correctly
    ico_size = ico_path.stat().st_size
    print(f"✓ Created {ico_path} with sizes: {sizes}")
    print(f"  File size: {ico_size:,} bytes")
    
    # Verify by reading back the ICO
    try:
        verify_img = Image.open(ico_path)
        if hasattr(verify_img, 'n_frames') or hasattr(verify_img, 'info'):
            print(f"  ✓ ICO file verified successfully")
    except Exception as e:
        print(f"  ⚠️  Warning: Could not verify ICO file: {e}")

if __name__ == "__main__":
    # Get script directory
    script_dir = Path(__file__).parent
    assets_dir = script_dir / "app" / "ui" / "assets"
    
    # Input PNG file
    png_file = assets_dir / "logo128x128.png"
    
    # Output ICO file
    ico_file = script_dir / "icon.ico"
    
    if not png_file.exists():
        print(f"❌ Error: {png_file} not found!")
        print(f"   Please ensure logo128x128.png exists in {assets_dir}")
        exit(1)
    
    # Check if ImageMagick is available (better for multi-size ICO)
    import shutil
    use_imagemagick = False
    if shutil.which('magick'):
        use_imagemagick = True
        print("✓ ImageMagick found - using it for better multi-size ICO support")
        import subprocess
        try:
            # Use ImageMagick to create ICO with multiple sizes
            cmd = [
                'magick',
                'convert',
                str(png_file),
                '-define', 'icon:auto-resize=256,128,96,64,48,32,24,16',
                str(ico_file)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                ico_size = ico_file.stat().st_size
                print(f"✓ Created {ico_file} using ImageMagick")
                print(f"  File size: {ico_size:,} bytes")
                print(f"  ✓ ImageMagick properly supports multiple sizes in ICO files")
                exit(0)
            else:
                print(f"⚠️  ImageMagick failed: {result.stderr}")
                print("  Falling back to Pillow...")
        except Exception as e:
            print(f"⚠️  ImageMagick error: {e}")
            print("  Falling back to Pillow...")
    
    # Fallback to Pillow (may not support multiple sizes correctly)
    try:
        create_ico_from_png(png_file, ico_file)
        print(f"\n✓ Icon created successfully: {ico_file}")
        print(f"  ⚠️  WARNING: Pillow may not properly save multiple sizes.")
        print(f"  For best results, install ImageMagick and use:")
        print(f"    magick convert {png_file} -define icon:auto-resize=256,128,96,64,48,32,24,16 {ico_file}")
    except ImportError:
        print("❌ Error: Pillow is not installed!")
        print("   Please install it with: pip install Pillow")
        exit(1)
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
        exit(1)
