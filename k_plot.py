import time
from math import pi
import pandas as pd
from datetime import datetime
import numpy as np
import sys, os
from bokeh.io import output_notebook
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Rect, HoverTool, Range1d, LinearAxis, WheelZoomTool, PanTool, ResetTool, ResizeTool, SaveTool
#output_notebook()
output_file("kline.html")

infile = sys.argv[1]
quotes = pd.read_csv(infile)
#quotes[quotes['Volume']==0]=np.nan
quotes= quotes.dropna()
openp=quotes['Open']
closep=quotes['Close']
highp=quotes['High']
lowp=quotes['Low']
volume=quotes['Volume']
#time=quotes.index
#date=[x.strftime("%Y-%m-%d") for x in quotes.index]
#time=quotes['Time']
time=[datetime.strptime(x, '%Y-%m-%d') for x in quotes['Time']]
date=[x.strftime("%Y-%m-%d") for x in time]
quotes['Date']=date

w = 12*60*60*1000 # half day in ms
mids = (openp + closep)/2
spans = abs(closep-openp)
inc = closep > openp
dec = openp > closep

ht = HoverTool(tooltips=[
            ("date", "@mids"),
            ("open", "@open"),
            ("close", "@close"),
            ("high", "@high"),
            ("low", "@low"),
            ("volume", "@volume"),])
TOOLS = [ht, WheelZoomTool(), ResizeTool(), ResetTool(),PanTool(), SaveTool()]

max_x = max(highp)
min_x = min(lowp)
x_range = max_x - min_x  
y_range = (min_x - x_range / 2.0, max_x + x_range * 0.1)  
p = figure(x_axis_type="datetime", tools=TOOLS, plot_height=600, plot_width=950,toolbar_location="above", y_range=y_range)

p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3
p.background_fill_color = "black"

quotesdate=dict(date1=quotes['Date'],open1=openp,close1=closep,high1=highp,low1=lowp)
ColumnDataSource(quotesdate)
x_rect_inc_src =ColumnDataSource(quotes[inc])
x_rect_dec_src =ColumnDataSource(quotes[dec])
print x_rect_inc_src

time_inc = [time[i] for i in xrange(len(inc)) if inc[i]==True]
time_dec = [time[i] for i in xrange(len(inc)) if dec[i]==True]
mids_inc = [mids[i] for i in xrange(len(inc)) if inc[i]==True]
mids_dec = [mids[i] for i in xrange(len(inc)) if dec[i]==True]
spans_inc = [spans[i] for i in xrange(len(inc)) if inc[i]==True]
spans_dec = [spans[i] for i in xrange(len(inc)) if dec[i]==True]
highp_inc = [highp[i] for i in xrange(len(inc)) if inc[i]==True]
highp_dec = [highp[i] for i in xrange(len(inc)) if dec[i]==True]
lowp_inc = [lowp[i] for i in xrange(len(inc)) if inc[i]==True]
lowp_dec = [lowp[i] for i in xrange(len(inc)) if dec[i]==True]

#p.rect(x='Date', y='Volume', width=0.75, height=spans[inc], fill_color="red", line_color="red", source=x_rect_inc_src)
p.rect(x=time_inc, y=mids[inc], width=w, height=spans_inc, fill_color="red", line_color="red")
p.rect(x=time_dec, y=mids[dec], width=w, height=spans_dec, fill_color="green", line_color="green")
#p.segment(time[inc], highp[inc], time[inc], lowp[inc], color="red")
#p.segment(time[dec], highp[dec], time[dec], lowp[dec], color="green")
p.segment(time_inc, highp_inc, time_inc, lowp_inc, color="red")
p.segment(time_dec, highp_dec, time_dec, lowp_dec, color="green")
show(p)
