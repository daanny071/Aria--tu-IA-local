import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from config import CREDENTIALS_PATH, TOKEN_GMAIL_PATH

SCOPES_GMAIL = ['https://www.googleapis.com/auth/gmail.readonly']

def _get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_GMAIL_PATH):
        with open(TOKEN_GMAIL_PATH, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES_GMAIL)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_GMAIL_PATH, 'wb') as f:
            pickle.dump(creds, f)
    return build('gmail', 'v1', credentials=creds)

def emails_no_leidos():
    try:
        service = _get_gmail_service()
        resultado = service.users().messages().list(
            userId='me',
            labelIds=['INBOX', 'UNREAD'],
            maxResults=5
        ).execute()

        mensajes = resultado.get('messages', [])
        if not mensajes:
            return "No tienes emails sin leer."

        total = resultado.get('resultSizeEstimate', len(mensajes))
        respuesta = f"Tienes {total} emails sin leer. Los últimos son: "

        for msg in mensajes[:3]:
            detalle = service.users().messages().get(
                userId='me', id=msg['id'], format='metadata',
                metadataHeaders=['From', 'Subject']
            ).execute()
            headers = {h['name']: h['value'] for h in detalle['payload']['headers']}
            remitente = headers.get('From', 'Desconocido').split('<')[0].strip()
            asunto = headers.get('Subject', 'Sin asunto')
            respuesta += f"De {remitente}, asunto: {asunto}. "

        return respuesta
    except Exception as ex:
        return f"No pude acceder al correo: {ex}"

def leer_ultimo_email():
    try:
        service = _get_gmail_service()
        resultado = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            maxResults=1
        ).execute()

        mensajes = resultado.get('messages', [])
        if not mensajes:
            return "No tienes emails en la bandeja de entrada."

        msg = service.users().messages().get(
            userId='me', id=mensajes[0]['id'], format='full'
        ).execute()

        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        remitente = headers.get('From', 'Desconocido').split('<')[0].strip()
        asunto = headers.get('Subject', 'Sin asunto')

        cuerpo = ""
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    cuerpo = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    break
        elif 'body' in msg['payload']:
            data = msg['payload']['body'].get('data', '')
            cuerpo = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

        cuerpo = cuerpo.strip()[:500]
        return f"Último email de {remitente}, asunto: {asunto}. Contenido: {cuerpo}"
    except Exception as ex:
        return f"No pude leer el email: {ex}"
