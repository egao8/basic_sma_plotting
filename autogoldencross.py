import yfinance as yf
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def fetch_sp500_tickers():
    """Fetch the list of S&P 500 tickers from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_table = pd.read_html(url, header=0)
    tickers = sp500_table[0]["Symbol"].tolist()
    return tickers


def fetch_stock_data(ticker, period="5y"):
    """Fetch stock data for a given ticker."""
    try:
        stock_data = yf.download(ticker, period=period, progress=False)
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()


def calculate_sma(data, window):
    """Calculate the Simple Moving Average (SMA)."""
    return data['Close'].rolling(window=window).mean()


def identify_golden_cross(data):
    """Identify golden crosses in the stock data."""
    data['50_SMA'] = calculate_sma(data, 50)
    data['200_SMA'] = calculate_sma(data, 200)
    data['Golden_Cross'] = (data['50_SMA'] > data['200_SMA']) & (data['50_SMA'].shift(1) <= data['200_SMA'].shift(1))
    return data[data['Golden_Cross']]


def save_to_excel(results, filename="golden_crosses.xlsx"):
    """Save the results to an Excel file."""
    df = pd.DataFrame(results)
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")


def send_email(to_email, subject, body, attachment):
    """Send an email with an attachment."""
    from_email = "eddiegao8@gmail.com" # you have to change this for your own email 
    password = "zbxi uusj qtob nuqf" # then, generate an app password (not ur gmail password)

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))


    with open(attachment, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={attachment}")
    msg.attach(part)


    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

    print(f"Email sent to {to_email}")


def main():
    tickers = fetch_sp500_tickers()
    results = []

    for ticker in tickers:
        print(f"Processing {ticker}...")
        stock_data = fetch_stock_data(ticker)

        if stock_data.empty:
            continue

        golden_crosses = identify_golden_cross(stock_data)
        for index, row in golden_crosses.iterrows():
            results.append({
                "Ticker": ticker,
                "Date": index.strftime("%Y-%m-%d"),
                "Price": row["Close"]
            })

    filename = "golden_crosses.xlsx"
    save_to_excel(results, filename)

    to_email = "eddiegao8@gmail.com" # replace with ur email - this is my personal
    subject = "Golden Cross Analysis for S&P 500"
    body = "Please find attached the Golden Cross analysis for S&P 500 stocks."
    send_email(to_email, subject, body, filename)


if __name__ == "__main__":
    main()
