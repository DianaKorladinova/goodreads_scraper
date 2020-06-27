import re
import requests
from bs4 import BeautifulSoup
from database import create_connection, insert_stuff

cookie = 'ccsid=327-1044404-4063019; locale=en; _session_id2=8da738aee173a8f86c05ed8c23992e57; ' \
         'mobvious.device_type=desktop; blocking_sign_in_interstitial=true; ' \
         'u=Oie5j2C6RF4qeIrXp3xhb2sOc0QsHyTNMaNqPVN5hp51RU_o; p=r7hNBJAOghw10m5-LKKUnZSXX_No8JJ2Bnrnl92sti2W840X '


def scrape_shelf(shelf_link):
    genre = shelf_link.split('/')[-1]
    connection = create_connection()
    page = 1
    response = requests.get(shelf_link + f"?page={page}", headers={
        'Cookie': cookie}, )
    while response.status_code != 404:
        page += 1
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.select("div.leftContainer div.elementList")

        for book in books:
            regex = r"\d\.\d\d?"
            regex2 = r" ((\d{1,3},)?)*\d{1,3} "
            book_obj = {}
            item = book.select('div.left')[0]
            ratings = item.findChildren('span', class_='greyText smallText')[0].getText()
            book_obj['avg rate'] = re.search(regex, ratings).group()
            book_obj['number of ratings'] = re.search(regex2, ratings).group().replace(',', ' ')
            book_obj['title'] = item.findChildren('a', class_='bookTitle')[0].getText()
            book_obj['author'] = item.findChildren('a', class_='authorName')[0].getText()
            insert_stuff(book_obj['title'], book_obj['author'], genre, book_obj['avg rate'],
                         book_obj['number of ratings'],
                         'tbd', connection)
        response = requests.get(shelf_link + f"?page={page}", headers={
            'Cookie': cookie}, )
    connection.close()
