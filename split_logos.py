from PIL import Image
import os

def split_logos(image_path, brand_names, output_dir):
    img = Image.open(image_path)
    width, height = img.size
    
    # Grid is 2 columns x 3 rows
    cell_width = width // 2
    cell_height = height // 3
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for i, name in enumerate(brand_names):
        col = i % 2
        row = i // 2
        
        left = col * cell_width
        top = row * cell_height
        right = left + cell_width
        bottom = top + cell_height
        
        logo = img.crop((left, top, right, bottom))
        # Add some padding removal or fine tuning if needed
        # For now, 512x341 is a good base. 
        # We can also resize to a square if preferred.
        
        logo.save(os.path.join(output_dir, f"logo_{name}_premium.png"))
        print(f"Saved: logo_{name}_premium.png")

# Set 1 brands
set1_brands = ["cat", "cummins", "doosan", "hyundai", "international", "iveco"]
# Set 2 brands
set2_brands = ["jcb", "komatsu", "kubota", "mitsubishi", "perkins", "volvo"]

# Paths
base_path = r"C:\Users\mardi\.gemini\antigravity\brain\543d434c-3615-4cba-88d6-df67567a8fc8"
out_path = r"d:\montoya-web-fastapi\static\images\marcas\premium"

split_logos(
    os.path.join(base_path, "industrial_brands_set_01_1776197016897.png"),
    set1_brands,
    out_path
)

split_logos(
    os.path.join(base_path, "industrial_brands_set_02_1776197160062.png"),
    set2_brands,
    out_path
)
