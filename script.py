#!usr/bin/python3
#Python script for completing daily symptom checking
#Created using gmails api with credential code borrowed from the "quickstart" example
#Written by Andrew Kettle, Last edit: 09/14/2020

#ignoring incorrect pylint error
#pylint:disable=E1101 

from __future__ import print_function
import pickle
import base64
import webbrowser
import os.path
import urllib.parse
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from email.utils import formatdate
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#Scopes are used to define what you plan on doing with the email
SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.modify']

def main():

    #Log in to gmail account
    creds = None
    #token file already exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    #Token file doesn't already exist or credentials failed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    desired_message_id = None
    #getting current date
    curr_date = formatdate(localtime=True)
    _, curr_day, curr_month, curr_year, _, _ = curr_date.split() #ignoring time and day of the week

    #Filter for desired email
    raw_message_list = service.users().messages().list(userId='me', q="subject:UCI Student Daily Symptom Monitoring").execute()
    messages = raw_message_list.get('messages', [])
    for message in messages:
        curr_message = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Date']).execute()
        email_date = ((curr_message.get('payload').get('headers'))[0])['value'] #can hardcode 0 because there is only one element in the list
        _, day, month, year, _, _, _ = email_date.split() #ignoring time and day of the week
        if(int(day) < 10): #incredibly lazy fix to mismatched day formatting
            day = '0' + day
        if((curr_day == day) and (curr_month == month) and (curr_year==year)):
            desired_message_id = message['id']
            break

    #open email and convert base64url to raw html 
    message = service.users().messages().get(userId='me',id=desired_message_id).execute()
    raw_message = message.get('payload').get('parts')
    filtered_message = raw_message[0] #first attachment is the link
    unfilt_b64 = (filtered_message['body'])['data']
    raw_html = base64.urlsafe_b64decode(unfilt_b64)

    #find link for not on campus, decode the web format into recip, subject, body
    org_html = BeautifulSoup(raw_html, features='html.parser') 
    email_link = org_html.a['href'] #getting the reply url from the formatting html
    link = urllib.parse.unquote(email_link) #removing web formatting from the link
    flink1 = link.split('?subject=') #splitting to find subject and recipient
    recip = flink1[0].replace('mailto:', '') 
    flink2 = flink1[1].split('&body=') #splitting to find the body of the email
    subject = flink2[0]
    body = flink2[1]

    #create reply
    send_message = MIMEText(body)
    send_message['to'] = recip
    send_message['subject'] = subject
    raw_send_message = base64.urlsafe_b64encode((send_message.as_string()).encode('UTF-8'))
    raw_msg = {'raw': raw_send_message.decode('UTF-8')}

    ret_message = service.users().messages().send(userId='me',body=raw_msg).execute()


#main convention in python
if __name__ == '__main__':
    main()