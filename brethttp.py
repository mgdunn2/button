from httplib2 import Http
from json import dumps, load
from datetime import datetime

confData = load(open('button.conf'))
appkey = confData["APPKEY"]
url = "https://www.wasbretontime.com/api/" + appkey + "/addtime"

def send(time):
    data = dumps({'datetime': str(time)})
    http = Http()
    resp, content = http.request(uri=url,method='POST',headers={'Content-Type': 'application/json; charset=UTF-8'},body=data)
    if resp and 'status' in resp:
        return resp['status'] == '200'
    return False
