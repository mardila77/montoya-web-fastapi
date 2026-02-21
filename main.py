from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 1. Le decimos a FastAPI dónde están los archivos públicos (CSS, JS, Imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Le decimos a FastAPI dónde están los archivos HTML
templates = Jinja2Templates(directory="templates")


# 3. Modificamos la ruta principal para que cargue la plantilla
@app.get("/")
def leer_raiz(request: Request):
    # Renderizamos el index.html original de la plantilla
    return templates.TemplateResponse("index.html", {"request": request})
