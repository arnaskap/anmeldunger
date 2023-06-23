from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

WRITE_HTML = False

URL_ROOT = 'https://service.berlin.de'
CALENDAR_ENDPOINT = 'terminvereinbarung/termin/all/120686/'
NO_APPT_AVAILABLE_TEXT = 'An diesem Tag sind keine Termine möglich'
APPT_AVAILABLE_TEXT = 'An diesem Tag einen Termin buchen'


def get_parsed_website(url):
    session = requests.Session()
    response = session.get(url, allow_redirects=True)

    if response.status_code != 200:
        raise Exception(f'Bürgeramt website retrieval failed with code {response.status_code}')

    return BeautifulSoup(response.content, 'html.parser')


def filter_available_date_elements(parsed_website):
    available_date_elements = []
    # not_available_date_elements = []

    month_elements = parsed_website.find_all(class_='calendar-month-table')

    if not month_elements:
        raise Exception('No expected calendar elemenets found in website')

    for month_element in month_elements:
        day_elements = month_element.find_all('td')
        for day_element in day_elements:
            day_element_inner = day_element.find('a')
            day_element_title = day_element_inner.get('title') if day_element_inner else day_element.get('title')

            if day_element_title and APPT_AVAILABLE_TEXT in day_element_title:
                available_date_elements.append(day_element_inner)

            # if day_element_title and NO_APPT_AVAILABLE_TEXT in day_element_title:
            #     not_available_date_elements.append(day_element)

    return available_date_elements


calendar_url = urljoin(URL_ROOT, CALENDAR_ENDPOINT)
parsed_appt_calendar = get_parsed_website(calendar_url)
available_dates = filter_available_date_elements(parsed_appt_calendar)

for date in available_dates:
    print(f'{date.get("aria-label")}: {urljoin(URL_ROOT, date.get("href"))}')

if WRITE_HTML:
    file_path = 'output/startpage.html'
    file = open(file_path, 'w')
    file.write(parsed_appt_calendar.prettify())
