from httplib2 import Http
from json import dumps, load

confData = load(open('button.conf'))
appkey = confData["APPKEY"]
url = "https://www.wasbretontime.com/api/" + appkey + "/addtime"

def send(time):
    resp, content = Http().request(
        uri=url,
        method='POST',
        headers={'Content-Type': 'application/json; charset=UTF-8'},
        body=dumps({'datetime': str(time)}))
    return resp and 'status' in resp and resp['status'] == '200'
