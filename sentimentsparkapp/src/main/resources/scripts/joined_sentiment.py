import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import mplcyberpunk

def compound_score(title):
    vader = SentimentIntensityAnalyzer()
    return vader.polarity_scores(title)['compound']

def per_company_plot(df, tickers):
    vader = SentimentIntensityAnalyzer()
    df['compound'] = df['title'].apply(compound_score)
    df['date'] = pd.to_datetime(df.date).dt.date
    df['time'] = pd.to_datetime(df.time, format='%I:%M%p').dt.time

    grouped_data = df.groupby(['ticker', 'date'])['compound'].mean().reset_index()

    # Ensure we have enough colors for the number of tickers
    num_tickers = len(tickers)
    colors = plt.cm.viridis(range(num_tickers))

    # Plot for each ticker
    for i, ticker in enumerate(tickers):
        ticker_data = grouped_data[grouped_data['ticker'] == ticker]

        if ticker_data.empty:
            print(f"No data available for ticker {ticker}. Skipping plot.")
            continue

        plt.figure(figsize=(12, 6))

        plt.plot(ticker_data['date'], ticker_data['compound'], marker='o', linestyle='-', color=colors[i], linewidth=2, label=ticker)

        plt.fill_between(ticker_data['date'], ticker_data['compound'], where=ticker_data['compound'] >= 0,
                         color='green', alpha=0.3, interpolate=True, label='Above 0')


        plt.fill_between(ticker_data['date'], ticker_data['compound'], where=ticker_data['compound'] < 0,
                         color='red', alpha=0.3, interpolate=True, label='Below 0')

        plt.title(f'Sentiment Scores for {ticker}')
        plt.xlabel('Date')
        plt.ylabel('Average Sentiment Score')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.style.use('cyberpunk')

        # Save the plot
        plt.savefig(f'../plots/subplots/sentiment_analysis_{ticker}_line.png', format='png', dpi=300)
        plt.savefig(f'../../../src/main/resources/plots/subplots/sentiment_analysis_{ticker}_line.png', format='png', dpi=300)
        plt.close()
