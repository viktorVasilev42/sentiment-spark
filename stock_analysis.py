import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import sys
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import mplcyberpunk

def trim_date_time(input_string):
    match = re.search(
        r'(?:Today )?(?:[A-Za-z]{3}-\d{2}-\d{2} )?\d{2}:\d{2}(?:AM|PM)',
        input_string
    )
    if match:
        return match.group()
    else:
        return ""

def compound_score(title):
    return vader.polarity_scores(title)['compound']

def fetch_stock_news(ticker):
    url = f'https://stockanalysis.com/stocks/{ticker}/'
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
    news_container = soup.select_one('div.flex.flex-col.space-y-3.overflow-x-hidden.bg-gray-200')

    if not news_container:
        print("Failed to find the news container.")
        return None

    news_items = news_container.find_all('div', class_='p-4')
    parsed_data = []



    for item in news_items:
        title_element = item.find('h3')
        title = title_element.text.strip() if title_element else 'No title'
        div_element = item.select('div')
        date_element=div_element[1]
        raw_date = date_element.text.strip() if date_element else 'No date'
        date = format_date(raw_date)
        time = '12:07PM'
        parsed_data.append((ticker, date, time, title))

    return parsed_data


from datetime import datetime, timedelta
import re


def format_date(raw_date):
    now = datetime.now()

    hours_pattern = re.compile(r'(\d+)\s+hours?\s+ago')
    days_pattern = re.compile(r'(\d+)\s+days?\s+ago')

    hours_match = hours_pattern.search(raw_date)
    if hours_match:
        hours = int(hours_match.group(1))
        date_obj = now - timedelta(hours=hours)
        return date_obj.strftime('%Y-%m-%d')

    days_match = days_pattern.search(raw_date)
    if days_match:
        days = int(days_match.group(1))
        date_obj = now - timedelta(days=days)
        return date_obj.strftime('%Y-%m-%d')

    return datetime.now().date()


print(format_date("19 hours ago - Investopedia"))
print(format_date("3 days ago - Reuters"))

n = len(sys.argv)
tickers = sys.argv[1:]
list_df = []

for ticker in tickers:
    data = fetch_stock_news(ticker)
    if data:
        df = pd.DataFrame(data, columns=['ticker', 'date', 'time', 'title'])
        list_df.append(df)

final_df = pd.concat(list_df, ignore_index=True)
print(final_df)

vader = SentimentIntensityAnalyzer()
final_df['compound'] = final_df['title'].apply(compound_score)
final_df['date'] = pd.to_datetime(final_df['date']).dt.date
final_df['time'] = pd.to_datetime(final_df['time'], format='%I:%M%p').dt.time

grouped_data = final_df.groupby(['ticker', 'date'])['compound'].mean().reset_index()
pivot_data = grouped_data.pivot(index='date', columns='ticker', values='compound')
print(pivot_data)

plt.style.use('cyberpunk')
pivot_data.plot(kind='bar', figsize=(12, 6), width=0.8)
plt.title('Sentiment Scores by Ticker and Date')
plt.xlabel('Date')
plt.ylabel('Average Sentiment Score')
plt.xticks(rotation=45)
plt.legend(title='Ticker')
plt.tight_layout()

for i in range(len(plt.gca().containers)):
    mplcyberpunk.add_bar_gradient(bars=plt.gca().containers[i])

plt.savefig('sentimentsparkapp/src/main/resources/plots/sentiment_analysis_bar.png', format='png', dpi=300)
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sentiment_data = final_df.copy()
sentiment_data['positive'] = sentiment_data['compound'].apply(lambda x: x if x > 0 else 0)
sentiment_data['negative'] = sentiment_data['compound'].apply(lambda x: x if x < 0 else 0)

pos_data = sentiment_data.groupby('ticker')['positive'].sum().reset_index()
neg_data = sentiment_data.groupby('ticker')['negative'].sum().reset_index()

pos_data.set_index('ticker', inplace=True)
neg_data.set_index('ticker', inplace=True)
combined_data = pos_data.join(neg_data, how='outer').fillna(0)

ax.barh(combined_data.index, combined_data['positive'], color='green', label='Positive')
ax.barh(combined_data.index, combined_data['negative'], color='red', label='Negative')

ax.legend()
ax.set_xlabel('Sentiment Score')
ax.set_title('Sentiment Analysis Population Pyramid')
ax.grid(True)

plt.savefig('sentimentsparkapp/src/main/resources/plots/sentiment_analysis_pyramid.png', format='png', dpi=300)
plt.show()