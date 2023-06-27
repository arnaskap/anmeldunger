class AppointmentDate:
    def __init__(self, date, url):
        self._date = date
        self._url = url

    def __str__(self):
        return f'{self._date} - {self._url}'