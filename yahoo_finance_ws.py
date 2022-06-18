from doctest import ELLIPSIS_MARKER
from telnetlib import LINEMODE
#from selenium import webdriver
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
from bs4 import BeautifulSoup
import requests
import re
import numpy as np


#driver = webdriver.Chrome('/Users/sergioroldan/Downloads/chromedriver')

data_sgst_dict = {}

company_name = str(input("Write the company name => \n"))
base_path = "https://finance.yahoo.com/"
lookup_path = "lookup/all?s={}".format(company_name)
search_path = base_path + lookup_path

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
}

data_search = requests.get(search_path, headers=headers).text

soup_search = BeautifulSoup(data_search, 'html.parser')

sgst_list = soup_search.find('tbody', class_=False).find_all('a')
sgst_tab = soup_search.find('tbody', class_=False).find_all('tr')



def filter_checker(lookup_path, search_path, from_yr, from_dy, from_mt, to_yr, to_dy, to_mt, f, freq):
    date_from = ""
    date_to = ""
    
    if from_yr > to_yr:
        print("Please, be aware that the initial year must be before in time that the final year")
        stock_history(lookup_path, search_path)
    
    elif f not in freq:
        print("Please, use one of these frequency selectors: {}".format(freq))
        stock_history(lookup_path, search_path)           
    else:
        if f == 'Daily':
            f = '1d'
        elif f == 'Weekly':
            f = '1wk'
        else:
            f = '1mo'
        try:
            date_from = datetime.datetime(int(from_yr), int(from_mt), int(from_dy))
            date_to = datetime.datetime(int(to_yr), int(to_mt), int(to_dy))
            return date_from, date_to, f
        except Exception as e:
            print("Please, use the following format and length for years: yyyy\nfor days: dd\nfor months: mm")
            print(e)
            stock_history(lookup_path, search_path)
                    

def display_stats(vm, sph, ss, ds, fy, pft, me, ins, bs, cfs):
    print("\n"+"-- Valuation Measures --\n")
    print("-------------------------")
    for k,v in vm.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("-- Trading Information --")
    print("\n"+"Stock Price History\n")
    print("-------------------------")
    for k,v in sph.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("\n"+"Share Statistics\n")
    print("-------------------------")
    for k,v in ss.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("\n"+"Dividends & Splits\n")
    print("-------------------------")
    for k,v in ds.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("-- Financial Highlights --")
    print("\n"+"Fiscal Year\n")
    print("-------------------------")
    for k,v in fy.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("\n"+"Profitability\n")
    print("-------------------------")
    for k,v in pft.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("\n"+"Management Effectiveness\n")
    print("-------------------------")
    for k,v in me.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("\n"+"Income Statement\n")
    print("-------------------------")
    for k,v in ins.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("\n"+"Balance Sheet\n")
    print("-------------------------")
    for k,v in bs.items():
        print("{} => {}".format(k,v))
        
    print("-------------------------\n")
    print("\n"+"Cash Flow Statement\n")
    print("-------------------------")
    for k,v in cfs.items():
        print("{} => {}".format(k,v))

    print("-------------------------\n")

       
def stock_statistics(lookup_path, search_path):
    split = search_path.split('?')
    search_path = base_path + split[0] + lookup_path + split[1]
    data_search = requests.get(search_path, headers=headers).text
    soup_search = BeautifulSoup(data_search, 'html.parser')
    stats_tab = soup_search.find('div', class_='Mstart(a) Mend(a)')
    stats_tab_divs = stats_tab.find_all('tbody')
    
    #Valuation Measures
    vm = stats_tab_divs[0].find_all('td')
    value_measures = {}
    #Stock Price History
    sph = stats_tab_divs[1].find_all('td')
    stock_price_hist = {}
    #Share Statistics
    ss = stats_tab_divs[2].find_all('td')
    share_stats = {}
    #Dividends & Splits
    ds = stats_tab_divs[3].find_all('td')
    dividends_splits = {}
    #Fiscal Year
    fy = stats_tab_divs[4].find_all('td')
    fiscal_year = {}
    #Profitability
    pft = stats_tab_divs[5].find_all('td')
    profitability = {}
    #Management Effectiveness
    me = stats_tab_divs[6].find_all('td')
    mgmt_effectiveness = {}
    #Income Statement
    ins = stats_tab_divs[7].find_all('td')
    income_statement = {}
    #Balance Sheet
    bs = stats_tab_divs[8].find_all('td')
    balace_sheet = {}
    #Cash Flow Statement
    cfs = stats_tab_divs[9].find_all('td')
    cash_flow_statement = {}

    #support variables
    x= ""
    y = ""
    
    for e in vm:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        value_measures[x] = y

    for e in sph:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        stock_price_hist[x] = y

    for e in ss:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        share_stats[x] = y

    for e in ds:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        dividends_splits[x] = y
                
    for e in fy:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        fiscal_year[x] = y
                
    for e in pft:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        profitability[x] = y
                
    for e in me:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        mgmt_effectiveness[x] = y
                   
    for e in ins:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        income_statement[x] = y
                
    for e in bs:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        balace_sheet[x] = y  
    
    for e in cfs:
        if e.span != None:
            x = e.span.text
        else:
            y = e.text
        cash_flow_statement[x] = y
        
    
    display_stats(value_measures, stock_price_hist, share_stats, dividends_splits, fiscal_year, profitability, mgmt_effectiveness, income_statement, balace_sheet, cash_flow_statement)
    
    
