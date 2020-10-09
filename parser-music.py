import requests
from bs4 import BeautifulSoup


class ParseMusic:
    def __init__(self):
        self.URL = 'https://hotmo.org/songs/top-today'
        self.HEADERS = {}

    def get_html(self, url):
        req = requests.get(url, headers=self.HEADERS)
        return req

    def content(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('a', class_='track__info-l')
        list_songs = []
        list_desc = []
        complete = {}
        for item in items:
            list_songs.append(item.find('div', class_='track__title').get_text(strip=True))
            list_desc.append(item.find('div', class_='track__desc') .get_text())

        for i in range(len(list_songs)):
            complete[list_songs[i]] = list_desc[i]
        return complete

    def parse(self):
        html = self.get_html(self.URL)
        if html.status_code == 200:
            c = self.content(html.text)
        return с
