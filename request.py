import requests
import json


data = {"flower":"1,3,5,7"}
headers = {"Content-Type": "application/json"}

resp = requests.post('http://localhost:5000/iris_post', data=json.dumps(data), headers=headers)

print(resp.text)