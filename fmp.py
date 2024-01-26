import requests
import os
import io
import json
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

    def get_financial_data(self, symbol, years, period):
        # stock_name = self.symbol_to_name[symbol]
        # print(f'Fetching {period} reports for {stock_name} for {years} years')
        # Get report date and accumulate all fields from all potentially required categories
        limit = years
        if period=='quarter':
            limit *= 4
        response_is = self.make_query('income-statement', symbol, period, limit)
        response_bs = self.make_query('balance-sheet-statement', symbol, period, limit)
        response_cf = self.make_query('cash-flow-statement', symbol, period, limit)
        # Drop entry if it returns less than the required number of historical reports 
        dates = [statement['date'] for statement in response_is]
        # if len(dates) < limit:
            # return None
        # Accumulate responses into a time-series
        return _make_dataframe(response_is, response_bs, response_cf)

    def make_query(self, func, symbol, period, limit):
        url = f'https://financialmodelingprep.com/api/v3/{func}/{symbol}?period={period}&limit={limit}&apikey={self._apikey}'
        response = requests.get(url)
        decoded_content = response.content.decode('utf-8')
        return json.loads(decoded_content)

    def get_company_info(self, symbol):
        result_df = self.symbols[self.symbols['symbol'] == symbol]
        return result_df.iloc[0]

