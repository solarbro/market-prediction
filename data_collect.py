import argparse, os, sys
from fmp import FinancialModelPrep, DATA_DIR

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█', print_end='\r'):
    percent = ('{0:.1f}').format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

def collect(history):
    fmp = FinancialModelPrep()
    print(f'Found {len(fmp.symbols)} listed companies')
    print(fmp.symbols.info())
    # Need history for input and additional 10 years for ground truth as we want 
    # to predict the stock's growth over the next 3, 5, and 10 years
    total = len(fmp.symbols)
    current = 0
    count_failed = 0
    for sym in fmp.symbols.symbol:
        print_progress_bar(current, total, prefix='Progress:', suffix='Complete', length=50)
        try:
            df = fmp.get_financial_data(sym, history, 'quarter')
            df.to_csv(os.path.join(DATA_DIR, f'{sym}.csv'), sep=',')
        except:
            # print(f'Failed to accumulate data for {sym}')
            count_failed += 1
            # return
        current += 1
    print(f'Saved data for {total - count_failed} of {total} companies')

def main():
    parser = argparse.ArgumentParser('data_collect.py')
    parser.add_argument('history', type=int, default=[10], help='Number of years of historical data to download')
    args = parser.parse_args()
    collect(args.history)

if __name__=='__main__':
    main()