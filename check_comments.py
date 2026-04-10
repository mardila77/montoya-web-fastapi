import os
import glob
template_dir = r"d:\montoya-web-fastapi\templates"
files = glob.glob(os.path.join(template_dir, "*.html"))

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "/*" in line:
                print(f"{os.path.basename(f)}:{i+1}: {line.strip()}")
