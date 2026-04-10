import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional
from fastapi import FastAPI, Request, Form, File, UploadFile
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

# Ruta POST para envío de correos desde Contacto
@app.post("/enviar_contacto")
async def enviar_contacto(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    plate_image: Optional[UploadFile] = File(None)
):
    # Variables de entorno
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = os.getenv("CONTACT_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if smtp_password and smtp_user:
        try:
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = smtp_user  # Se envían el correo a sí mismos (Grupo Montoya-Pérez)
            msg['Subject'] = f"Nuevo Contacto Web: {name}"

            body = f"Nombre del prospecto: {name}\nCorreo de contacto: {email}\n\nMensaje:\n{message}"
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # Si hay imagen anexada, la extraemos y codificamos
            if plate_image and plate_image.filename:
                file_content = await plate_image.read()
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file_content)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{plate_image.filename}"')
                msg.attach(part)

            # Envío real del correo al servicio SMTP de Google
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Error interno SMTP: {e}")
            # En producción, esto debería disparar un alert a la terminal.

    # Indiferentemente del estado del SMTP, respondemos éxito visualmente en web
    return templates.TemplateResponse(
        "contacto.html",
        {
            "request": request, 
            "phone": CONTACTO["telefono"], 
            "email": CONTACTO["email"],
            "exito": True
        },
    )
