import requests
from bs4 import BeautifulSoup


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

    news_items = element.find_all('tr')
    for news_item in news_items:
        print(news_item)
        print("\n")

    # if element:
    #     return element.get_text(strip=True)
    # else:
    #     raise Exception(f"Element with ID {element_id} not found")


def main():
    url = 'https://finviz.com/'
    element_id = 'js-signals_1'

    try:
        content = fetch_element_content(url, element_id)
        print("Element content:", content)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
