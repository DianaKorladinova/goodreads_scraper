import requests
import threading
from bs4 import BeautifulSoup
from scraper_shelves import scrape_shelf

response = requests.get("https://www.goodreads.com/")
soup = BeautifulSoup(response.content, 'html.parser')
genre_box = soup.find('div', class_='u-defaultType')
list_columns = list(genre_box.children)


def not_empty(el):
    return el != '\n'


list_columns = list(filter(not_empty, list_columns))
list_genres = []

for column in list_columns:
    for kid in list(column.children):
        list_genres.append(kid)


def valid(genre):
    if genre != '\n':
        if genre.name != 'br':
            return True
    return False


list_genres = list(filter(valid, list_genres))
list_genres.pop(-1)


def link(genre):
    return "https://www.goodreads.com/shelf/show/" + genre['href'].split('/')[-1]


list_genres = list(map(link, list_genres))

for genre in list_genres:
    scrape_shelf(genre)
