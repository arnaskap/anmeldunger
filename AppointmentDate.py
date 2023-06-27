class AppointmentDate:
    def __init__(self, date, url):
        self.date = date
        self.url = url

    def __str__(self):
        return f'{self.date} - {self.url}'
