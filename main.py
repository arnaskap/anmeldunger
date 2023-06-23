from bs4 import BeautifulSoup
import requests

WRITE_HTML = True

appt_calendar_url = 'https://service.berlin.de/dienstleistung/120686/'

session = requests.Session()
response = session.get(appt_calendar_url, allow_redirects=True)

if response.status_code != 200:
    raise Exception(f'Request failed with code {response.status_code}')

response = session.get('https://service.berlin.de/terminvereinbarung/termin/all/120686/', allow_redirects=True)

if response.status_code != 200:
    raise Exception(f'Request failed with code {response.status_code}')

appt_calendar_soup = BeautifulSoup(response.content, 'html.parser')
print(appt_calendar_soup.prettify())

if WRITE_HTML:
    file_path = 'output/startpage.html'
    file = open(file_path, 'w')
    file.write(appt_calendar_soup.prettify())
