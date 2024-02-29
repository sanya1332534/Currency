import csv
import random
from time import sleep
import sqlite3

import requests
from bs4 import BeautifulSoup


def random_sleep():
    sleep(random.randint(2, 4))


def get_page_content(page: int, page_size: int = 100):
    base_url = 'https://auto.ria.com/uk/search/'
    query_params = {
        'indexName': 'auto,order_auto,newauto_search',
        'categories.main.id': '1',
        'country.import.usa.not': '-1',
        'price.currency': '1',
        'abroad.not': '0',
        'custom.not': '1',
        'page': page,
        'size': page_size,
    }

    response = requests.get(base_url, params=query_params)
    response.raise_for_status()
    return response.text


def get_car_details(url_suffix: str):
    base_url = 'https://auto.ria.com/uk'
    full_url = f"{base_url}{url_suffix}"

    response = requests.get(full_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    price_value = soup.find('div', class_='price_value')
    price = price_value.find('strong').text.replace(' ', '') if price_value else 'Без цiни'
    return price


class CSVWriter:
    def __init__(self, file_name: str, headers: list):
        self.file_name = file_name

        with open(self.file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    def write_data(self, data):
        with open(self.file_name, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)


class SQLiteWriter:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id TEXT PRIMARY KEY,
                mark TEXT,
                model TEXT,
                year TEXT,
                link TEXT,
                price TEXT
            )
        ''')
        self.conn.commit()

    def write_data(self, data):
        self.cursor.execute('''
                INSERT INTO cars (id, mark, model, year, link, price) 
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    mark=excluded.mark,
                    model=excluded.model,
                    year=excluded.year,
                    link=excluded.link,
                    price=excluded.price
            ''', data)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


def main():
    page = 0
    headers = ['id', 'mark', 'model', 'year', 'link', 'price']

    writers = (
        CSVWriter('cars.csv', headers),
        SQLiteWriter('cars.db'),
    )

    while True:
        random_sleep()
        print(f"Processing page {page}!")

        page_content = get_page_content(page)

        soup = BeautifulSoup(page_content, 'html.parser')
        search_results = soup.find('div', id="searchResults")
        ticket_items = search_results.find_all("section", class_="ticket-item")

        if not ticket_items:
            print(f"No more items on page {page}!")
            break

        for ticket_item in ticket_items:
            car_details = ticket_item.find("div", class_="hide")
            car_id = car_details['data-id']
            car_mark_details = car_details['data-mark-name']
            car_model_name = car_details['data-model-name']
            car_year = car_details['data-year']

            car_link_to_view = car_details['data-link-to-view']
            car_price = get_car_details(car_link_to_view)

            data = [car_id, car_mark_details, car_model_name, car_year, car_link_to_view, car_price]

            for writer in writers:
                writer.write_data(data)

        page += 1


if __name__ == '__main__':
    main()
