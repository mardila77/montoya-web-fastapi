import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from typing import Optional
from fastapi import FastAPI, Request, Form, File, UploadFile, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Importamos nuestro gestor de Google Sheets y la zona horaria
from app.sheets_manager import sheets_manager, VENEZUELA_TZ

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
    current_year = datetime.now(VENEZUELA_TZ).year
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"], "current_year": current_year},
    )


# Ruta de contacto (debe ir después de la inicialización de app y variables)
@app.get("/contacto")
async def contacto(request: Request):
    current_year = datetime.now(VENEZUELA_TZ).year
    return templates.TemplateResponse(
        "contacto.html",
        {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"], "current_year": current_year},
    )

# --- Rutas de Sectores ---
@app.get("/{sector}")
async def sectores(request: Request, sector: str):
    sectores_validos = ["agricola", "construccion", "petrolera", "mineria", "energia", "nosotros"]
    current_year = datetime.now(VENEZUELA_TZ).year
    if sector in sectores_validos:
        return templates.TemplateResponse(
            f"{sector}.html",
            {"request": request, "phone": CONTACTO["telefono"], "email": CONTACTO["email"], "current_year": current_year},
        )
    return templates.TemplateResponse("index.html", {"request": request, "current_year": current_year})

# Función auxiliar para envío de correos automatizados (Admin + Cliente)
async def enviar_correos_automatizados(
    name: str, 
    email: str, 
    phone: str, 
    service: str, 
    message: str, 
    plate_image: Optional[UploadFile] = None,
    is_whatsapp: bool = False
):
    smtp_user = os.getenv("CONTACT_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not (smtp_user and smtp_password):
        print("Error: SMTP credentials not found in environment.")
        return

    try:
        # --- CORREO 1: Notificación a Marco (Interno) ---
        msg_internal = MIMEMultipart()
        msg_internal['From'] = f"GMPC Web {'[WhatsApp]' if is_whatsapp else ''} <{smtp_user}>"
        msg_internal['To'] = smtp_user
        msg_internal['Subject'] = f"{'WHATSAPP ' if is_whatsapp else ''}Nuevo Lead [{service}]: {name}"

        body_internal = f"{'CONTACTO VÍA WHATSAPP' if is_whatsapp else 'CONTACTO VÍA EMAIL'}\n\n"
        body_internal += f"Nombre: {name}\nEmail: {email}\nTeléfono: {phone}\nServicio: {service}\n\nMensaje:\n{message}"
        msg_internal.attach(MIMEText(body_internal, 'plain', 'utf-8'))

        if plate_image and plate_image.filename:
            file_content = await plate_image.read()
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file_content)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{plate_image.filename}"')
            msg_internal.attach(part)

        # --- CORREO 2: Respuesta Premium al Cliente (Externo) ---
        msg_customer = MIMEMultipart()
        msg_customer['From'] = f"Marco Montoya - GMPC <{smtp_user}>"
        msg_customer['To'] = email
        msg_customer['Subject'] = "Gracias por contactar a Grupo Montoya-Pérez"

        now_ve = datetime.now(VENEZUELA_TZ)
        fecha_ve = now_ve.strftime("%d/%m/%Y")
        hora_ve = now_ve.strftime("%I:%M %p")

        # Extraer solo el primer nombre para el correo de agradecimiento (más personal)
        first_name = name.split()[0] if name else "Cliente"

        html_content = templates.get_template("email_agradecimiento.html").render({
            "name": first_name,
            "fecha": fecha_ve,
            "hora": hora_ve,
            "current_year": now_ve.year
        })
        msg_customer.attach(MIMEText(html_content, 'html', 'utf-8'))

        # Adjuntar Logo como CID para visibilidad en Gmail/Outlook
        logo_path = os.path.join(BASE_DIR, "static", "images", "logo-rectangular.jpeg")
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            msg_img = MIMEImage(logo_data)
            msg_img.add_header('Content-ID', '<logo_gmpc>')
            msg_img.add_header('Content-Disposition', 'inline', filename="logo-rectangular.jpeg")
            msg_customer.attach(msg_img)

        # Envío de ambos correos
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg_internal)
        server.send_message(msg_customer)
        server.quit()
    except Exception as e:
        print(f"Error en envío de correos automatizados: {e}")


# Endpoint para registro asíncrono (WhatsApp) + Notificación por Email Interna
@app.post("/registrar_lead")
async def registrar_lead(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    service: str = Form(...),
    message: str = Form(...),
    channel: str = Form("whatsapp"),
    plate_image: Optional[UploadFile] = File(None)
):
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "message": message,
        "channel": channel
    }
    
    # 1. Registrar en sheets (OPERACIÓN SÍNCRONA CRÍTICA)
    registro_exitoso = sheets_manager.register_lead(data)
    
    if not registro_exitoso:
        print(f"ALERTA CRÍTICA: Falló el registro en Sheets para el lead: {name}")

    # 2. Envío de correos automáticos (Marco + Cliente)
    background_tasks.add_task(
        enviar_correos_automatizados,
        name=name, email=email, phone=phone, service=service, message=message, is_whatsapp=True
    )

    return {"status": "success"}


# Ruta POST para envío de correos desde Contacto (Flujo Asíncrono/AJAX)
@app.post("/enviar_contacto")
async def enviar_contacto(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    service: str = Form(...),
    message: str = Form(...),
    plate_image: Optional[UploadFile] = File(None)
):
    lead_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "message": message,
        "channel": "email"
    }
    # 1. Registrar en Google Sheets (SÍNCRONO)
    sheets_manager.register_lead(lead_data)

    # 2. Envío de correos automáticos (Marco + Cliente)
    background_tasks.add_task(
        enviar_correos_automatizados,
        name=name, email=email, phone=phone, service=service, message=message, plate_image=plate_image
    )

    return {"status": "success"}
