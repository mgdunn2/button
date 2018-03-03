from httplib2 import Http
from json import dumps
from datetime import datetime

class brethttp():
	def __init__(self):
		self.url = "https://www.wasbretontime.com/api/4a3fc4da-900f-429e-8e62-405edb3fc258/addtime"

	def send(self, time):
		data = dumps({'datetime': str(time)})
		http = Http()
		#http.add_credentials("mike", "passwordwordpass")
		resp, content = http.request(uri=self.url,method='POST',headers={'Content-Type': 'application/json; charset=UTF-8'},body=data)
		if resp and 'status' in resp:
			return resp['status'] == '200'
		return False
