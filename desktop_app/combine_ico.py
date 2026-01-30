"""
Combine multiple ICO files into a single multi-size ICO file.
This script combines the individual size ICO files into one icon.ico
"""
from pathlib import Path
from PIL import Image
import sys

def combine_ico_files(ico_files: list, output_path: Path):
    """
    Combine multiple ICO files into a single multi-size ICO.
    
    Args:
        ico_files: List of ICO file paths (sorted by size, largest first)
        output_path: Path to output ICO file
    """
    if not ico_files:
        print("❌ Error: No ICO files provided!")
        return False
    
    # Load all ICO images
    ico_images = []
    sizes_list = []
    
    for ico_file in ico_files:
        if not ico_file.exists():
            print(f"⚠️  Warning: {ico_file} not found, skipping...")
            continue
        
        try:
            img = Image.open(ico_file)
            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            ico_images.append(img)
            sizes_list.append((img.size[0], img.size[1]))
            print(f"  ✓ Loaded {ico_file.name}: {img.size}")
        except Exception as e:
            print(f"⚠️  Warning: Could not load {ico_file}: {e}")
            continue
    
    if not ico_images:
        print("❌ Error: No valid ICO images loaded!")
        return False
    
    # Sort by size (largest first) for better ICO structure
    sorted_data = sorted(zip(ico_images, sizes_list), key=lambda x: x[1][0], reverse=True)
    ico_images_sorted = [img for img, _ in sorted_data]
    sizes_list_sorted = [size for _, size in sorted_data]
    
    # Save as multi-size ICO
    base_image = ico_images_sorted[0]
    append_images = ico_images_sorted[1:] if len(ico_images_sorted) > 1 else []
    
    try:
        if append_images:
            base_image.save(
                str(output_path),
                format='ICO',
                sizes=sizes_list_sorted,
                append_images=append_images
            )
        else:
            base_image.save(
                str(output_path),
                format='ICO',
                sizes=sizes_list_sorted
            )
        
        output_size = output_path.stat().st_size
        print(f"\n✓ Created {output_path}")
        print(f"  File size: {output_size:,} bytes")
        print(f"  Sizes included: {[f'{w}x{h}' for w, h in sizes_list_sorted]}")
        return True
    except Exception as e:
        print(f"❌ Error saving ICO: {e}")
        return False

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    assets_dir = script_dir / "app" / "ui" / "assets"
    output_file = script_dir / "icon.ico"
    
    # List of ICO files to combine (from largest to smallest)
    ico_files = [
        assets_dir / "256x256.ico",
        assets_dir / "128x128.ico",
        assets_dir / "64x64.ico",
        assets_dir / "48x48.ico",
        assets_dir / "32x32.ico",
        assets_dir / "24x24.ico",
        assets_dir / "16x16.ico",
    ]
    
    print("Combining ICO files into icon.ico...")
    print(f"Output: {output_file}\n")
    
    # Try ImageMagick first (better support for multi-size ICO)
    import shutil
    use_imagemagick = False
    if shutil.which('magick'):
        use_imagemagick = True
        print("✓ ImageMagick found - using it for better multi-size ICO support")
        import subprocess
        
        # ImageMagick can combine ICO files directly
        # Method: Convert all ICO files to PNG first, then combine into ICO
        try:
            # Create temporary directory for PNG files
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                png_files = []
                
                # Convert each ICO to PNG
                for ico_file in ico_files:
                    if ico_file.exists():
                        png_file = tmp_path / f"{ico_file.stem}.png"
                        cmd = ['magick', 'convert', str(ico_file), str(png_file)]
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        if result.returncode == 0:
                            png_files.append(png_file)
                            print(f"  ✓ Converted {ico_file.name} to PNG")
                
                if png_files:
                    # Combine all PNG files into one multi-size ICO
                    # ImageMagick will automatically create all sizes
                    cmd = ['magick', 'convert'] + [str(f) for f in png_files] + [
                        '-define', 'icon:auto-resize',
                        str(output_file)
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        output_size = output_file.stat().st_size
                        print(f"\n✓ Created {output_file} using ImageMagick")
                        print(f"  File size: {output_size:,} bytes")
                        print(f"  ✓ ImageMagick properly supports multiple sizes in ICO files")
                        print("\n✓ Success! icon.ico created with multiple sizes.")
                        print("  Now you can:")
                        print("  1. Clear Windows icon cache: clear_icon_cache.bat")
                        print("  2. Build again: ./build.sh")
                        sys.exit(0)
                    else:
                        print(f"⚠️  ImageMagick combine failed: {result.stderr}")
                        print("  Falling back to Pillow...")
        except Exception as e:
            print(f"⚠️  ImageMagick error: {e}")
            print("  Falling back to Pillow...")
    
    # Fallback to Pillow (may not work correctly for multi-size)
    if combine_ico_files(ico_files, output_file):
        print("\n✓ Success! icon.ico created with multiple sizes.")
        print("  ⚠️  WARNING: Pillow may not properly save multiple sizes.")
        print("  For best results, install ImageMagick:")
        print("    https://imagemagick.org/script/download.php")
        print("  Then this script will use ImageMagick automatically.")
        print("\n  Now you can:")
        print("  1. Clear Windows icon cache: clear_icon_cache.bat")
        print("  2. Build again: ./build.sh")
    else:
        print("\n❌ Failed to create icon.ico")
        sys.exit(1)
