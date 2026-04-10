import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from dotenv import load_dotenv

# Cargamos las variables de entorno del archivo .env
load_dotenv()

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount(
    "/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static"
)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Extraemos las variables para tenerlas listas
CONTACTO = {"telefono": os.getenv("CONTACT_PHONE"), "email": os.getenv("CONTACT_EMAIL")}


@app.get("/")
async def leer_raiz(request: Request):
    # Inyectamos los datos de contacto de forma dinámica
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"]},
    )


# Ruta de contacto (debe ir después de la inicialización de app y variables)
@app.get("/contacto")
async def contacto(request: Request):
    return templates.TemplateResponse(
        "contacto.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"]},
    )

# Ruta del sector agrícola
@app.get("/agricola")
async def agricola(request: Request):
    return templates.TemplateResponse(
        "agricola.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"]},
    )

# Ruta del sector construcción
@app.get("/construccion")
async def construccion(request: Request):
    return templates.TemplateResponse(
        "construccion.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"]},
    )

# Ruta del sector petrolero
@app.get("/petrolera")
async def petrolera(request: Request):
    return templates.TemplateResponse(
        "petrolera.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"]},
    )

# Ruta del sector minería
@app.get("/mineria")
async def mineria(request: Request):
    return templates.TemplateResponse(
        "mineria.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"]},
    )

# Ruta de Energía
@app.get("/energia")
async def energia(request: Request):
    return templates.TemplateResponse(
        "energia.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"]},
    )

# Ruta Nosotros / Quiénes Somos
@app.get("/nosotros")
async def nosotros(request: Request):
    return templates.TemplateResponse(
        "nosotros.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"]},
    )
