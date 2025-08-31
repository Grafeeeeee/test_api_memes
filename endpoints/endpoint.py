import requests


class Endpoint:
    url = "http://memesapi.course.qa-practice.com"

    def __init__(self, session):
        self.session = session or requests.Session()
        self.response = None

    def check_response_status_is_200(self):
        assert self.response.status_code == 200, f"Ожидался 200, а пришёл {self.response.status_code}"

    def check_response_status_is_400(self):
        assert self.response.status_code == 400, f"Ожидался 400, а пришёл {self.response.status_code}"

    def check_response_status_is_404(self):
        assert self.response.status_code == 404, f"Ожидался 404, а пришёл {self.response.status_code}"

    def check_response_status_is_403(self):
        assert self.response.status_code == 403, f"Ожидался 403, а пришёл {self.response.status_code}"
