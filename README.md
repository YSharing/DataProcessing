# DataProcessing
This repository is to keep data processing functions in separated modules that can be used in other projects.

#CustomFinanceData.py
This module can be run in console mode to test the functions. "test_" functions are demo for the "get" functions.

Test function menu:
1. Web Scraping to Json: Extract snp 500 symbol, description and sectors from Wiki page
2. API to Json: Get histroical 10yr minus 2yr spread (recession indicator) from Fred (Federal Reserve Economic Data)
3. API to CSV: Calculate stock corrrelation, sourcing Yahoo Finance historical prices
4. Exit

For Fred API, you will need to get your own api key and save it in file "apikey" (without file extension) in order to use the function. The "apikey" file needs to be same folder as "CustomFinanceData.py". the First line of the "apikey" file is the api key from Fred account.  You can create a free account by visiting "https://fred.stlouisfed.org/" and go to "My Account".


