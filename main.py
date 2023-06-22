import requests

url = 'https://service.berlin.de/standorte/buergeraemter/'

response = requests.get(url)

if response.status_code == 200:
    print(response.content)
else:
    print(f'Request failed with code {response.status_code}')