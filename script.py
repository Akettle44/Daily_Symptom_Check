#!usr/bin/python3
#Python script for completing daily symptom checking
#Created using gmails api with code borrowed from the "quickstart" example
#Written by Andrew Kettle, Last edit: 09/09/2020

#ignoring incorrect pylint error
#pylint:disable=E1101 

from __future__ import print_function
import pickle
import os.path
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

    subject_line = 'UCI Student Daily Symptom Monitoring'
    #Find email via name (time isn't accurate enough)
    raw_message_list = service.users().messages().list(userId='me').execute()
    messages = raw_message_list.get('messages', [])

    #iterate over messages via id and look for labels
    for message in messages:
        curr_message = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = curr_message.get('payload')
        headers = payload.get('headers', [])
        #print(headers)
        for header in headers:
            if(header['name'] == 'Subject'):
                name = header['value']
                if(name == subject_line):
                    print(name)
        #sender = headers
        #print(sender)

#    if(messages):
#        for message in messages:
#            print(message['threadId']) 
#    else:
#        print("No messages were found")

    #Find Not on campus today

    #Click the above

    #Send email

    #terminate


#main convention in python
if __name__ == '__main__':
    main()