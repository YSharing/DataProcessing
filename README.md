# DataProcessing
This repository is to keep data processing functions in separated modules that can be used in other projects.

"CustomFinanceData.py"
This module is collections of custom functions. There are 2 main classes.
1. Info class for query security info and analysis (Wiki for S&P 500 GISC sector, yFinance for stock price correlation)
2. Historical class for query security historical data from different source (Fred - Federal Reserve Economic Data)
3. Each function has optional output format. Either in class structure or Json/CSV. Refer "test_CustomFinanceData.py" for samples.
     
For Fred API, you will need to get your own api key and save it in file "apikey" (without file extension) in order to use the function. The "apikey" file needs to be same folder as "CustomFinanceData.py". the First line of the "apikey" file is the api key from Fred account.  You can create a free account by visiting "https://fred.stlouisfed.org/" and go to "My Account".


"test_CustomFinanceData.py"
This module is to demostrate how to use functions and classes in "CustomFinanceData.py"

Test function menu:
1. Web Scraping to Sec_GISC class: Extract snp 500 symbol, description and sectors from Wiki page"
2. API to Yeild10y2y class: Get histroical 10yr minus 2yr spread (recession indicator) from Fred"
3. API to Narray: Calculate stock corrrelation, sourcing Yahoo Finance historical prices"
4. Web Scraping to Json: Extract snp 500 symbol, description and sectors from Wiki page"
5. API to Json: Get histroical 10yr minus 2yr spread (recession indicator) from Fred"
6. API to CSV: Calculate stock corrrelation, sourcing Yahoo Finance historical prices"
7. Exit    



