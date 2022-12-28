import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "O1EL9WPC3DAV5OL9"  # Your key
NEWS_API_KEY = ""  # Your key
TWILIO_SID = ""  # Your SID
AUTH_TOKEN = ""  # Your token
TWILIO_NUMBER = ""  #Your number

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "interval": "60min",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stock_list = [value for (key, value) in stock_data.items()]
yesterday_price = stock_list[0]["4. close"]
day_before_yesterday_price = stock_list[1]["4. close"]

difference = float(yesterday_price) - float(day_before_yesterday_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
difference_percent = round((difference / float(yesterday_price)) * 100)

if abs(difference_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]

    articles = news_data[:3]

    formatted_articles = [f"{COMPANY_NAME}: {up_down}{difference_percent}%\n" \
                          f"Headline: {article['title']}. \nBrief: {article['description']}" for article in articles]

    client = Client(TWILIO_SID, AUTH_TOKEN)
    for article in articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_NUMBER,
            to=TWILIO_NUMBER,
        )


