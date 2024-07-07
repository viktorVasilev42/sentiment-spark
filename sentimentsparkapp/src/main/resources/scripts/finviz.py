from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import sys


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


n = len(sys.argv)
tickers = sys.argv[1:]
finviz_url = 'https://finviz.com/quote.ashx?t='
# tickers = ['AMZN', 'GOOG',]
# tickers = ['META', 'AMZN', 'GOOG', 'NFLX']

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

        threshold_date = pd.Timestamp.now().normalize() - pd.Timedelta(days=4)
        if date and pd.Timestamp(date) >= threshold_date:
            parsed_data.append([ticker, date, time, title])

df = pd.DataFrame(parsed_data,
                  columns=['ticker', 'date', 'time', 'title']  # type: ignore
                  )

vader = SentimentIntensityAnalyzer()
df['compound'] = df['title'].apply(compound_score)

df['date'] = pd.to_datetime(df.date).dt.date
df['time'] = pd.to_datetime(df.time, format='%I:%M%p').dt.time

grouped_data = df.groupby(['ticker', 'date'])['compound'].mean().reset_index()

# Pivot the data for easier plotting
pivot_data = grouped_data.pivot(index='date', columns='ticker', values='compound')
print(pivot_data)

# Plotting the bar chart
plt.style.use('cyberpunk')
pivot_data.plot(kind='bar', figsize=(18, 6), width=0.7)
plt.title('Sentiment Scores by Ticker and Date')
plt.xlabel('Date')
plt.ylabel('Average Sentiment Score')
plt.xticks(rotation=45)
plt.legend(title='Ticker')
plt.tight_layout()

for i in range(0, len(tickers)):
    mplcyberpunk.add_bar_gradient(bars=plt.gca().containers[i])

# Save the bar chart
plt.savefig('../plots/sentiment_analysis_bar.png', format='png', dpi=300)
plt.savefig('../../../src/main/resources/plots/sentiment_analysis_bar.png', format='png', dpi=300)

# Show the bar chart (optional)

# Plotting the population pyramid chart
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate positive and negative sentiment scores
sentiment_data = df.copy()
sentiment_data['positive'] = sentiment_data['compound'].apply(lambda x: x if x > 0 else 0)
sentiment_data['negative'] = sentiment_data['compound'].apply(lambda x: x if x < 0 else 0)

# Group data by ticker for positive and negative sentiment
pos_data = sentiment_data.groupby('ticker')['positive'].sum().reset_index()
neg_data = sentiment_data.groupby('ticker')['negative'].sum().reset_index()

# Combine positive and negative data for plotting
pos_data.set_index('ticker', inplace=True)
neg_data.set_index('ticker', inplace=True)
combined_data = pos_data.join(neg_data, how='outer').fillna(0)

# Plot positive sentiment bars
ax.barh(combined_data.index, combined_data['positive'], color='green', label='Positive')

# Plot negative sentiment bars
ax.barh(combined_data.index, combined_data['negative'], color='red', label='Negative')

# Adding the legend
ax.legend()

# Adding labels
ax.set_xlabel('Sentiment Score')
ax.set_title('Sentiment Analysis Population Pyramid')

# Adding grid
ax.grid(True)

# Save the population pyramid plot
plt.savefig('../plots/sentiment_analysis_pyramid.png', format='png', dpi=300)
plt.savefig('../../../src/main/resources/plots/sentiment_analysis_pyramid.png', format='png', dpi=300)
