# market-prediction
Experiment with long-term market predictions.  

The goal is to use the past `N` years of a comapny's financial reports to predict its growth over the next 3, 5, and 10 years.

## Dataset
Fetching the training dataset requires a [FMP](https://site.financialmodelingprep.com/) API key.  
Just put your API key in a text file called `apikey.txt` in the project root.

To fetch the dataset run `python data_collect.py NUM_SAMPLES [--history YEARS]`  
This will fetch all the required financial data for the desired number of data samples.

**Note**: the model requires `NUM_SAMPLES + 10` years worth of financial reports for training, which will require a paid subscription with FMP. The free tier only provides 5 years of data.

## Training
TODO

## Inference
TODO
