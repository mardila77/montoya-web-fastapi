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
