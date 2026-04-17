import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz

# Configuración de zona horaria de Venezuela
VENEZUELA_TZ = pytz.timezone('America/Caracas')

class GMPCSheetsManager:
    def __init__(self):
        self.credentials_path = os.path.join(os.getcwd(), 'google_credentials.json')
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.client = None
        self.sheet_name = "GMPC_Leads"

    def _authenticate(self):
        """Autenticación con la cuenta de servicio de Google."""
        if not os.path.exists(self.credentials_path):
            print(f"ALERTA: No se encontró el archivo {self.credentials_path}. La integración con Sheets está desactivada.")
            return False
        
        try:
            creds = Credentials.from_service_account_file(self.credentials_path, scopes=self.scopes)
            self.client = gspread.authorize(creds)
            return True
        except Exception as e:
            print(f"Error al autenticar con Google Sheets: {e}")
            return False

    def register_lead(self, data: dict):
        """
        Registra un nuevo lead en la hoja de cálculo.
        Data esperada: {name, email, phone, service, message, channel}
        """
        if not self.client and not self._authenticate():
            return False

        try:
            # Obtener o crear la hoja
            try:
                spreadsheet = self.client.open(self.sheet_name)
            except gspread.exceptions.SpreadsheetNotFound:
                # Si no existe, se debería crear manualmente y compartir, 
                # pero gspread permite crearla si se desea. 
                # Sin embargo, siguiendo el plan, Marco la crea y la comparte.
                print(f"Error: La hoja '{self.sheet_name}' no fue encontrada o no ha sido compartida con el robot.")
                return False

            sheet = spreadsheet.get_worksheet(0) # Primera pestaña

            # Preparar la fila
            now = datetime.now(VENEZUELA_TZ)
            fecha = now.strftime("%d/%m/%Y")
            hora = now.strftime("%H:%M:%S")

            row = [
                fecha,
                hora,
                data.get("name"),
                data.get("email"),
                data.get("phone"),
                data.get("service"),
                data.get("message"),
                data.get("channel")
            ]

            sheet.append_row(row)
            return True
        except Exception as e:
            print(f"Error al registrar lead en Sheets: {e}")
            return False

# Instancia global para uso en la app
sheets_manager = GMPCSheetsManager()