def _make_dataframe(income, balance_sheet, cash_flow):
    # Get list of dates
    dates = [statement['calendarYear']+statement['period'] for statement in income]
    dates.extend([statement['calendarYear']+statement['period'] for statement in balance_sheet])
    dates.extend([statement['calendarYear']+statement['period'] for statement in cash_flow])
    unique_dates = set(dates)
    dates = sorted(list(unique_dates))
    # print(dates)
    # Initialize entries
    num_entries = len(dates)
    entries = {
        'timestamp': [None] * num_entries,
        'reportedCurrency': [None] * num_entries,
        # Income statement
        'revenue': [None] * num_entries,
        'costOfRevenue': [None] * num_entries,
        'grossProfit': [None] * num_entries,
        'grossProfitRatio': [None] * num_entries,
        'researchAndDevelopmentExpenses': [None] * num_entries,
        'generalAndAdministrativeExpenses': [None] * num_entries,
        'sellingAndMarketingExpenses': [None] * num_entries,
        'sellingGeneralAndAdministrativeExpenses': [None] * num_entries,
        'otherExpenses': [None] * num_entries,
        'operatingExpenses': [None] * num_entries,
        'costAndExpenses': [None] * num_entries,
        'interestIncome': [None] * num_entries,
        'interestExpense': [None] * num_entries,
        'depreciationAndAmortization': [None] * num_entries,
        'ebitda': [None] * num_entries,
        'ebitdaratio': [None] * num_entries,
        'operatingIncome': [None] * num_entries,
        'operatingIncomeRatio': [None] * num_entries,
        'totalOtherIncomeExpensesNet': [None] * num_entries,
        'incomeBeforeTax': [None] * num_entries,
        'incomeBeforeTaxRatio': [None] * num_entries,
        'incomeTaxExpense': [None] * num_entries,
        'netIncome': [None] * num_entries,
        'netIncomeRatio': [None] * num_entries,
        'eps': [None] * num_entries,
        'epsdiluted': [None] * num_entries,
        'weightedAverageShsOut': [None] * num_entries,
        'weightedAverageShsOutDil': [None] * num_entries,
        # Balance sheet
        'cashAndCashEquivalents': [None] * num_entries,
        'shortTermInvestments': [None] * num_entries,
        'cashAndShortTermInvestments': [None] * num_entries,
        'netReceivables': [None] * num_entries,
        'inventory': [None] * num_entries,
        'otherCurrentAssets': [None] * num_entries,
        'totalCurrentAssets': [None] * num_entries,
        'propertyPlantEquipmentNet': [None] * num_entries,
        'goodwill': [None] * num_entries,
        'intangibleAssets': [None] * num_entries,
        'goodwillAndIntangibleAssets': [None] * num_entries,
        'longTermInvestments': [None] * num_entries,
        'taxAssets': [None] * num_entries,
        'otherNonCurrentAssets': [None] * num_entries,
        'totalNonCurrentAssets': [None] * num_entries,
        'otherAssets': [None] * num_entries,
        'totalAssets': [None] * num_entries,
        'accountPayables': [None] * num_entries,
        'shortTermDebt': [None] * num_entries,
        'taxPayables': [None] * num_entries,
        'deferredRevenue': [None] * num_entries,
        'otherCurrentLiabilities': [None] * num_entries,
        'totalCurrentLiabilities': [None] * num_entries,
        'longTermDebt': [None] * num_entries,
        'deferredRevenueNonCurrent': [None] * num_entries,
        'deferredTaxLiabilitiesNonCurrent': [None] * num_entries,
        'otherNonCurrentLiabilities': [None] * num_entries,
        'totalNonCurrentLiabilities': [None] * num_entries,
        'otherLiabilities': [None] * num_entries,
        'capitalLeaseObligations': [None] * num_entries,
        'totalLiabilities': [None] * num_entries,
        'preferredStock': [None] * num_entries,
        'commonStock': [None] * num_entries,
        'retainedEarnings': [None] * num_entries,
        'accumulatedOtherComprehensiveIncomeLoss': [None] * num_entries,
        'othertotalStockholdersEquity': [None] * num_entries,
        'totalStockholdersEquity': [None] * num_entries,
        'totalEquity': [None] * num_entries,
        'totalLiabilitiesAndStockholdersEquity': [None] * num_entries,
        'minorityInterest': [None] * num_entries,
        'totalLiabilitiesAndTotalEquity': [None] * num_entries,
        'totalInvestments': [None] * num_entries,
        'totalDebt': [None] * num_entries,
        'netDebt': [None] * num_entries,
        # Cash flow
        'deferredIncomeTax': [None] * num_entries,
        'stockBasedCompensation': [None] * num_entries,
        'changeInWorkingCapital': [None] * num_entries,
        'accountsReceivables': [None] * num_entries,
        'accountsPayables': [None] * num_entries,
        'otherWorkingCapital': [None] * num_entries,
        'otherNonCashItems': [None] * num_entries,
        'netCashProvidedByOperatingActivities': [None] * num_entries,
        'investmentsInPropertyPlantAndEquipment': [None] * num_entries,
        'acquisitionsNet': [None] * num_entries,
        'purchasesOfInvestments': [None] * num_entries,
        'salesMaturitiesOfInvestments': [None] * num_entries,
        'otherInvestingActivites': [None] * num_entries,
        'netCashUsedForInvestingActivites': [None] * num_entries,
        'debtRepayment': [None] * num_entries,
        'commonStockIssued': [None] * num_entries,
        'commonStockRepurchased': [None] * num_entries,
        'dividendsPaid': [None] * num_entries,
        'otherFinancingActivites': [None] * num_entries,
        'netCashUsedProvidedByFinancingActivities': [None] * num_entries,
        'effectOfForexChangesOnCash': [None] * num_entries,
        'netChangeInCash': [None] * num_entries,
        'cashAtEndOfPeriod': [None] * num_entries,
        'cashAtBeginningOfPeriod': [None] * num_entries,
        'operatingCashFlow': [None] * num_entries,
        'capitalExpenditure': [None] * num_entries,
        'freeCashFlow': [None] * num_entries
    }
    # Save entries from cash flow statement
    for S in cash_flow:
        t = S['calendarYear'] + S['period']
        try:
            index = dates.index(t)
        except:
            # print(dates)
            # print(S)
            # print(f'Failed to find {date} in {dates}')
            return None
            # continue
        for k, v in S.items():
            if k in entries:
                entries[k][index] = v
    for S in balance_sheet:
        t = S['calendarYear'] + S['period']
        try:
            index = dates.index(t)
        except:
            # print(dates)
            # print(S)
            # print(f'Failed to find {date} in {dates}')
            return None
            # continue
        for k, v in S.items():
            if k in entries:
                entries[k][index] = v
    for S in income:
        t = S['calendarYear'] + S['period']
        try:
            index = dates.index(t)
        except:
            # print(f'Failed to find {date} in {dates}')
            return None
            # continue
        for k, v in S.items():
            if k in entries:
                entries[k][index] = v
        entries['timestamp'][index] = t
    return pd.DataFrame.from_dict(entries)

