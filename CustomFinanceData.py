#dependencies

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

import yfinance as yf

from fredapi import Fred
import logging

from dataclasses import dataclass, astuple, asdict, field
import inspect
from pprint import pprint

#Info class: this is class to get stock info or analysis
# 1. Get SNP500 GISC sector in json format or 'Sec_GISC' class
# 2. Get Stock Correlation Matrix in csv format or NArray class
#Historical data: this class to get historical data
# 1. Get historical yield spread 10y minus 2y from Fred



@dataclass
class Custom_data:
    ErrorMessage: str = ""

@dataclass(frozen=True, order=True)
class StockInfo:
    
    Symbol:str = ""
    SecurityName:str = ""
    GISC_Sector:str = ""
    GISC_Sub_INDUSTRY:str = ""
    CIK:str = "" 

@dataclass       
class Sec_GISC(Custom_data):
    
    Tickers : list[StockInfo] = field(default_factory=list)  #expect to add stockInfo class
    
    def Add(self, stockInfoOjb):
        self.Tickers.append(stockInfoOjb)
    def __str__(self):
        if self.ErrorMessage == "":
            return f"Sec_GISC with {len(self.Tickers)} items"
        else:
            return f"Sec_GISC with error: {self.ErrorMessage}"


@dataclass(frozen=True, order=True)
class yield_data:
    Date: datetime
    Spread: float

@dataclass
class Yield10y2y(Custom_data):
    data: list[yield_data] = field(default_factory=list)        

    def Add(self, yield_dataObj):
        self.data.append(yield_dataObj)

    def __str__(self):
        if self.ErrorMessage == "":
            return f'Yield10y2y with {len(self.data)} items'
        else:
            return f'Yield10y2y with error: {self.ErrorMessage}'

class Info:

    def __init__(self) -> None:
        pass
    #Web scraping

    # Shared function to make the HTTP request and obtain the content
    def get_html_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logging.warning(f"Error in reading page: {response.status_code}")
            raise Exception(f"Error in obtaining page content, status code: {response.status_code}")
            
    # Shared function to parse HTML content with BeautifulSoup
    def parse_html_to_soup(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup


    # Function to extract the data from the current S&P 500 constituents table
    def extract_current_snp_data_listOfList(self, soup):
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

    def extract_current_snp_data_listOfStockInfo(self, soup)->list[StockInfo]:
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
            current_data.append(StockInfo(SecurityName= security,Symbol= symbol, GISC_Sector= gis_sector, GISC_Sub_INDUSTRY= gis_sub_ind,CIK= cik_code))
        return current_data


    # Extract data and create a DataFrame
    def get_snp500_list_with_sector(self, output_format = "class"):

        # Define the URL of the Wikipedia page for scraping
        URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

        snp500_sec_gisc = Sec_GISC()

        try:
            # Get the HTML content of the Wikipedia page
            html_content = self.get_html_content(URL)

            # Parse the HTML content to get the BeautifulSoup object
            soup = self.parse_html_to_soup(html_content)

            # Verify that significant content was extracted
            test_element = soup.find('h1', id="firstHeading")
            assert test_element is not None, "The HTML content does not contain the expected element."
            print("The HTML content has been successfully extracted and parsed.")

            
            if output_format == "json":
                logging.debug(f"output to json format with keyword {output_format}")
                current_data = self.extract_current_snp_data_listOfList(soup)
                return pd.DataFrame(current_data).to_json(orient='records', lines=True)
            else:
                logging.debug(f"output to class format with keyword {output_format}")
                snp500_sec_gisc.Tickers = self.extract_current_snp_data_listOfStockInfo(soup)
                return snp500_sec_gisc
            
        except requests.exceptions.RequestException as e:
            # Handle connection errors, timeouts, or invalid URLs
            print(f"An error occurred: {e}")
            
            snp500_sec_gisc.ErrorMessage("Error occur")
            return "Error while scraping data"
        

    #Get Stocks correlation via yFinance Data
    def get_stocks_correlation(self, tickers, start_date, end_date, output_format="class"):
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

        if output_format == "csv":
        #return data in csv format
            return correlation_matrix.to_csv()
        else:
            return correlation_matrix





#API functions


class HistoricalData:


    #API from Fred. Get 10 years minus 2 years yield curve. Negative # means yield curve inversion
    #param: "T10Y2Y"    
    def get_file_contents(self, filename):
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


    def get_10y2y_yield(self, output_format="class"):
        filename = 'apikey'

        try:
            api_key = self.get_file_contents(filename)
            fred = Fred(api_key=api_key) 
            yield10y2y_d = fred.get_series_latest_release('T10Y2Y')
            
            yield10y2y_d = pd.DataFrame(yield10y2y_d).reset_index()
            yield10y2y_d.columns = ['Date','Spread']
            
            yield10y2y_d['Date'] = yield10y2y_d['Date'].apply(lambda x: x.strftime("%Y-%m-%d"))

            if output_format=="json":

                return yield10y2y_d.to_json(orient='records', lines=True)
            else:
                Yield10y2y_obj = Yield10y2y()
                for i in yield10y2y_d.index:
                    Yield10y2y_obj.Add(yield_data(yield10y2y_d['Date'][i], yield10y2y_d['Spread'][i]))
                return Yield10y2y_obj
                
        except:

            # Handle connection errors, timeouts, or invalid URLs
            
            Yield10y2y_obj = Yield10y2y()
            Yield10y2y_obj.ErrorMessage("Error occur")
            return "Error while API calling"
        



if __name__=='__main__':

    print("This is Custom Finance Data class. Refer test_customFinanceData.py for how to call the functions")
    
    