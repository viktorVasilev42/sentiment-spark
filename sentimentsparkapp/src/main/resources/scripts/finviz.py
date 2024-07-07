from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import pandas as pd
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


def main(tickers):
    final_df = get_stock_data(tickers)
    analyze_sentiment(final_df, tickers)


def get_stock_data(tickers):
    finviz_url = 'https://finviz.com/quote.ashx?t='

    news_tables = {}
    for ticker in tickers:
        url = finviz_url + ticker

        req = Request(url=url, headers={'user-agent': 'my-app'})
        response = urlopen(req)

        html = BeautifulSoup(response, features='html.parser')
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table

    parsed_data = []
    date = ""

    for ticker, news_table in news_tables.items():

        for row in news_table.findAll('tr'):

            title = row.a.text
            date_data = trim_date_time(row.td.text).split(' ')

            if len(date_data) == 1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]

            if (date == 'Today'):
                date = pd.Timestamp.now().date()

            threshold_date = pd.Timestamp.now().normalize() - pd.Timedelta(days=3)
            if date and pd.Timestamp(date) >= threshold_date: #  type: ignore
                parsed_data.append([ticker, date, time, title])

    df = pd.DataFrame(parsed_data,
                      columns=['ticker', 'date', 'time', 'title']  # type: ignore
                      )
    return df
