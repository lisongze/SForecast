import sys, os
import math
import numpy as np
import pandas as pd
import datetime

trade_start_day = datetime.datetime.strptime('2015-01-04', '%Y-%m-%d')
new_stock_day_offset = 120
halt_day_offset = 20
up_ratio_thre1 = 0.15
low_ratio_thre1 = -0.05
up_ratio_thre2 = 0.05
low_ratio_thre2 = -0.15

def isHalt(open_price, close_price, high_price, low_price):
    if open_price==close_price==high_price==low_price:
        return True
    else:
        return False

def getSampleType(history, forecast):
    label = 1
    history_close_price = [float(x) for x in history['Close']]
    forecast_close_price = [float(x) for x in forecast['Close']]
    reference_price = history_close_price[-1]
    if (max(forecast_close_price)-reference_price) / reference_price > up_ratio_thre1 and (min(forecast_close_price)-reference_price) / reference_price < low_ratio_thre1:
        label = 1
    else:
        label = 0
    '''
    if (max(forecast_close_price)-reference_price) / reference_price < up_ratio_thre2 and (min(forecast_close_price)-reference_price) / reference_price > low_ratio_thre2:
        label = -1
    '''
    return label

def doLabel(history, forecast, sample_type):
    ref_open_price = history['Open'][-1]
    ref_close_price = history['Close'][-1]
    ref_high_price = history['High'][-1]
    ref_low_price = history['Low'][-1]
    ref_turnover_ratio = history['Turnover_ratio'][-1]
    ref_volumn = history['Volume'][-1]

    history_norm = []
    forecast_norm = []
    '''
    history_norm_open_price = []
    history_norm_close_price = []
    history_norm_high_price = []
    history_norm_low_price = []
    history_norm_turnover_ratio = []
    history_norm_volumn = []

    forecast_norm = []
    forecast_norm_open_price = []
    forecast_norm_close_price = []
    forecast_norm_high_price = []
    forecast_norm_low_price = []
    forecast_norm_turnover_ratio = []
    forecast_norm_volumn = []
    '''
    
    for index, row in history.iterrows():
        norm_open_price = row['Open'] / ref_open_price
        norm_close_price = row['Close'] / ref_close_price
        norm_high_price = row['High'] / ref_high_price
        norm_low_price = row['Low'] / ref_low_price
        norm_turnover_ratio = row['Turnover_ratio'] / ref_turnover_ratio
        norm_volumn = row['Volume'] / ref_volumn

        day_data = {'open': norm_open_price, 'close': norm_close_price, 'high': norm_high_price, 'low': norm_low_price, 'turnover_ratio': norm_turnover_ratio, 'volumn': norm_volumn}
        history_norm.append(day_data)

        '''
        history_norm_open_price .append(norm_open_price)
        history_norm_close_price.append(norm_close_price)
        history_norm_high_price.append(norm_high_price)
        history_norm_low_price.append(norm_low_price)
        history_norm_turnover_ratio.append(norm_turnover_ratio)
        history_norm_volumn.append(norm_volumn)
        '''

    for index, row in forecast.iterrows():
        norm_open_price = row['Open'] / ref_open_price
        norm_close_price = row['Close'] / ref_close_price
        norm_high_price = row['High'] / ref_high_price
        norm_low_price = row['Low'] / ref_low_price
        norm_turnover_ratio = row['Turnover_ratio'] / ref_turnover_ratio
        norm_volumn = row['Volume'] / ref_volumn

        day_data = {'open': norm_open_price, 'close': norm_close_price, 'high': norm_high_price, 'low': norm_low_price, 'turnover_ratio': norm_turnover_ratio, 'volumn': norm_volumn}
        forecast_norm.append(day_data)

        '''
        forecast_norm_open_price .append(norm_open_price)
        forecast_norm_close_price.append(norm_close_price)
        forecast_norm_high_price.append(norm_high_price)
        forecast_norm_low_price.append(norm_low_price)
        forecast_norm_turnover_ratio.append(norm_turnover_ratio)
        forecast_norm_volumn.append(norm_volumn)
        '''

    label = {'history': history_norm, 'forecast': forecast_norm, 'class': sample_type}

    return label

def isNewStock(first_day):
    offset_day = first_day - trade_start_day
    if offset_day.days>0:
        return True
    return False

if __name__ == '__main__':
    infile = sys.argv[1]
    csv_content = pd.read_csv(infile, index_col=[0])
    first_day = datetime.datetime.strptime(csv_content.index[0],'%Y-%m-%d')
    if isNewStock(first_day)==True:
        csv_content = csv_content.icol[new_stock_day_offset:]
    date = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in csv_content.index]
    sample_len_thre = 44
    epoch_start = x[0]
    epoch_end = x[0]
    halt_epochs = []
    halt_start = False
    halt_end = False
    halt_start_index = 0
    halt_end_index = 0
    halt_days = 0
    for i in xrange(len(date)):
        open_price = csv_content['Open'][i]
        close_price = csv_content['Close'][i]
        high_price = csv_content['High'][i]
        low_price = csv_content['Low'][i]
        if isHalt(open_price, close_price, high_price, low_price)==True:
            if halt_start==False:
                halt_start = True
                halt_start_index = i
                halt_end_index = i
                halt_days = halt_days + 1
            else:
                halt_end_index = i
                halt_days = halt_days + 1
        else:
            if halt_start==True:
                halt = {'start': halt_start_index, 'end': halt_end_index, 'days': halt_days}
                halt_start = False
                halt_days = 0
                halt_epochs.append(halt)
    
    halt_epochs = [x for x in halt_epochs if x['days']>3]
    sample_start_index = 0
    sample_end_index = 0
    samples = []
    for x in halt_epochs:
        sample_end_index = x['start']
        sample = {'start': sample_start_index, 'end': sample_end_index, 'days': sample_end_index - sample_start_index + 1}
        samples.append(sample)
        sample_start_index = x['end']
        print 'start: ', x['start'], ', end: ', x['end'], ', days: ', x['days']
    sample_end_index = len(csv_content.index) - 1
    sample = {'start': sample_start_index, 'end': sample_end_index, 'days': sample_end_index - sample_start_index + 1}
    samples.append(sample)

    raw_samples = [x for x in samples if x['days']>sample_len_thre]
    samples = []
    for i in range(1, len(raw_samples), 1):
        x = raw_samples[i]
        if x['days']>sample_len_thre+halt_day_offset:
            sample_start_index = x['start'] + halt_day_offset
            sample_end_index = x['end']
            days = sample_end_index - sample_start_index + 1
            sample = {'start': sample_start_index, 'end': sample_end_index, 'days': days}
            samples.append(sample)
    for x in samples:
        print 'start: ', x['start'], ', end: ', x['end'], ', days: ', x['days']

    day_stride = 1
    history_days = 30
    forecast_days = 14
    labels = []
    for x in samples:
        end_day_index = x['days']-sample_len_thre+1
        for i in range(0, end_day_index, day_stride):
            history = csv_content.iloc[i+0 : i+history_days] 
            forecast = csv_content.iloc[i+history_days : i+history_days+forecast_days]
            sample_type = getSampleType(history, forecast)
            if sample_type==1 or sample_type==2:
                label = doLabel(history, forecast,sample_type)
                label_history = label['history']
                for x in label_history:
                    print str(x) + ' '
                print '-------------------------------'
                labels.append(label)
