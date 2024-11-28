import requests

url = "http://192.168.1.130:8191/v1"
headers = {"Content-Type": "application/json"}
data = {
    "cmd": "request.get",
    "url": "http://es.ninemanga.com/manga/Kusuriya+no+Hitorigoto.html",
    "maxTimeout": 60000
}
response = requests.post(url, headers=headers, json=data)
print(response.text)