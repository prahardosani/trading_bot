import time
import requests
from alpha_vantage.timeseries import TimeSeries
from telegram.ext import Updater, CommandHandler #v13.7 seems to work (20.6 does not)
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

configure()
# Initialize the Alpha Vantage API client
alpha_vantage = TimeSeries(key=os.getenv('ALPHA_VANTAGE_API_KEY'), output_format='pandas')

# Function to send a message to the Telegram bot
def send_message(update, context, message):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Function to fetch real-time stock data and generate signals
def check_sma_strategy(update, context):
    try:
        symbol = 'AAPL'  # Example: Apple Inc. stock
        sma_period = 50   # Example: 50-period SMA

        # Fetch real-time stock data
        data, _ = alpha_vantage.get_quote_endpoint(symbol=symbol)

        # Extract the current price
        current_price = data['05. price']

        # Calculate the SMA
        historical_data, _ = alpha_vantage.get_intraday(symbol=symbol, interval='5min', outputsize='full')
        closes = historical_data['4. close'].astype(float)
        sma = closes.tail(sma_period).mean()

        # Send a buy or sell signal based on the strategy
        if current_price > sma:
            send_message(update, context, f'Buy Signal: {symbol} Price above {sma_period}-SMA')
        else:
            send_message(update, context, f'Sell Signal: {symbol} Price below {sma_period}-SMA')

    except Exception as e:
        print(f'Error: {str(e)}')

# Define a Telegram command to start the bot
def start(update, context):
    send_message(update, context, "SMA Bot is now active.")
    context.job_queue.run_repeating(check_sma_strategy, interval=600, first=0, context=update)

# Add the /start command to the bot
updater = Updater(token=os.getenv('TELEGRAM_API_TOKEN'), use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Start the Telegram bot
updater.start_polling()
updater.idle()