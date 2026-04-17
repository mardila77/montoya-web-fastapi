import base64
import re
import os

img_path = 'static/images/logo-rectangular.jpeg'
html_path = 'templates/email_agradecimiento.html'

if os.path.exists(img_path) and os.path.exists(html_path):
    with open(img_path, 'rb') as f:
        b64_str = base64.b64encode(f.read()).decode()
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Buscamos la etiqueta img con data:image y reemplazamos el Base64
    pattern = r'src="data:image/jpeg;base64,[^"]*"'
    replacement = f'src="data:image/jpeg;base64,{b64_str}"'
    new_html = re.sub(pattern, replacement, html_content)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Logo updated successfully.")
else:
    print(f"Error: Path not found. Img: {os.path.exists(img_path)}, HTML: {os.path.exists(html_path)}")
