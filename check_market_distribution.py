import os
from fmp import FinancialModelPrep, DATA_DIR

def list_files(data_dir):
    files = os.listdir(data_dir)
    files.remove('list.csv')
    file_names = [os.path.splitext(file)[0] for file in files]
    return file_names

def main():
    # List files in data dir
    files = list_files(DATA_DIR)
    fmp = FinancialModelPrep()

    market_counts = {}
    for sym in files:
        info = fmp.get_company_info(sym)
        exchange = info.exchangeShortName
        if exchange in market_counts:
            market_counts[exchange] += 1
        else:
            market_counts[exchange] = 1

    print(f'Total saved companies: {len(files)}')
    for key, val in market_counts.items():
        print(f'{key}\t{val}')

if __name__=='__main__':
    main()