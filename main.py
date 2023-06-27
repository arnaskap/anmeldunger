import argparse

from AppointmentRetriever import AppointmentRetriever


parser = argparse.ArgumentParser()

parser.add_argument('--calendar-endpoint', default='terminvereinbarung/termin/all/120686/',
                    help='Website endpoint to initiate calendar checking session with.')
parser.add_argument('--output-path', default=None, help='Directory to output HTML files. Must be set to output files.')
parser.add_argument('--refresh-rate-seconds', default=60, help='How often to refresh for new appointments.')
parser.add_argument('--root-url', default='https://service.berlin.de', help='Root URL of Buergeramt website.')
parser.add_argument('--write-html', action='store_true', default=False,
                    help='Output html files of accessed links. Useful for debugging.')

args = parser.parse_args()

appointment_retriever = AppointmentRetriever(args.root_url, args.calendar_endpoint)

inited_session = appointment_retriever.try_initiate_session()
if not inited_session:
    exit(0)

available_appointments = appointment_retriever.parse_available_appointments()
for appointment in available_appointments:
    print(appointment)
