import requests
import os
import io
# import json
import pandas as pd

ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

class FinancialModelPrep:
    def __init__(self):
        # Load API key
        with open(os.path.join(ROOT_DIR, 'apikey.txt'), 'rt') as F:
            self._apikey = F.readline()

        # Get list of symbols
        list_file_path = os.path.join(DATA_DIR, 'list.csv')
        if os.path.exists(list_file_path):
            print('Loading list of symbols from file')
            self.symbols = pd.read_csv(list_file_path)
        else:
            print('Fetching list of symbols from FMP')
            url = f'https://financialmodelingprep.com/api/v3/stock/list?apikey={self._apikey}'
            response = requests.get(url)
            decoded_content = response.content.decode('utf-8')
            self.symbols = pd.read_json(io.StringIO(decoded_content))
            # Filter entries that are not stocks
            self.symbols = self.symbols.drop(self.symbols[self.symbols.type != 'stock'].index)
            # Save list for future use
            self.symbols.to_csv(list_file_path, sep=',')
        # Map symbols to names for easy access
        self.symbol_to_name = self.symbols.set_index('symbol')['name'].to_dict()

    def get_data(self, symbol):
        # Income statement
        url = f'https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&apikey={self._apikey}'
        url = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement-as-reported/{symbol}?period=annual&limit=100&apikey={self._apikey}'
        url = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?period=annual&apikey={self._apikey}&limit=20'
        response = requests.get(url)
        decoded_content = response.content.decode('utf-8')
        print(decoded_content)
        # Balance sheet
        # Cash flow

    def get_financial_data(self, symbol, years, period):
        stock_name = self.symbol_to_name[symbol]
        print(f'Fetching {period} reports for {stock_name} for {years} years')
        # Get report date and accumulate all fields from all potentially required categories
        # Return time series as a DataFrame 