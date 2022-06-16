import pandas as pd
import numpy as numpy
import requests
import re
from bs4 import BeautifulSoup


stock = input("Which company would you like to retrieve information from? => ")
    

def content_scraper(stck):
    stock = stck
    
    base_URL= "https://www.google.com/finance"

    search_URL = base_URL+("/quote/{}").format(stock)
    
    data_search = requests.get(search_URL).text

    soup_search = BeautifulSoup(data_search, 'html.parser')
    
    if soup_search.find('ul', class_='sbnBtf xJvDsc ANokyb') is not None:

        parser_search = soup_search.find('ul', class_='sbnBtf xJvDsc ANokyb').li.a.attrs['href'][1:]

        URL = base_URL+parser_search

        data = requests.get(URL).text
    
        soup = BeautifulSoup(data, 'html.parser')
    
        return soup
    
    else:
        stock = input("Which company would you like to retrieve information from? => ")
        content_scraper(stock)        

        

def table_gen():   
    soup = content_scraper(stock)
    r = "(-?\d+(?:\.\d+)?)"
    if soup is not None:
        
        stk_title = soup.find('div', class_='zzDege').text + "\n" + soup.find('div', class_='PdOqHc').text

        date = soup.find('div', class_='zsnTKc').find('span', class_='VfPpkd-vQzf8d').text

        table_fs = soup.find_all('table', class_='QzSQAb')[0]
        table_bs = soup.find_all('table', class_='QzSQAb')[1]
        table_cf = soup.find_all('table', class_='QzSQAb')[2]

        rows_table_fs = table_fs.find_all('tr', class_='roXhBd')
        rows_table_bs = table_bs.find_all('tr', class_='roXhBd')
        rows_table_cf = table_cf.find_all('tr', class_='roXhBd')

        idx_tb_fs = []
        col_1_tb_fs = []
        col_2_tb_fs = []

        idx_tb_bs = []
        col_1_tb_bs = []
        col_2_tb_bs = []

        idx_tb_cf = []
        col_1_tb_cf = []
        col_2_tb_cf = []


        for row in rows_table_fs:
            x = re.search(r, row.find('td', class_='QXDnM').text)
            y = re.search(r, row.find('td', class_='gEUVJe').text)
            idx_tb_fs.append(row.find('div', class_='GKeVic').text)
            try:
                col_1_tb_fs.append(float(x.group()))
            except:
                col_1_tb_fs.append("-")
            
            try:
                col_2_tb_fs.append(float(y.group()))
            except:
                col_2_tb_fs.append("-")

        df_fs = pd.DataFrame(data={date: col_1_tb_fs, 'Y/Y Change': col_2_tb_fs}, index=idx_tb_fs)


        for row in rows_table_bs:
            x = re.search(r, row.find('td', class_='QXDnM').text)
            y = re.search(r, row.find('td', class_='gEUVJe').text)
            idx_tb_bs.append(row.find('div', class_='GKeVic').text)
            try:
                col_1_tb_bs.append(float(x.group()))
            except:
                col_1_tb_bs.append("-")
            
            try:
                col_2_tb_bs.append(float(y.group()))
            except:
                col_2_tb_bs.append("-")

        df_bs = pd.DataFrame(data={date: col_1_tb_bs, 'Y/Y Change': col_2_tb_bs}, index=idx_tb_bs)

        for row in rows_table_cf:
            x = re.search(r, row.find('td', class_='QXDnM').text)
            y = re.search(r, row.find('td', class_='gEUVJe').text)
            idx_tb_cf.append(row.find('div', class_='GKeVic').text)
            try:
                col_1_tb_cf.append(float(x.group()))
            except:
                col_1_tb_cf.append("-")
            
            try:
                col_2_tb_cf.append(float(y.group()))
            except:
                col_2_tb_cf.append("-")

        df_cf = pd.DataFrame(data={date: col_1_tb_cf, 'Y/Y Change': col_2_tb_cf}, index=idx_tb_cf)
        print("\n")
        print(stk_title)
        print("------------------------------------------------------")
        print(df_fs)
        print("------------------------------------------------------")
        print(df_bs)
        print("------------------------------------------------------")
        print(df_cf)
        print("------------------------------------------------------")
    else:
        content_scraper(stock)


if __name__ == "__main__":
    table_gen()
            

