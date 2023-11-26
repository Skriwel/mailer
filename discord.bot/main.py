
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

	random = base64.urlsafe_b64encode(secrets.token_bytes(32)) #создали 32 случайных байта  
	m = hashlib.sha256()
	m.update(random)
	d = m.digest()
	code_challenge = base64.urlsafe_b64encode(d).decode().replace("=", "")

	client_id = '01f2b79e34aa44ddaa90b934ed351d88'


	url = print_auth_url(client_id, code_challenge=code_challenge)
	#code = callback()
	print(f'\nВаша ссылка для авторизации:\n {url}')
	#input('Нажмите любую клавишу после авторизации')
	

	
	


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


	'''data = sso_response.json()
	access_token = data["access_token"]
	jwt = validate_eve_jwt(access_token)
	character_id = jwt["sub"].split(":")[2]
	character_name = jwt["name"]
	sand_mail = ("https://esi.evetech.net/legacy/characters/{character_id}/mail/".format(character_id))

	headers = {
		"Authorization": "Bearer {}".format(access_token)
	}

	res = requests.get(sand_mail, headers=headers)

	print("\nMade request to {} with headers: "
			"{}".format(sand_mail, res.request.headers))

	res.raise_for_status()'''









if __name__ == "__main__":
    main()
