# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 20:48:34 2020

@author: singh
"""
from flask import Flask, request, render_template, session, redirect
import pandas as pd
from datetime import datetime
import requests
import json

def get_high_price(symbol,my_ident):
    url = "https://www.nseindia.com/api/quote-derivative?symbol="+symbol+"&identifier="+my_ident
    payload = {}
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
      'Accept': '*/*'}
    response2 = requests.request("GET", url, headers=headers, data = payload)
    dict2 = json.loads(response2.text)
    # my_ident = dict2['info']['identifier']
    
    for i,j in enumerate(dict2['stocks']):
        # print([j][i]['underlyingValue'])
        if j['metadata']['identifier'] == my_ident:
            return (j['metadata']['highPrice'])

def table_maker():
    url = "https://www.nseindia.com/api/liveEquity-derivatives?index=stock_opt"
    payload = {}
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
      'Accept': '*/*'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    new_dict = json.loads(response.text)
    top_twenty_df = pd.DataFrame(new_dict['data'])
    new_df = top_twenty_df[['underlying','identifier','expiryDate','strikePrice','instrumentType','optionType','lastPrice']].copy()
    new_df["highPrice"] = new_df.apply(lambda x : get_high_price(x['underlying'],x['identifier']) , axis =1 )
    new_df["checkPrice"] =  new_df.apply(lambda x : True if x["lastPrice"]/x["highPrice"] >= 0.85 else False, axis =1 )
    final_df = new_df[new_df['checkPrice']==True][['underlying','expiryDate','strikePrice','optionType','lastPrice','highPrice',"checkPrice"] ].reset_index()
    final_df['index'] = final_df['index']+1
    final_df.rename(columns={"index": "Rank in Top 20","checkPrice" : ">85%"},inplace = True)
    return final_df

app = Flask(__name__)
@app.route('/', methods=("POST", "GET"))
def html_table():
    df = table_maker()
    df['time'] = datetime.now()
    return df.to_html(index=False)
    # return render_template('simple.html',  tables=[df.to_html()], titles=df.columns.values)

if __name__ == '__main__':
    app.run(host='0.0.0.0')