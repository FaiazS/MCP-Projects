import os

import random

from polygon import RESTClient

from datetime import datetime, timezone

from dotenv import load_dotenv

from functools import lru_cache

from equity_database import update_equity_market_data, get_equity_market_data

load_dotenv(override=True)

polygon_api_key =  os.getenv('POLYGON_API_KEY')

polygon_client = RESTClient(api_key = polygon_api_key)

polygon_free = True

def is_equity_market_open() -> bool:

    equity_market_status = polygon_client.get_market_status()

    return equity_market_status.market == 'open'

def get_all_equity_prices_eod() -> dict[str, float]:

    probe = polygon_client.get_previous_close_agg('SPY')[0]

    last_close = datetime.fromtimestamp(probe.timestamp / 1000, tz = timezone.utc).date()

    equity_prices = polygon_client.get_grouped_daily_aggs(last_close, adjusted=True, include_otc= False)

    return {price.ticker: price.close for price in equity_prices}

@lru_cache(maxsize=2)
def get_equity_market_info_for_prior_date(current_date):

 current_equity_market_info = get_equity_market_data(date = current_date)

 if not current_equity_market_info:

    current_equity_market_info = get_all_equity_prices_eod()

    update_equity_market_data(date = current_date, equity_market_data = current_equity_market_info)

 return current_equity_market_info


def get_equity_price_eod(company_symbol) -> float:
   
   current_day = datetime.now().strftime('%d/%m/%Y')

   equity_info = get_equity_market_info_for_prior_date(current_date = current_day)

   return equity_info.get(company_symbol, 0.0)


def get_min_equity_price(company_symbol):
   
   result = polygon_client.get_snapshot_ticker('stocks', company_symbol)

   return result.min.close or result.prev_day

def get_equity_price(company_symbol) -> float:
   
   if not polygon_free:
      
      return get_min_equity_price(company_symbol=company_symbol)
   
   else:
      
      return get_equity_price_eod(company_symbol=company_symbol)


def get_company_equity_stock_price(company_symbol) -> float:
   
   if polygon_api_key:
      
      try:
         
        return get_equity_price(company_symbol=company_symbol)

      except Exception as e:
         
         print(f"Could not invoke Polygon API due to exception :{e}; thus using a random value")

      return float(random.randint(1, 250))














