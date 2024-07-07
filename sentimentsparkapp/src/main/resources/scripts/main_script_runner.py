import sys
from stock_analysis import fetch_stock_news as stocknews_data
from market_watch import fetch_marketwatch_news as marketwatch_data
from finviz import get_stock_data as finviz_data
from stock_analysis import main as stock_analysis
from market_watch import main as market_watch
from finviz import main as finviz
import pandas as pd
from joined_sentiment import per_company_plot

def main():
    if len(sys.argv) < 2:
        print("Please provide at least one ticker symbol.")
        sys.exit(1)

    scrapper = sys.argv[1]
    tickers = sys.argv[2:]
    data_dict = {
        'stock_analysis': stocknews_data,
        'market_watch': marketwatch_data,
        'finviz': finviz_data
    }

    function = data_dict.get(scrapper)
    if scrapper == "finviz":
        final_df = function(tickers)
        finviz(tickers)
        print(final_df)
    else:
        list_df = []
        for ticker in tickers:
            data = function(ticker)
            if data:
                df = pd.DataFrame(data, columns=['ticker', 'date', 'time', 'title'])
                list_df.append(df)
        final_df = pd.concat(list_df, ignore_index=True)
        print(final_df)
        if scrapper == "market_watch":
            market_watch(tickers)
        else:
            stock_analysis(tickers)

    per_company_plot(final_df, tickers)

if __name__ == '__main__':
    main()
