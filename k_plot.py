import time
from math import pi
import pandas as pd
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
time=[x.]
date=[x for x in time]
quotes['Date']=date

w = 12*60*60*1000 # half day in ms
mids = (openp + closep)/2
spans = abs(closep-openp)
inc = closep > openp
dec = openp > closep

ht = HoverTool(tooltips=[
            ("date", "@date"),
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
print quotes[inc]
print '---------------------------'
print x_rect_inc_src

#p.rect(x='Date', y='Volume', width=0.75, height=spans[inc], fill_color="red", line_color="red", source=x_rect_inc_src)
p.rect(x=time[inc], y=mids[inc], width=w, height=spans[inc], fill_color="red", line_color="red")
p.rect(x=time[dec], y=mids[dec], width=w, height=spans[dec], fill_color="green", line_color="green")
#p.segment(time[inc], highp[inc], time[inc], lowp[inc], color="red")
#p.segment(time[dec], highp[dec], time[dec], lowp[dec], color="green")
show(p)
