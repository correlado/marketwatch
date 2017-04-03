#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function


import json
import urllib2
import requests
import datetime
import pandas

class Market(object):
    """
    based on coinmarketcap.com api
    """

    def current_stats(self):
        url = 'https://api.coinmarketcap.com/v1/global/?convert=EUR'
        r = requests.get(url)
        data = r.json()
        data['date']=datetime.date.today()
        
        return data
    
    def current_ticker(self,limit=100):
        #download ticker list of top <limit> currencies
        url = 'https://api.coinmarketcap.com/v1/ticker/?convert=EUR&limit={}'.format(limit)
        r = requests.get(url)
        data = r.json()
        df = pandas.DataFrame(columns=data[0].keys()+['date'])
        for i in range(len(data)):
            df.loc[i]=data[i].values()+[datetime.date.today()]
        
        return df
        
    def current_historic_data(self, symbol='ETH', year=datetime.date.today().year):
        
        url='http://coinmarketcap.northpole.ro/api/v5/history/{0}_{1}.json'.format(symbol,year)
        r = requests.get(url)
        data = r.json()
        
        df = pandas.DataFrame(columns=['symbol','date','price','marketCap','availableSupplyNumber','volume24'])
        for i in range(len(data['history'].values())):
            row = data['history'].values()[i]
            
            df.loc[i]=[
                        row['symbol'],
                        datetime.datetime.strptime('-'.join(data['history'].keys()[i].split('-')),'%d-%m-%Y').date(),
                        float(row['price']['eur']),
                        float(row['marketCap']['eur']),
                        row['availableSupplyNumber'],
                        float(row['volume24']['btc']),
                        ]
        
        return df.sort_values(by='date')
    
    def full_historic_data(self,symbol='ETH',years=range(datetime.date.today().year-1, datetime.date.today().year+1,1)):
        
        return pandas.concat([self.current_historic_data(year=y) for y in years])
