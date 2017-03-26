import sys, os
import numpy as np
import pandas as pd
import datetime

def isHalt(open_price, close_price, high_price, low_price):
    if open_price==close_price==high_price==low_price:
        return True
    else:
        return False

if __name__ == '__main__':
    infile = sys.argv[1]
    csv_content = pd.read_csv(infile, index_col=[0])
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

    samples = [x for x in samples if x['days']>sample_len_thre]
    for x in samples:
        print 'start: ', x['start'], ', end: ', x['end'], ', days: ', x['days']
