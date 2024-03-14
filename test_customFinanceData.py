import CustomFinanceData as cfd
from datetime import datetime, timedelta


#Test functions


def test_get_snp500_list_Wiki():
    info = cfd.Info()
    snp500_info = info.get_snp500_list_with_sector()

    # Display the first records to confirm
    print(snp500_info)
    for tick in snp500_info.Tickers:
        print(tick)

def test_get_snp500_list_WikiJson():
    info = cfd.Info()
    snp500_json = info.get_snp500_list_with_sector(output_format="json")

    # Display the first records to confirm
    print(snp500_json)
    


def test_Fred10y2y():
    historicaldata = cfd.HistoricalData()

    fred10y2y = historicaldata.get_10y2y_yield()
    print(fred10y2y.data[-1])

def test_Fred10y2yJson():
    historicaldata = cfd.HistoricalData()

    fred10y2y_json = historicaldata.get_10y2y_yield(output_format="json")
    print(fred10y2y_json)


def test_get_stocks_correlation():
    info = cfd.Info()
    symbol_list = ['AAPL', 'IBM', 'SPY']
    end_date = datetime.today()
    start_date = end_date - timedelta(days = 1*365)
    
    corr_json = info.get_stocks_correlation(symbol_list, start_date=start_date, end_date=end_date)
    print(corr_json)

def test_get_stocks_correlationCSV():
    info = cfd.Info()
    symbol_list = ['AAPL', 'IBM', 'SPY']
    end_date = datetime.today()
    start_date = end_date - timedelta(days = 1*365)
    
    corr_json = info.get_stocks_correlation(symbol_list, start_date=start_date, end_date=end_date, output_format="csv")
    print(corr_json)



def FunctionsListDescription():
    print("Test function menu:")
    print("1. Web Scraping to Sec_GISC class: Extract snp 500 symbol, description and sectors from Wiki page")
    print("2. API to Yeild10y2y class: Get histroical 10yr minus 2yr spread (recession indicator) from Fred")
    print("3. API to Narray: Calculate stock corrrelation, sourcing Yahoo Finance historical prices")
    print("4. Web Scraping to Json: Extract snp 500 symbol, description and sectors from Wiki page")
    print("5. API to Json: Get histroical 10yr minus 2yr spread (recession indicator) from Fred")
    print("6. API to CSV: Calculate stock corrrelation, sourcing Yahoo Finance historical prices")
    
    
    


def display_menu():
    while True:
        FunctionsListDescription()

        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

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
            print("You selected Option 4")
            test_get_snp500_list_WikiJson()
        elif choice == "5":
            print("You selected Option 5")
            test_Fred10y2yJson()
        elif choice == "6":
            print("You selected Option 6")
            test_get_stocks_correlationCSV()
            
        elif choice == "7":
            print("Exiting the menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__=='__main__':
    display_menu()