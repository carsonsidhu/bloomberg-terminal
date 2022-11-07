import requests
from twilio.rest import Client

account_sid ='AC82adf5e7798ccb01f38cf440fdf17274'
auth_token = "4de115328241d28ae7459db9f6a6d7db"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": "BBQ0DII7RWAB4JTZ"
}

news_params = {
    "q": "tesla",
    "apiKey": "5d349b2661d54eed9625b9082e8e864e"
}

response_stocks = requests.get(STOCK_ENDPOINT, params=stock_params)
response_stocks.raise_for_status()
stock_data = response_stocks.json()
# print(stock_data["Time Series (Daily)"])
stock_data_daily = stock_data["Time Series (Daily)"]
# print(stock_data_daily["2022-10-17"]["4. close"])

closing_prices = []

for day in stock_data_daily:
    closing_prices.append(stock_data_daily[day]["4. close"])

# print(closing_prices)

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
yesterday_close = closing_prices[0]

#Get the day before yesterday's closing stock price
day_before_close = closing_prices[1]

#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
pos_difference = abs(float(yesterday_close) - float(day_before_close))

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent_diff = float(yesterday_close)/float(day_before_close)
if percent_diff > 1:
    percent_diff = (percent_diff - 1) * 100
else:
    percent_diff = (1 - percent_diff) * 100

#If TODO4 percentage is greater than 5 then print("Get News").
if percent_diff > 5:
    print("Get news")

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
response_news = requests.get(NEWS_ENDPOINT, params=news_params)
response_news.raise_for_status()
news_data = response_news.json()["articles"]
# print(news_data)

all_titles = []
all_articles = []
for article in news_data:
    all_titles.append(article["title"])
    all_articles.append(article["description"])

#Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

recent_titles = all_titles[:3]
recent_articles = all_articles[:3]

print(recent_titles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#Create a new list of the first 3 article's headline and description using list comprehension.

formatted_articles = []
for i in range(len(recent_articles)):
    formatted_articles.append(f"Headline: {recent_titles[i]}\nBrief: {recent_articles[i]}")

#Send each article as a separate message via Twilio.

client = Client(account_sid, auth_token)

for article in formatted_articles:
    message = client.messages.create(
        messaging_service_sid='MG09718d77e02ecf560302a7e8a6c86247',
        body=article,
        from_='+14057844981',
        to='+16048287821'
    )

    print(message.status)
