import numpy as np
import pandas as pd
import sys, os
import math
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

def mydatetime(x):
    return np.array(x, dtype=np.datetime64)

infile = sys.argv[1]
datafile = sys.argv[2]
stock_content = pd.read_csv(infile, index_col=[0])
date = mydatetime(stock_content.index)
close_price = stock_content['Close']
p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'
p1.line(date, close_price, color='#A6CEE3', legend='000002')

data_content = pd.read_csv(datafile)
g = {'nan': 0}
inf = {'inf': 0}
samples = data_content['sample']
samples = [eval(x, g, inf) for x in samples]
print samples[0]['trade_date']
print samples[1]['trade_date']
samples = np.array(samples)
classes = data_content['class']
buy_samples = [x for x in samples if x['class']!=-1]
sell_samples = [x for x in samples if x['class']==-1]
#buy_samples = samples[classes==-1]
#sell_samples = samples[classes!=-1]
for x in buy_samples:
    print x['trade_date'], ' ', x['trade_price']
#print buy_samples

price_offset = 0.20
buy_trade_date = [(x['trade_date']) for x in buy_samples]
buy_trade_price = [(x['trade_price']*(1+price_offset)) for x in buy_samples]
buy_trade_date = mydatetime(buy_trade_date)
sell_trade_date = [(x['trade_date']) for x in sell_samples]
sell_trade_price = [(x['trade_price']*(1-price_offset)) for x in sell_samples]
sell_trade_date = mydatetime(sell_trade_date)
p1.circle(buy_trade_date, buy_trade_price, size=4, legend='buy', color='red', alpha=0.2)
p1.circle(sell_trade_date, sell_trade_price, size=4, legend='sell', color='green', alpha=0.2)

output_file("stocks.html", title="stocks.py example")
show(gridplot([[p1]], plot_width=800, plot_height=600))

