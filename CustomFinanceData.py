#dependencies

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

import yfinance as yf

from fredapi import Fred





def FunctionsList():
    print("Test function menu:")
    print("1. Web Scraping to Json: Extract snp 500 symbol, description and sectors from Wiki page")
    print("2. API to Json: Get histroical 10yr minus 2yr spread (recession indicator) from Fred")
    print("3. API to CSV: Calculate stock corrrelation, sourcing Yahoo Finance historical prices")

#Web scraping

# Shared function to make the HTTP request and obtain the content
def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error in obtaining page content, status code: {response.status_code}")

# Shared function to parse HTML content with BeautifulSoup
def parse_html_to_soup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


# Function to extract the data from the current S&P 500 constituents table
def _extract_current_snp_data(soup):
    table = soup.find('table', {'id': 'constituents'})
    rows = table.find_all('tr')[1:]  # Exclude the table header
    current_data = []
    for row in rows:
        cols = row.find_all('td')
        symbol = cols[0].text.strip()
        security = cols[1].text.strip()
        gis_sector = cols[2].text.strip()
        gis_sub_ind = cols[3].text.strip()
        cik_code = cols[6].text.strip() #for EDGAR filing
        current_data.append({'Security': security, 'Symbol': symbol, 'GISC_Sector': gis_sector, 'GISC_SUB_INDUSTRY': gis_sub_ind, "CIK": cik_code})
    return current_data

# Extract data and create a DataFrame
def get_snp500_list_with_sector():

    # Define the URL of the Wikipedia page for scraping
    URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # Get the HTML content of the Wikipedia page
    html_content = get_html_content(URL)

    # Parse the HTML content to get the BeautifulSoup object
    soup = parse_html_to_soup(html_content)

    # Verify that significant content was extracted
    test_element = soup.find('h1', id="firstHeading")
    assert test_element is not None, "The HTML content does not contain the expected element."
    print("The HTML content has been successfully extracted and parsed.")

    current_data = _extract_current_snp_data(soup)
    return pd.DataFrame(current_data).to_json(orient='records', lines=True)



#API functions


#1. Get Stocks correlation via yFinance Data
def get_stocks_correlation(tickers, start_date, end_date):
    Num_days = 252

    #download daily adjust priced from yFinance with given date range
    adj_close_df = pd.DataFrame()
    for ticker in tickers:

        data = yf.download(ticker, start = start_date,end = end_date)
        adj_close_df[ticker] = data['Adj Close']

    #calculate daily returns, get avg, then annualize it
    simple_returns = adj_close_df.pct_change()
    simple_returns = simple_returns.dropna()
    
    #calculate covariance and correlation
    simple_avg_return = simple_returns.mean() * Num_days
    simple_cov = simple_returns.cov() * Num_days


    # Calculate the standard deviations (square roots of variances)
    std_deviations = np.sqrt(np.diag(simple_cov))

    # Compute the outer product of standard deviations
    outer_product = np.outer(std_deviations, std_deviations)

    # Divide the covariance matrix by the outer product to get the correlation matrix
    correlation_matrix = simple_cov / outer_product


    #return data in csv format
    return correlation_matrix.to_csv()
    


#2. API from Fred. Get 10 years minus 2 years yield curve. Negative # means yield curve inversion
#param: "T10Y2Y"    
def get_file_contents(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


def get_10y2y_yield():
    filename = 'apikey'
    api_key = get_file_contents(filename)
    fred = Fred(api_key=api_key) 
    yield10y2y = fred.get_series_latest_release('T10Y2Y')
    
    yield10y2y = pd.DataFrame(yield10y2y).reset_index()
    yield10y2y.columns = ['Date','Spread']
    
    yield10y2y['Date'] = yield10y2y['Date'].apply(lambda x: x.strftime("%Y-%m-%d"))
    return yield10y2y.to_json(orient='records', lines=True)


#Test functions


def test_get_snp500_list_Wiki():
    snp500_json = get_snp500_list_with_sector()

    # Display the first records to confirm
    print(snp500_json)

def test_Fred10y2y():
    fred10y2y_json = get_10y2y_yield()
    print(fred10y2y_json)

def test_get_stocks_correlation():
    symbol_list = ['AAPL', 'IBM', 'SPY']
    end_date = datetime.today()
    start_date = end_date - timedelta(days = 1*365)
    
    corr_json = get_stocks_correlation(symbol_list, start_date=start_date, end_date=end_date)
    print(corr_json)

def display_menu():
    while True:
        FunctionsList()

        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            print("You selected Option 1")
            test_get_snp500_list_Wiki()
        elif choice == "2":
            print("You selected Option 2")
            test_Fred10y2y()
        elif choice == "3":
            print("You selected Option 3")
            test_get_stocks_correlation()
        elif choice == "4":
            print("Exiting the menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")



if __name__=='__main__':
    display_menu()

    
    