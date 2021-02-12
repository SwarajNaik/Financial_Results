import re
import json
from bs4 import BeautifulSoup
import requests
from io import StringIO

url_financial = 'https://finance.yahoo.com/quote/{}/financials?p={}'

stock = 'KOTAKBANK.BO'

reponse = requests.get(url_financial.format(stock, stock))

soup = BeautifulSoup(reponse.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')

script_data = soup.find('script', text=pattern).contents[0]

start = script_data.find("context")-2
json_data = json.loads(script_data[start:-12])

annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quaterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']


annual_is_statement = []

for s in annual_is:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
        
    annual_is_statement.append(statement)

while True:

    symbol = input('Stock symbol(please spell correctly): ')
    period = input('Annual Income Statement(a)/ Quaterly Income Statement(q): ')

    stock = symbol

    reponse = requests.get(url_financial.format(stock, stock))

    soup = BeautifulSoup(reponse.text, 'html.parser')

    pattern = re.compile(r'\s--\sData\s--\s')

    script_data = soup.find('script', text=pattern).contents[0]

    start = script_data.find("context")-2
    json_data = json.loads(script_data[start:-12])

    annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
    quaterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']


    annual_is_statement = []

    for s in annual_is:
        statement = {}
        for key, val in s.items():
            try:
                statement[key] = val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
            
        annual_is_statement.append(statement)

        if period == 'a':
            print(annual_is_statement)
        
        elif period == 'q':
            print(quaterly_is)
        
        else:
            print('Spell correctly...')

