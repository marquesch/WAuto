from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from collections import OrderedDict
import time as t
import base64
import os

main_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
gmail_cfg_path = os.path.join(main_dir, 'cfg', 'gmail')
token_path = os.path.join(gmail_cfg_path, 'token.json')
credentials_path = os.path.join(gmail_cfg_path, 'credentials.json')

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def dict_list_to_name_list(disc_dict_list):
    name_list = []
    for disc_dict in disc_dict_list:
        name_list.append(disc_dict['disc_name'])
    return name_list


def get_html_dict(disc_name_list: list, convert=False):
    t.sleep(10)
    if convert:
        disc_name_list = dict_list_to_name_list(disc_name_list)
    no_of_emails = round(len(disc_name_list) * 1.3) + 1
    html_dict = OrderedDict()
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    creds = Credentials.from_authorized_user_file(token_path)
    gmailserv = build('gmail', 'v1', credentials=creds)
    results = gmailserv.users().messages().list(userId='me', maxResults=no_of_emails).execute()
    messages = results.get('messages', [])

    for msg in messages:
        message = gmailserv.users().messages().get(userId='me', id=msg['id']).execute()
        payload = message['payload']
        data = ''

        if 'parts' in payload:
            for p in payload['parts']:
                if p['mimeType'] == 'text/html':
                    data = base64.urlsafe_b64decode(p['body']['data']).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/html':
                data = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        for disc_name in disc_name_list:
            disc_text = f'A disciplina \"{disc_name}\" foi aprovada.'
            if disc_text in data:
                disc_name_list.remove(disc_name)
                html_dict[disc_name] = data

    if len(disc_name_list) > 0:
        print('Disciplinas não encontradas: ')
        for disc in disc_name_list:
            print(disc)

    return html_dict
