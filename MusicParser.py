import requests
from bs4 import BeautifulSoup

URL = 'https://hotmo.org/songs/top-today'
HEADERS = {}


def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req


def content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='track__info-l', limit=22)
    list_songs = []
    list_desc = []
    complete = {}
    for item in items:
        list_songs.append(item.find('div', class_='track__title').get_text(strip=True))
        list_desc.append(item.find('div', class_='track__desc').get_text())

    for i in range(len(list_songs)):
        complete[list_songs[i]] = list_desc[i]
    return complete


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        c = content(html.text)
    return c

