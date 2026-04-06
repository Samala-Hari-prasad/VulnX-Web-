import requests
import time
from urllib.parse import urljoin

class Requester:
    def __init__(self, headers=None, cookies=None, timeout=5):
        self.session = requests.Session()
        self.timeout = timeout
        if headers:
            self.session.headers.update(headers)
        if cookies:
            self.session.cookies.update(cookies)

    def get(self, url, params=None):
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return response
        except requests.RequestException:
            return None

    def post(self, url, data=None):
        try:
            response = self.session.post(url, data=data, timeout=self.timeout)
            return response
        except requests.RequestException:
            return None
