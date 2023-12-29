import argparse
from fmp import FinancialModelPrep

def query_url(symbol, function, apikey):
    return f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}&RANGE=2013-07-01&RANGE=2023-08-31'

def collect(num_samples, history):
    fmp = FinancialModelPrep()
    print(f'Found {len(fmp.symbols)} listed symbols')
    print(fmp.symbols.head(num_samples))
    print(fmp.symbols.info())
    # Need history for input and additional 10 years for ground truth as we want 
    # to predict the stock's growth over the next 3, 5, and 10 years
    num_required_years = history + 10 
    for sym in fmp.symbols.symbol:
        fmp.get_financial_data(sym, num_required_years, 'quarter')

def main():
    parser = argparse.ArgumentParser('data_collect.py')
    parser.add_argument('samples', nargs=1, type=int, help='Number of training samples to gather')
    parser.add_argument('--history', nargs=1, type=int, default=[10], help='Number of years of historical data to use for each input sample')
    args = parser.parse_args()
    collect(args.samples[0], args.history[0])

if __name__=='__main__':
    main()