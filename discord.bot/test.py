from list import char_list
from list import partition 
import urllib
import json

import requests

from validate_jwt import validate_eve_jwt

char_id_corp = char_list()
const = { 
	"recipient_id": 2116434445, 
	"recipient_type": "character"
}

char_id = [] #Список из 359 словариков
for i in char_id_corp:
	ls = dict(recipient_id = i, recipient_type="character")
	char_id.append(ls)
            
char_id = list(partition(char_id, n=49)) #Разрезали список словариков по 49 значений 
#print(char_id)   

for i in char_id:
	recipient_id = []
	for d in i:
		recipient_id.append(const)
		recipient_id.append(d)
	print(recipient_id)
	
	data = {
		"approved_cost": 0,
		"body": "Письмецо 2 слова",
		"recipients": recipient_id,
		"subject": "str"
	}
	mail = json.dumps(data)
	res = requests.post(url, headers=headers, data=mail)
	print(res.raise_for_status)
