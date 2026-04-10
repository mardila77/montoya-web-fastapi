import os
import re
import glob
template_dir = r"d:\montoya-web-fastapi\templates"
files = glob.glob(os.path.join(template_dir, "*.html"))

pattern = re.compile(
    r'[ \t]*<h1 style="color: var\(--color-secundario-amarillo-cat, #FFCD00\); text-shadow: 1px 1px 5px rgba\(0,0,0,0\.8\); margin: 0; font-size: 1\.5em; letter-spacing: 1px;">\s*<a href="/" style="color: inherit; text-decoration: none;">Grupo Montoya-Pérez</a>\s*</h1>',
    re.MULTILINE
)

replacement = r'''            <h1 style="margin: 0; padding: 0; display: flex; align-items: center;">
                <a href="/" style="display: block; line-height: 0; text-decoration: none;">
                    <img src="{{ url_for('static', path='images/logo1x1.jpeg') }}" alt="Grupo Montoya-Pérez" style="height: 55px; width: auto; border-radius: 50%; box-shadow: 0 4px 15px rgba(0,0,0,1); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                </a>
            </h1>'''

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    new_content, count = pattern.subn(replacement, content)
    if count > 0:
        with open(f, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"Updated {f}")
