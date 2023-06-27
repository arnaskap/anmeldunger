from AppointmentDate import AppointmentDate
from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import urljoin


NO_APPT_AVAILABLE_TEXT = 'An diesem Tag sind keine Termine möglich'
APPT_AVAILABLE_TEXT = 'An diesem Tag einen Termin buchen'
TAKEN_URL = 'https://service.berlin.de/terminvereinbarung/termin/taken/'


class AppointmentRetriever:
    def __init__(self, url_root, calendar_endpoint):
        self._url_root = url_root
        self._calendar_url = urljoin(url_root, calendar_endpoint)

        self._session = None
        self._session_url = None

    def _get_for_session(self, url):
        response = self._session.get(url, allow_redirects=True)

        if response.status_code != 200:
            raise Exception(f'{self._calendar_url} retrieval failed with code {response.status_code}')

        return response

    def _parse_appointment_date(self, appointment_element):
        date = re.match(r'\d\d\.\d\d\.\d\d\d\d', appointment_element.get('title')).group()
        url = urljoin(self._url_root, appointment_element.get('href'))
        return AppointmentDate(date, url)

    def try_initiate_session(self):
        print(f'Starting new session with {self._calendar_url}')
        self._session = requests.Session()
        response = self._get_for_session(self._calendar_url)

        if response.url == TAKEN_URL:
            print(f'No appointments currently available')
            return False

        print(f'Succesfully started session, using {response.url} as the session URL')
        self._session_url = response.url
        return True

    def parse_available_appointments(self):
        response = self._get_for_session(self._calendar_url)
        parsed_website = BeautifulSoup(response.content, 'html.parser')

        available_date_elements = []

        month_elements = parsed_website.find_all(class_='calendar-month-table')

        if not month_elements:
            raise Exception('No expected calendar elements found in website')

        for month_element in month_elements:
            day_elements = month_element.find_all('td')
            for day_element in day_elements:
                day_element_inner = day_element.find('a')
                day_element_title = day_element_inner.get('title') if day_element_inner else day_element.get('title')

                if day_element_title and APPT_AVAILABLE_TEXT in day_element_title:
                    available_date_elements.append(self._parse_appointment_date(day_element_inner))

        return available_date_elements
