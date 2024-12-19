import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt




def fetch_stock_data(ticker, period="5y"):
    print(f"Fetching data for {ticker}...")
    stock_data = yf.download(ticker, period=period)
    return stock_data



def calculate_sma(data, window):
    return data['Close'].rolling(window=window).mean()

def identify_golden_cross(data):
    data['50_SMA'] = calculate_sma(data, 50)
    data['200_SMA'] = calculate_sma(data, 200)
    data['Golden_Cross'] = (data['50_SMA'] > data['200_SMA']) & (data['50_SMA'].shift(1) <= data['200_SMA'].shift(1)) # identifying where SMA is
    return data

def plot_stock_data(data, ticker):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label="Close Price", alpha=0.7)
    plt.plot(data['50_SMA'], label="50-Day SMA", linestyle='--', alpha=0.8) 
    plt.plot(data['200_SMA'], label="200-Day SMA", linestyle='--', alpha=0.8)

    # this is where golden cross is plotted
    golden_cross_points = data[data['Golden_Cross']]
    plt.scatter(golden_cross_points.index, golden_cross_points['Close'], color='gold', label="Golden Cross", marker='o')

    plt.title(f"{ticker} - Moving Averages and Golden Cross")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    while True:
        ticker = input("Enter the stock ticker (or 'exit' to quit): ").upper()
        if ticker == "EXIT":
            print("Exiting the program.")
            break

        try:
            stock_data = fetch_stock_data(ticker)

            if stock_data.empty:
                print("No data found for the given ticker. Please try again.")
                continue

            analyzed_data = identify_golden_cross(stock_data)

            plot_stock_data(analyzed_data, ticker)

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
