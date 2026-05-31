import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from config import CREDENTIALS_PATH, TOKEN_CALENDAR_PATH

SCOPES_CALENDAR = ['https://www.googleapis.com/auth/calendar.readonly']

def _get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_CALENDAR_PATH):
        with open(TOKEN_CALENDAR_PATH, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES_CALENDAR)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_CALENDAR_PATH, 'wb') as f:
            pickle.dump(creds, f)
    return build('calendar', 'v3', credentials=creds)

def eventos_manana():
    try:
        service = _get_calendar_service()
        ahora = datetime.datetime.utcnow()
        manana = ahora + datetime.timedelta(days=1)
        inicio = datetime.datetime(manana.year, manana.month, manana.day, 0, 0, 0).isoformat() + 'Z'
        fin = datetime.datetime(manana.year, manana.month, manana.day, 23, 59, 59).isoformat() + 'Z'

        eventos = service.events().list(
            calendarId='primary',
            timeMin=inicio,
            timeMax=fin,
            singleEvents=True,
            orderBy='startTime'
        ).execute().get('items', [])

        if not eventos:
            return "Mañana no tienes nada en el calendario."

        respuesta = f"Mañana tienes {len(eventos)} evento{'s' if len(eventos) > 1 else ''}. "
        for e in eventos:
            nombre = e.get('summary', 'Evento sin nombre')
            inicio_e = e['start'].get('dateTime', e['start'].get('date', ''))
            if 'T' in inicio_e:
                hora = inicio_e[11:16]
                respuesta += f"A las {hora}, {nombre}. "
            else:
                respuesta += f"{nombre} todo el día. "
        return respuesta
    except Exception as ex:
        return f"No pude acceder al calendario: {ex}"

def eventos_hoy():
    try:
        service = _get_calendar_service()
        ahora = datetime.datetime.utcnow()
        inicio = datetime.datetime(ahora.year, ahora.month, ahora.day, 0, 0, 0).isoformat() + 'Z'
        fin = datetime.datetime(ahora.year, ahora.month, ahora.day, 23, 59, 59).isoformat() + 'Z'

        eventos = service.events().list(
            calendarId='primary',
            timeMin=inicio,
            timeMax=fin,
            singleEvents=True,
            orderBy='startTime'
        ).execute().get('items', [])

        if not eventos:
            return "Hoy no tienes nada en el calendario."

        respuesta = f"Hoy tienes {len(eventos)} evento{'s' if len(eventos) > 1 else ''}. "
        for e in eventos:
            nombre = e.get('summary', 'Evento sin nombre')
            inicio_e = e['start'].get('dateTime', e['start'].get('date', ''))
            if 'T' in inicio_e:
                hora = inicio_e[11:16]
                respuesta += f"A las {hora}, {nombre}. "
            else:
                respuesta += f"{nombre} todo el día. "
        return respuesta
    except Exception as ex:
        return f"No pude acceder al calendario: {ex}"
