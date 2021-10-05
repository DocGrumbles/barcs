#! python 3

import requests
import re
from bs4 import BeautifulSoup
import os.path
from twilio.rest import Client

URL = "https://www.barcs.org/adopt-dogs/#"
URL2 = "https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals2.aspx?species=Dog&gender=A&agegroup=All&location=&site=&onhold=A&orderby=ID&colnum=5&css=https://barcs.org/static/css/petango.css&authkey=5p95485kw470oqji4yeo8v83f77y591y9ll587m45p3wk477go&recAmount=&detailsInPopup=No&featuredPet=Include&stageID="

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}

# Path where project is saved
save_path = 'PYTHON FOLDER'
barcs = os.path.join(save_path, "barcs.txt")
# Add your Twilio Account Number Below*
account = '*TWILIO ACCOUNT NUMBER'
# Add your Twilio AUTH Token Number Below*
token = 'TWILIO AUTH TOKEN'

def get_source():
    page = requests.get(URL2, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser') # this is a class object
    soup_string = str(soup1)
    clean_txt = re.sub(r'<a href(.*?)>', '', soup_string)
   
    if os.path.exists(barcs):
        print("Barcs.txt file exists and will now be overwritten!")
        with open(barcs, "r+") as f:
            f.seek(0)
            f.write(clean_txt)
            f.truncate()
            f.close()
    else:
        print("The Barcs.txt file does not exist. Creating it now!")
        f = open(barcs, "a")
        f.write(clean_txt)
        f.close()

# Scrapes barcs.txt for dog names and breeds and adds them to a dictionary
def scrape_lists():

    textfile = open(barcs, "r")
    filetext = textfile.read()
    check_names = re.findall(r'list-animal-name">(.*?)<', filetext)
    check_breed = re.findall(r'list-animal-breed">(.*?),', filetext)
    textfile.close()
    
    name_and_breed = {}
    for key in check_names:
        for value in check_breed:
            name_and_breed[key] = value
            break

    for value in name_and_breed.values():
      # Update the values to specify the breed of dog you are looking for
        if value == 'Corgi' or value == 'Basset Hound':
            send_sms()
            break
        else:
            break

# Send a text message notification
def send_sms():
    #access Twilio Accound SID and AUTH token
    client = Client(account, token)

    try:
        client.messages.create(to = "*RECEIVER NUMBER*", 
                                from_="*TWILIO SENDER NUMBER*", #Twilio account number
                                body = 'Hello! Either a Corgi or a Basset Hound has been identified on the barcs website!' 
                                )
        print("Successfully sent SMS message!")
    except Exception as e:
        print(e)

get_source()
scrape_lists()
