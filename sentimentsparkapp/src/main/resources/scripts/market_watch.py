import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import re
import sys
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import mplcyberpunk
from sentiment_analyzer import analyze_sentiment


def trim_date_time(input_string):
    match = re.search(
        r'(?:Today )?(?:[A-Za-z]{3}-\d{2}-\d{2} )?\d{2}:\d{2}(?:AM|PM)',
        input_string
    )
    if match:
        return match.group()
    else:
        return ""



def fetch_marketwatch_news(ticker):
    url = f'https://www.marketwatch.com/investing/stock/{ticker}?mod=mw_quote_tab'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    news_container = soup.select_one(
        '#maincontent > div.region.region--primary > div.column.column--primary > div:nth-child(1) > mw-tabs > div.element__body.j-tabPanes > div.tab__pane.is-active.j-tabPane > mw-scrollable-news-v2 > div > div')

    if not news_container:
        print("Failed to find the news container.")
        return None

    news_items = news_container.find_all('div', class_='article__content')
    parsed_data = []

    for item in news_items:
        title_element = item.find('a', class_='link')
        title = title_element.text.strip() if title_element else 'No title'
        date_element = item.select_one('span.article__timestamp')
        raw_date = date_element.text.strip() if date_element else 'No date'
        date = format_date(raw_date)
        time = '12:07PM'
        parsed_data.append((ticker, date, time, title))

    return parsed_data


def format_date(raw_date):
    try:
        date_str = re.split(r'\s+at\s+', raw_date)[0]
        date_obj = datetime.strptime(date_str, '%b. %d, %Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return 'Invalid date'


def main(tickers):

    list_df = []

    for ticker in tickers:
        data = fetch_marketwatch_news(ticker)
        if data:
            df = pd.DataFrame(data, columns=['ticker', 'date', 'time', 'title'])
            list_df.append(df)

    if not list_df:
        print("No data to analyze.")
        return

    final_df = pd.concat(list_df, ignore_index=True)
    analyze_sentiment(final_df, tickers)


if __name__ == '__main__':
    main()
