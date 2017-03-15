import numpy as np
import sys, os
import pandas as pd

if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]

    f = open(infile, 'r')
    fcontent = f.readlines()
    f.close()
    data_list = []
    time_list = []
    open_price_list = []
    close_price_list = []
    high_price_list = []
    low_price_list = []
    volume_list = []
    turnover_ratio_list = []
    money_list = []

    for line in fcontent:
        col_content = line.split(' ')
        if len(col_content) > 2:
            if col_content[3]=='INFO':
                time = col_content[0]
                open_price = float(col_content[5])
                close_price = float(col_content[6])
                high_price = float(col_content[7])
                low_price = float(col_content[8])
                volume = float(col_content[9])
                turnover_ratio = float(col_content[10])
                money = float(col_content[11])
                if volume==0.0 or np.isnan(volume) or turnover_ratio==0.0 or np.isnan(turnover_ratio):
                    continue
                else:
                    time_list.append(time)
                    open_price_list.append(open_price)
                    close_price_list.append(close_price)
                    high_price_list.append(high_price)
                    low_price_list.append(low_price)
                    volume_list.append(volume)
                    turnover_ratio_list.append(turnover_ratio)
                    money_list.append(money)
                    #data = {'Time':col_content[0], 'Open':open_price, 'Close':close_price, 'High':high_price, 'Low':low_price, 'Volume':volume, 'Turnover_ratio':turnover_ratio}
                    #data_list.append(data)

    s = pd.DataFrame({'Time':pd.Series(time_list), 'Open':pd.Series(open_price_list), 'Close':pd.Series(close_price_list), 'High':pd.Series(high_price_list), 'Low':pd.Series(low_price_list), 'Volume':pd.Series(volume_list), 'Turnover_ratio':pd.Series(turnover_ratio_list), 'Money':pd.Series(money_list)})
    #s = pd.Series(data_list)
    print s.columns
    s.to_csv(outfile)
