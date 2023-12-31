"""Contains all shared OAuth 2.0 flow functions for examples

This module contains all shared functions between the two different OAuth 2.0
flows recommended for web based and mobile/desktop applications. The functions
found here are used by the OAuth 2.0 examples contained in this project.
"""
import urllib
import json

import requests
import sqlite3

from validate_jwt import validate_eve_jwt
from list import char_list
from list import partition

db = sqlite3.connect('char.db')
cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
    characters INT
)''')
db.commit()

def print_auth_url(client_id, code_challenge=None): #функция составления и вывода ссылки для авторизации в консоль
    base_auth_url = "https://login.eveonline.com/v2/oauth/authorize/" #базовая ссылка для авторизации
    params = { #параметры для запроса авторизации
        "response_type": "code",
        "redirect_uri": "https://localhost:5000/callback/",
        "client_id": client_id,
        "scope": "esi-mail.send_mail.v1 esi-mail.read_mail.v1",
        "state": "qwery"
    }

    if code_challenge: #почему нельзя это просто записать в параметры, зачем обновлять? 
        params.update({
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        })

    string_params = urllib.parse.urlencode(params) #кодирование параметров для запроса и сохранение в переменную
    full_auth_url = "{}?{}".format(base_auth_url, string_params) #составление полной ссылки запроса (базовая ссылка + параметры)
    return full_auth_url

def send_token_request(form_values, add_headers={}):

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "login.eveonline.com",
    }

    if add_headers:
        headers.update(add_headers)

    res = requests.post(
        "https://login.eveonline.com/v2/oauth/token",
        data=form_values,
        headers=headers,
    )

    print('\n\nЗапрос на получение токена доступа выполнен: ')
    

    res.raise_for_status()

    return res


def handle_sso_token_response(sso_response):
    if sso_response.status_code == 200:
        data = sso_response.json()
        access_token = data["access_token"]

        #print(access_token)

        jwt = validate_eve_jwt(access_token)
        character_id = jwt["sub"].split(":")[2]
        character_name = jwt["name"]
        url = ("https://esi.evetech.net/latest/characters/{}/mail/".format(character_id))

        
        headers = {
            "Authorization": "Bearer {}".format(access_token)
        }

        char_id_corp = char_list()
        
        char_id = []
        for i in char_id_corp:
            ls = dict(recipient_id = i, recipient_type="character")
            char_id.append(ls)
            
        char_id = list(partition(char_id, n=49)) #Разрезали список словариков по 49 значений 
        #print(char_id)   
        const = {'recipient_id': 2116434445, 'recipient_type': 'character'}
        for i in char_id:
            recipient_id = []
            for d in i:
                recipient_id.append(d)
                if const not in recipient_id:
                    recipient_id.append(const)

            print(len(recipient_id))
        
            data = {
                "approved_cost": 0,
                "body": "Тестовое письмо, пожалуйста игнорируйте",
                "recipients": recipient_id,
                "subject": "str"
            }
            mail = json.dumps(data)
            res = requests.post(url, headers=headers, data=mail)
            print(res.raise_for_status)

            for i in recipient_id:
                cur.execute(f"INSERT INTO users VALUES (?)", (i['recipient_id'],))
                db.commit()


    else:
        print("\nSomething went wrong! Re read the comment at the top of this "
              "file and make sure you completed all the prerequisites then "
              "try again. Here's some debug info to help you out:")
        print("\nSent request with url: {} \nbody: {} \nheaders: {}".format(
            sso_response.request.url,
            sso_response.request.body,
            sso_response.request.headers
        ))
        print("\nSSO response code is: {}".format(sso_response.status_code))
        print("\nSSO response JSON is: {}".format(sso_response.json()))
