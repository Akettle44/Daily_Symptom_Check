#!usr/bin/python3
#Python script for completing daily symptom checking
#Created using gmails api with code borrowed from the "quickstart" example
#Written by Andrew Kettle, Last edit: 09/09/2020

#ignoring incorrect pylint error
#pylint:disable=E1101 

from __future__ import print_function
import pickle
import base64
import os.path
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
    #Filter for desired email

    desired_message_id = None
    #getting current date
    curr_date = formatdate(localtime=True)
    _, curr_day, curr_month, curr_year, _, _ = curr_date.split() #ignoring time and day of the week

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

    #open email and find "not on campus section"
    message = service.users().messages().get(userId='me',id=desired_message_id).execute()
    #message = service.users().messages().get(userId='me',format='raw', id=desired_message_id).execute()
    raw_message = message.get('payload').get('parts')
    filtered_message = raw_message[0] #first attachment is the link
    unfilt_b64 = (filtered_message['body'])['data']
    raw_html = base64.urlsafe_b64decode(unfilt_b64)
    print(raw_html)


    
    #
    #for dtype in raw_message:
    #    print(dtype)
    #    print('\n')
    #    message_link = raw_message('attachmentId')
    #    print(message_link)

    #Click the above

    #Send email

    #terminate


#main convention in python
if __name__ == '__main__':
    main()