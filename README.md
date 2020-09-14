# Daily Symptom Check

## Description
The school I am attending has started sending emails about daily symptom checks for Covid-19. I support this fully for people who are in the school's area as it should slow down the spread. However, for people living at home with no intentions of going to campus at all (me), it doesn't make a lot of sense to fill it out every day. This script finds the correct email, extracts relevant information, and creates a correctly formatted reply. 

Environment: Python 3.6.9 <br/>
Necessary Packages: pickle, base64, os.path, urllib.parse, MIMEText, BeautifulSoup, formatdate <br/>
This script interfaces with gmail's api (since our school's email is run through gmail), so various packages from gmail will also be necessary. <br/>
OS: Anything with a python interpreter (only tested on elementary OS) <br/>

## Installing pacakages
```
pip3 install urllib3 bs4 --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Enabling Gmail

In order to use this script, you will need to allow the gmail api to interface with it. Follow this link: https://developers.google.com/gmail/api/quickstart/python and perform step one to allow access. Make sure that the client configuration file is downloaded to the current working directory, as the guide says. Having your credentials as a local file means that embedding your login data into the script isn't necessary.

## Running the script

In the python interpreter
```
./dsc.py
```

From bash 
```
python3 ./dsc.py
```
If running it via bash fails, make sure that the first line ```#!usr/bin/python3``` is reflective of where your python source is installed.



