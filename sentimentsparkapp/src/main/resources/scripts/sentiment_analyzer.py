import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import re
import sys
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import mplcyberpunk


def compound_score(title):
    vader = SentimentIntensityAnalyzer()
    return vader.polarity_scores(title)['compound']


def analyze_sentiment(df, tickers):
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
    pivot_data.plot(kind='bar', figsize=(12, 6), width=0.8)
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