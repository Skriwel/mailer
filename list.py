import requests
import json
import sqlite3

db = sqlite3.connect('char.db')
cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
	characters INT
)''')
db.commit()

def partition(l, n=None):
		for i in range(0, len(l), n):
			yield l[i:i + n]

def char_list():
	l = []
	for i in open('text.txt'):
		l.append(i[:-1])

	char_list = list(partition(l, n=500))

	new_corp = [1000165, 1000166, 1000077, 1000044, 1000045, 1000167, 1000169, 1000168, 1000115, 1000172, 1000170, 1000171]
	char_id_corp = []

	url_char_id = "https://esi.evetech.net/latest/universe/ids/"
	url_corp_id = "https://esi.evetech.net/latest/characters/affiliation/"

	headers = {
		"Accept-Language": "en"
	}

	for lst in char_list:

		data = json.dumps(lst)
		res = requests.post(url_char_id, headers=headers, data=data)
		print('Получение ID персонажей: ', res.status_code)

		id_char = json.loads(res.text) #создаём словарь из ответа АПИ

		char_id_list = []  
		for char in id_char['characters']:
			char_id_list.append(char['id'])

		data = json.dumps(char_id_list)
		res_corp = requests.post(url_corp_id, data=data)
		print('Получение ID корпораций: ', res_corp.status_code)
	
		id_corp = json.loads(res_corp.text)
		for i in id_corp:
			if i['corporation_id'] in new_corp:
	
				res = cur.execute('SELECT * FROM users WHERE characters=?', (i['character_id'],))
				if res.fetchone() is None:
					char_id_corp.append(i['character_id'])
					

	print('Подходящих персонажей:', len(char_id_corp))
	return char_id_corp


