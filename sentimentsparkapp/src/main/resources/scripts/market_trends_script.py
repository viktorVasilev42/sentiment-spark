import requests
from bs4 import BeautifulSoup
import csv
import os


def fetch_element_content(url, element_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to load page, status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    element = soup.find(id=element_id)
    parsed_data = []
    news_items = element.find_all('tr')
    for news_item in news_items:
        name = news_item.find('a')
        value = news_item.findAll('td')
        value = value[1]
        percent_change = news_item.find('span')
        parsed_data.append((name.text, value.text, percent_change.text))

    return parsed_data


def write_files_to_csv(parsed_data):
    filepath_1 = "../market_data/stock_data.csv"
    filepath_2 = "../../../../target/classes/market_data/stock_data.csv"

    os.makedirs(os.path.dirname(filepath_1), exist_ok=True)
    os.makedirs(os.path.dirname(filepath_2), exist_ok=True)
    with open(filepath_1, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Value', 'Percent Change'])
        writer.writerows(parsed_data)

    with open(filepath_2, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Value', 'Percent Change'])
        writer.writerows(parsed_data)


def main():
    url = 'https://finviz.com/'
    element_id = 'js-signals_1'
    content = fetch_element_content(url, element_id)
    write_files_to_csv(content)


if __name__ == "__main__":
    main()
