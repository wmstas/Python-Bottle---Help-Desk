import requests
response = requests.post('http://localhost/testpost')
print(response.text)
