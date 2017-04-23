import pandas as pd
import numpy as np
import os, sys

def read_label(label_file):
    csv_content = pd.read_csv(label_file)
    sample = csv_content['sample']
    sample = [eval(x) for x in sample]
    print sample[0]
    '''
    cls = csv_content['class']

    data = []
    label = []
    for i in xrange(len(sample)):
        history = sample[i]['history']
        d = np.zeros((6,len(history)))
        l = np.zeros(2)
        if (cls[i]==1):
            l[1] = 1
        else:
            l[0] = 1
        for j in xrange(len(history)):
            d[0][j] = history[j]['open']
            d[1][j] = history[j]['close']
            d[2][j] = history[j]['high']
            d[3][j] = history[j]['low']
            d[4][j] = history[j]['turnover_ratio']
            d[5][j] = history[j]['volume']
        data.append(d)
        label.append(l)
    rst_data = np.asarray(data)
    rst_label = np.asarray(label)
    return rst_data, rst_label
    '''
