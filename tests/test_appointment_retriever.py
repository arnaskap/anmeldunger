from anmeldunger.AppointmentRetriever import AppointmentRetriever
import responses
import unittest
from urllib.parse import urljoin


class TestAppointmentRetriever(unittest.TestCase):
    def setUp(self):
        root_url = 'https://service.berlin.de'
        calendar_endpoint = 'erminvereinbarung/termin/all/120686/'
        session_endpoint_available = 'terminvereinbarung/termin/day/'
        session_endpoint_unavailable = 'terminvereinbarung/termin/taken/'

        self.uut = AppointmentRetriever(root_url, calendar_endpoint)

        with open('data/calendar_with_appointments.html', 'r') as calendar_html_file:
            calendar_url = urljoin(root_url, calendar_endpoint)
            session_available_url = urljoin(root_url, session_endpoint_available)
            session_unavailable_url = urljoin(root_url, session_endpoint_unavailable)

            # Initial url contains a redirect
            self.init_response_available = responses.Response(responses.GET, calendar_url, status=301,
                                                              headers={"Location": session_available_url})
            self.init_response_unavailable = responses.Response(responses.GET, calendar_url, status=301,
                                                                headers={"Location": session_unavailable_url})

            self.successful_session_response = responses.Response(responses.GET, session_available_url, status=200,
                                                                  body=calendar_html_file.read())
            self.unsuccessful_session_response = responses.Response(responses.GET, session_unavailable_url, status=200,
                                                                    body='')

    @responses.activate
    def test_successful_session_initialise(self):
        responses.add(self.init_response_available)
        responses.add(self.successful_session_response)

        inited = self.uut.try_initiate_session()

        self.assertEqual(True, inited)

    @responses.activate
    def test_unsuccessful_session_initialise(self):
        responses.add(self.init_response_unavailable)
        responses.add(self.unsuccessful_session_response)

        inited = self.uut.try_initiate_session()

        self.assertEqual(False, inited)

    @responses.activate
    def test_appointment_retriever_retrieves_appointments(self):
        responses.add(self.init_response_available)
        responses.add(self.successful_session_response)

        self.uut.try_initiate_session()
        appointments = self.uut.parse_available_appointments()

        self.assertEqual(1, len(appointments))
        self.assertEqual('27.06.2023', appointments[0].date)
        self.assertEqual('https://service.berlin.de/terminvereinbarung/termin/time/1687816800/', appointments[0].url)


if __name__ == '__main__':
    unittest.main()
