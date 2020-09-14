#!usr/bin/python3
#Python script for completing daily symptom checking
#Created using gmails api with code borrowed from the "quickstart" example
#Written by Andrew Kettle, Last edit: 09/09/2020

#ignoring incorrect pylint error
#pylint:disable=E1101 

from __future__ import print_function
import pickle
import base64
import webbrowser
import os.path
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

    #find link for not on campus
    org_html = BeautifulSoup(raw_html, features='html.parser') 
    #email_link = org_html.a['href']
    print(org_html.a['href'])
    email_link = (org_html.a['href']).encode('UTF-8')

    body = {
        'raw' : (base64.urlsafe_b64encode(email_link)).decode(),
        'labelIds' : '["SENT"]',
        'threadid' : message.get('threadId')
    }
    ret_message = service.users().messages().send(userId='me',body=body).execute()

    #Send email

    #terminate


#main convention in python
if __name__ == '__main__':
    main()