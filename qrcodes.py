#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib
import requests
import shutil
import os 

API_URL = "https://api.qrserver.com/v1/create-qr-code/"
QR_PARAMS = "?color=000000&bgcolor=FFFFFF&qzone=1&margin=0&size=400x400&ecc=L&format=png"


def download_qr_code(description, output_directory="./qrcodes"):
    if len(description) == 0:
        return


    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


    name = description[0].strip()

    if len(description) > 1:
        last_name = description[1].strip()
    else:
        last_name = ''
   

    if len(description) > 2:
        company = description[2].strip()
    else:
        company = ''

    if len(description) > 3:
        role = description[3].strip()
    else:
        role = ''

    if len(description) > 4:
        phone_number = description[4].strip().replace(" ","")
    else:
        phone_number = ''

    if len(description) > 5:
        email = description[5].strip()
    else:
        email = ''

    if len(description) > 6:
        id = description[6].strip()
        id = name + "_" + last_name + "_" +id
    else:
        id = name + "_" + last_name


    vcard_data = generate_vcard_data(name, last_name, company, phone_number, email)
    full_url = API_URL + QR_PARAMS + "&data=" + vcard_data

  

    file_path = output_directory + "/qrcode_" + str(id) + ".png"
    if os.path.exists(file_path):
        print("QrCode already exists for " + str(id) + " (" +  name +  " " +  last_name + ").")
        return False


    r = requests.get(full_url, stream=True)
    if r.status_code == 200:
        print("Downloading qr_code for " + name + " " + last_name)

        with open(file_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)     
    return True


# BEGIN:VCARD
# VERSION:2.1
# FN:Jean Dupont
# N:Dupont;Jean
# ADR;WORK;PREF;QUOTED-PRINTABLE:;Bruxelles 1200=Belgique;6A Rue Th. Decuyper
# LABEL;QUOTED-PRINTABLE;WORK;PREF:Rue Th. Decuyper 6A=Bruxelles 1200=Belgique
# TEL;CELL:+1234 56789
# EMAIL;INTERNET:jean.dupont@example.com
# UID:
# END:VCARD


def generate_vcard_data(first_name, last_name, company, phone_number, email):
    data = "BEGIN:VCARD\nVERSION:A2.1"
    data += "\nFN:" + first_name +' '+last_name
    data += "\nN:" + last_name + ";" + first_name
    data += "\nTEL;CELL:" + phone_number
    data += "\nEMAIL;WORK;INTERNET:" + email
    data += "\nORG:" + company
    data += "\nEND:VCARD\n"

    url_encoded_data = urllib.quote(data)
    return url_encoded_data
