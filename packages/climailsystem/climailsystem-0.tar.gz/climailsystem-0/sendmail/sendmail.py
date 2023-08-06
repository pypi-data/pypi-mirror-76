from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import os
import urllib
from apiclient import errors
import base64
import email
import click
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.readonly']
def credentialcreater():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    try:
        creds = None
        dir_path = os.path.dirname(os.path.realpath(__file__))
        nameoffile = os.path.join(dir_path,'token.pickle')
        if os.path.exists(nameoffile):
            with open(nameoffile, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                path_creds = os.path.join(dir_path,'client.json')
                if os.path.exists(path_creds) != True:
                    credentials_api = input('Enter Credentials')
                    with open(path_creds,'w+') as  cl:
                        cl.write(credentials_api)
                flow = InstalledAppFlow.from_client_secrets_file(path_creds, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(nameoffile, 'wb') as token:
                pickle.dump(creds, token)
        service = build('gmail', 'v1', credentials=creds)
        user_token = service.users()
        return user_token
    except:
        print("Error in verifying credentials please verify your credits")
        try:
            os.remove(path_creds)
        except:
            print('try again')
        exit()
def usermessagedetails():
    data = creds.getProfile(userId="me").execute()
    return data
def userdetails():
    data = creds.settings().sendAs().list(userId="me").execute()
    return data
def deleteapicreds():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path,'client.json')
    os.remove(filename)
def login():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir_path,'token.pickle')
    global creds
    os.remove(filename)
    creds = credentialcreater()
def sendmessage(email,subject,mssg):
  message = MIMEText(mssg)
  message['to'] = email
  message['from'] = "me"
  message['subject'] = subject
  mssg_to_be_send = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
  try:
    message = (creds.messages().send(userId="me", body=mssg_to_be_send)
               .execute())
  except urllib.error.HTTPError as error:
    print('An error occurred: %s' % error)
def sendmessage_attach(email_id,subject,mssg,file_path):
  message = MIMEMultipart()
  message['to'] = email_id
  message['from'] = "me"
  message['subject'] = subject

  msg = MIMEText(mssg)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file_path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file_path, 'r')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file_path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file_path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file_path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file_path)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  mssg_send =  {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
  try:
    message = (creds.messages().send(userId="me", body=mssg_send)
               .execute())
  except urllib.error.HTTPError as error:
    print('An error occurred: %s' % error)
creds = credentialcreater()