def stock_history(lookup_path, search_path):
    hist_data_dict = {}
    freq = ['Daily', 'Weekly', 'Monthly', 'Monthly']
    split = search_path.split('?')
    search_path = base_path + split[0] + lookup_path + split[1]
    data_search = requests.get(search_path, headers=headers).text
    soup_search = BeautifulSoup(data_search, 'html.parser')
    print("\nFrom\n")
    from_yr = str(input("Year => "))
    from_mt = str(input("Month => "))
    from_dy = str(input("Day => "))
    print("\nTo\n")
    to_yr = str(input("Year => "))
    to_mt = str(input("Month => "))
    to_dy = str(input("Day => "))
    f = str(input("Frequency (Daily, weekly or Monthly) => "))
    
    date_from, date_to, f = filter_checker(lookup_path, search_path, from_yr, from_dy, from_mt, to_yr, to_dy, to_mt, f, freq)
    dt_from_unix = int(time.mktime(date_from.timetuple()))
    dt_to_unix = int(time.mktime(date_to.timetuple()))
    
    hist_path = '/history?period1={}&period2={}&interval={}&filter=history&frequency={}&includeAdjustedClose=true'.format(dt_from_unix, dt_to_unix, f, f)
    
    search_path = base_path + split[0] + hist_path
    data_search = requests.get(search_path, headers=headers).text
    soup_search = BeautifulSoup(data_search, 'html.parser')
    
    hist_table = soup_search.find('table', attrs={'data-test': 'historical-prices'})
    tbody = hist_table.tbody.find_all('tr')
    
    #driver.get(search_path)
    #time.sleep(2)
    #scroll_pause_time = 10
    #screen_height = driver.execute_script("return window.screen.height;")
    #i = 1
    
    #while True:
        # scroll one screen height each time
        #driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        #i += 1
        #time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        #scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        #if (screen_height) * i > scroll_height:
            #break
    idx = 0
    for td in tbody:
        span = td.find_all('span')
        try:
            date = span[0].text
            open = span[1].text
            high = span[2].text
            low = span[3].text
            close = span[4].text
            adj_close = span[5].text
            vol = span[6].text.replace(",", "")
            
            hist_data_dict[idx] = [date, open, high, low, close, adj_close, vol]
            idx += 1
        except Exception as e:
            pass       
        
        
    hist_df = pd.DataFrame.from_dict(hist_data_dict, 
                                     orient='index', 
                                     columns=['date', 'open', 'high', 'low', 'close', 'adj', 'volume'])
    hist_df.open.astype('float64')
    hist_df.high.astype('float64')
    hist_df.low.astype('float64')
    hist_df.close.astype('float64')
    hist_df.adj.astype('float64')
    hist_df.volume.astype('float64')
    
    print("\n"+"-----------------------------------------------------\n")
    print(hist_df)


def option_data_retriever(option, search_path):
    
    if option == '1':
        stock_statistics('/key-statistics?', search_path)
    elif option == '2':
        stock_history('/history?', search_path)


def stock_scraper(ticker_lookup_url):
    opts = ["1","2"]
    search_path = base_path + ticker_lookup_url
    data_search = requests.get(search_path, headers=headers).text
    soup_search = BeautifulSoup(data_search, 'html.parser')
    
    print("\n")    
    option = str(input("Would you like to retrieve Statistical [1] or Historical [2] Data ? => "))

    while option not in opts:
        print("\n")
        option = str(input("Would you like to retrieve Statistical [1] or Historical [2] Data ? => "))
    
    option_data_retriever(option, ticker_lookup_url)

def sugestions_builder():

    for opt in sgst_tab:
        data_symbol = opt.td.a['data-symbol']
        data_href = opt.td.a['href']
        data_title = opt.td.a['title']
        data_lastprice = "Last Price: " + opt.find('td', class_='data-col2 Ta(end) Pstart(20px) Pend(15px)').text
    
        data_sgst_dict[data_symbol] = [data_title, data_lastprice, data_href]

    print("Did you meant?\n")

    for k,v in data_sgst_dict.items():
    
        print("{} => {} - {}".format(k,v[0], v[1]))

    print("\n")    
    ticker_sel = str(input("Select one of these ticker stock sugestions above => ")).upper()

    while ticker_sel not in data_sgst_dict and ticker_sel is not None:
        print("\n")
        ticker_sel = str(input("Select one of these ticker stock sugestions above => ")).upper()

    
    stock_scraper(data_sgst_dict[ticker_sel][2])
    


sugestions_builder()
