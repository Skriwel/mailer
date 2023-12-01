
import base64
import hashlib
import secrets

from app import callback
import flask
from flask import request
from flask import Flask

from validate_jwt import validate_eve_jwt

from shared_flow import print_auth_url
from shared_flow import send_token_request
from shared_flow import handle_sso_token_response

def main():

	random = base64.urlsafe_b64encode(secrets.token_bytes(32)) 
	m = hashlib.sha256()
	m.update(random)
	d = m.digest()
	code_challenge = base64.urlsafe_b64encode(d).decode().replace("=", "")

	client_id = '01f2b79e34aa44ddaa90b934ed351d88'

	url = print_auth_url(client_id, code_challenge=code_challenge)

	print(f'\nВаша ссылка для авторизации:\n {url}')
	
	auth_code = input('\n\nПройдите авторизацию, после чего вас перебросит на новую страницу. Откройте строку с ссылкой и скопируйте значение после code=<букафки и циферки> до знака "&" \n**ПРИМЕР** То, что вам нужно скопировать выделено жирным: https: //localhost:5000/callback/?code=**1o-L5VR030uIdvIBFjILAw**&state=qwery \n\n Ваш код: ')
	
	code_verifier = random
	form_values = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": auth_code,
        "code_verifier": code_verifier
    }

	res = send_token_request(form_values)
	
	handle_sso_token_response(res)

if __name__ == "__main__":
	main()
