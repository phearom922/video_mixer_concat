"""
Script to convert PNG logo to ICO format for Windows executable icon.
Requires Pillow: pip install Pillow
"""
from pathlib import Path
from PIL import Image

def create_ico_from_png(png_path: Path, ico_path: Path, sizes: list = None):
    """
    Convert PNG to ICO format with multiple sizes.
    
    Args:
        png_path: Path to source PNG file
        ico_path: Path to output ICO file
        sizes: List of sizes to include in ICO (default: [16, 32, 48, 64, 128, 256])
    """
    if sizes is None:
        sizes = [16, 32, 48, 64, 128, 256]
    
    # Open the PNG image
    img = Image.open(png_path)
    
    # Create list of resized images
    ico_images = []
    for size in sizes:
        # Resize maintaining aspect ratio
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        ico_images.append(resized)
    
    # Save as ICO
    ico_images[0].save(
        ico_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in ico_images]
    )
    print(f"✓ Created {ico_path} with sizes: {sizes}")

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
    
    try:
        create_ico_from_png(png_file, ico_file)
        print(f"\n✓ Icon created successfully: {ico_file}")
        print(f"  You can now use this in pyinstaller.spec")
    except ImportError:
        print("❌ Error: Pillow is not installed!")
        print("   Please install it with: pip install Pillow")
        exit(1)
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
        exit(1)
