import sys
# append the path of the parent directory
sys.path.append("./")

import yfinance as yf
import pandas as pd
import numpy as np

import json
from datetime import datetime, timedelta, time, timezone
from dotenv import load_dotenv
import time as t

load_dotenv()

def send_to_kafka(producer, topic, key, partition, message):
    print("topic",topic)
    try:
        if not topic or not isinstance(topic, str):
            raise ValueError("Invalid Kafka topic provided.")
        print("Sent to Kafka:", message)
        producer.produce(topic, key=key, partition=partition, value=json.dumps(message).encode("utf-8"))
        producer.flush()
    except Exception as e:
        print(f"Error sending message to Kafka: {e}")

def retrieve_historical_data(producer, stock_symbol, kafka_topic, logger):
    # Define the date range for historical data
    stock_symbols = stock_symbol.split(",") if stock_symbol else []
    print("stock_symbols: ",stock_symbols)
    if not stock_symbols:
        logger.error(f"No stock symbols provided in the environment variable.")
        exit(1)
    
    # Fetch historical data
    end_date = datetime.now()
    start_date = (yf.Ticker(stock_symbols[0]).history(period="1d").index[0]).strftime('%Y-%m-%d')
    for symbol_index, stock_symbol in enumerate(stock_symbols):
        print("symbol: ",symbol_index)
        print("symbol: ",stock_symbol)
        historical_data = yf.download(stock_symbol, start=start_date, end=end_date, interval="2m", prepost=True)
        
        # Reset the index to ensure 'Datetime' is treated as a column and not part of multi-index
        historical_data.reset_index(inplace=True)

        print("cols",historical_data.columns[1][0])
        
        # Flatten the multi-index columns
        historical_data.columns = [col[0] for col in historical_data.columns]
        
        # Log the first few rows of historical data to inspect it
        logger.info(f"Fetched historical data for {stock_symbol}:\n{historical_data.head()}")

        # Handle empty DataFrame
        if historical_data.empty:
            logger.error(f"No historical data fetched for {stock_symbol}.")
            continue

        
        
        # Log the data after replacement for inspection
        logger.info(f"Processed historical data for {stock_symbol}:\n{historical_data.head()}")

        # Convert and send historical data to Kafka
        for index, row in historical_data.iterrows():
            historical_data_point = {
                'stock': stock_symbol,
                'date': row['Datetime'].isoformat(),  # Use 'Datetime' column after reset_index
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            }
            logger.info(f"Sending to Kafka: {historical_data_point}")
            if historical_data_point:  # Ensure the data point is not empty
                send_to_kafka(producer, kafka_topic, stock_symbol, symbol_index, historical_data_point)
            else:
                logger.warning(f"Skipping Kafka send for {stock_symbol} due to empty data point.")


def retrieve_real_time_data(producer, stock_symbol, kafka_topic, logger):
    # Define the stock symbol for real-time data
    logger.debug(f"Starting the data retrieval process for stock symbols: {stock_symbol}")
    retrieve_historical_data(producer, stock_symbol, kafka_topic, logger)
    stock_symbols = stock_symbol.split(",") if stock_symbol else []
    if not stock_symbols:
        logger.error(f"No stock symbols provided in the environment variable.")
        exit(1)
    
    logger.debug(f"Stock symbols to retrieve: {stock_symbols}")
    
    while True:
        # Fetch real-time data for the last 1 minute
        current_time = datetime.now()
        logger.debug(f"Current time: {current_time.isoformat()}")
        
        is_market_open_bool = is_stock_market_open(current_time)
        logger.debug(f"Is the market open? {is_market_open_bool}")
        
        if is_market_open_bool:
            end_time = datetime.now()
            start_time = end_time - timedelta(days=1)
            logger.debug(f"Market is open. Retrieving data from {start_time.isoformat()} to {end_time.isoformat()}")
            
            for symbol_index, stock_symbol in enumerate(stock_symbols):
                logger.debug(f"Retrieving data for symbol: {stock_symbol}, index: {symbol_index}")
                
                try:
                    real_time_data = yf.download(stock_symbol, start=start_time, end=end_time, interval="2m")
                    
                    if not real_time_data.empty:
                        # Convert and send the latest real-time data point to Kafka
                        latest_data_point = real_time_data.iloc[-1]
                        real_time_data_point = {
                            'stock': stock_symbol,
                            'date': datetime.now(),
                            'open': latest_data_point['Open'],
                            'high': latest_data_point['High'],
                            'low': latest_data_point['Low'],
                            'close': latest_data_point['Close'],
                            'volume': latest_data_point['Volume']
                        }
                        logger.debug(f"Latest data for {stock_symbol}: {real_time_data_point}")
                        send_to_kafka(producer, kafka_topic, stock_symbol, symbol_index, real_time_data_point)
                        logger.info(f"Stock value retrieved and pushed to Kafka topic {kafka_topic} for {stock_symbol}")
                    else:
                        logger.warning(f"No real-time data returned for {stock_symbol}")
                
                except Exception as e:
                    logger.error(f"Error retrieving real-time data for {stock_symbol}: {e}")
        
        else:
            logger.debug(f"Market is closed. Sending null data.")
            
            for symbol_index, stock_symbol in enumerate(stock_symbols):
                null_data_point = {
                    'stock': stock_symbol,
                    'date': current_time.isoformat(),
                    'open': None,
                    'high': None,
                    'low': None,
                    'close': None,
                    'volume': None
                }
                #send_to_kafka(producer, kafka_topic, stock_symbol, symbol_index, null_data_point)
                logger.info(f"Null data sent to Kafka topic {kafka_topic} for {stock_symbol}")

        t.sleep(3)



def is_stock_market_open(current_datetime=None):
    # If no datetime is provided, use the current datetime
    if current_datetime is None:
        current_datetime = datetime.now()

    # Define NYSE trading hours in Eastern Time Zone
    market_open_time = time(9, 30)
    market_close_time = time(16, 0)

    # Convert current_datetime to Eastern Time Zone
    current_time_et = current_datetime.astimezone(timezone(timedelta(hours=-4)))  # EDT (UTC-4)

    # Check if it's a weekday and within trading hours
    if current_time_et.weekday() < 5 and market_open_time <= current_time_et.time() < market_close_time:
        return True
    else:
        return False


