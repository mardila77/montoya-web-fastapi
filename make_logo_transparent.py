from PIL import Image

def make_transparent(img_path, output_path):
    img = Image.open(img_path)
    img = img.convert("RGBA")
    
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        # If pixel is near white (240-255), make it transparent
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Logo transparentado y guardado en: {output_path}")

base_logo = r"d:\montoya-web-fastapi\static\images\logo-premium.png"
glass_logo = r"d:\montoya-web-fastapi\static\images\logo-glass-v3.png"

make_transparent(base_logo, glass_logo)
