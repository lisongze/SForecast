import sys, os
import math
import numpy as np
import pandas as pd
import datetime
import operator


class SampleExtractor:
    def __init__(self, infile=''):
        self.time_format = '%Y-%m-%d'
        self.trade_start_day = '2005-01-04'
        self.trade_start_date = datetime.datetime.strptime(self.trade_start_day, self.time_format)
        self.new_stock_day_offset = 120
        self.halt_day_offset = 20
        self.up_ratio_thre1 = 0.02
        self.low_ratio_thre1 = 0.0
        self.up_ratio_thre2 = 0.05
        self.low_ratio_thre2 = -0.10
        self.hold_pro = 0.9
        self.sell_pro = 0.1
        self.close_position_ratio = -0.05
        self.history_days = 30
        self.forecast_days = 14
        self.day_stride = 1
        self.sample_len_thre = self.history_days + self.forecast_days
        self.tmax_thre = 0.10
        self.tmin_thre = -0.05

    def loadDataFromFile(self, infile):
        try:
            self.csv_content = pd.read_csv(infile, index_col=[0])
            #print self.csv_content.index
        except Exception, e:
            print Exception, ' : ', e

    def getOneDayData(self, index):
        time = self.csv_content.index[index]
        open_price = self.csv_content['Open'][index]
        close_price = self.csv_content['Close'][index]
        high_price = self.csv_content['High'][index]
        low_price = self.csv_content['Low'][index]
        volume = self.csv_content['Volume'][index]
        turnover_ratio = self.csv_content['Turnover_ratio'][index]
        money = self.csv_content['Money'][index]
        return time, open_price, close_price, high_price, low_price, volume, turnover_ratio ,money

    def getDataSegment(self):
        halt_epochs = []
        halt_start = False
        halt_end = False
        halt_start_index = 0
        halt_end_index = 0
        halt_days = 0
        for i in xrange(len(self.csv_content.index)):
            time, open_price, close_price, high_price, low_price, volume, turnover_ratio, money = self.getOneDayData(i)
            if self.isHalt(open_price, close_price, high_price, low_price, volume, turnover_ratio, money)==True:
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
            #print 'start: ', x['start'], ', end: ', x['end'], ', days: ', x['days']
        sample_end_index = len(self.csv_content.index) - 1
        sample = {'start': sample_start_index, 'end': sample_end_index, 'days': sample_end_index - sample_start_index + 1}
        samples.append(sample)

        raw_samples = [x for x in samples if x['days']>self.sample_len_thre]
        samples = []
        for i in range(0, len(raw_samples), 1):
            x = raw_samples[i]
            if x['days']>self.sample_len_thre + self.halt_day_offset:
                sample_start_index = x['start'] + self.halt_day_offset
                sample_end_index = x['end']
                days = sample_end_index - sample_start_index + 1
                sample = {'start': sample_start_index, 'end': sample_end_index, 'days': days}
                samples.append(sample)

        return samples

    def isHalt(self, open_price, close_price, high_price, low_price, volume, turnover_ratio, money):
        if open_price==close_price==high_price==low_price:
            return True
        elif volume<1e-6 or np.isnan(volume)==True:
            return True
        elif turnover_ratio<1e-6 or np.isnan(turnover_ratio)==True:
            return True
        elif money<1e-6 or np.isnan(money)==True:
            return True
        else:
            return False

    def normSample(self, history, forecast, sample_type):
        ref_open_price = history['Open'][-1]
        ref_close_price = history['Close'][-1]
        ref_high_price = history['High'][-1]
        ref_low_price = history['Low'][-1]
        ref_turnover_ratio = history['Turnover_ratio'][-1]
        ref_volume = history['Volume'][-1]
        ref_monry = history['Money'][-1]
        ref_date = history.index[-1]
        buy_in_price = (ref_high_price + ref_low_price) / 2.0

        history_norm = []
        forecast_norm = []

        for index, row in history.iterrows():
            norm_open_price = row['Open'] / ref_open_price
            norm_close_price = row['Close'] / ref_close_price
            norm_high_price = row['High'] / ref_high_price
            norm_low_price = row['Low'] / ref_low_price
            norm_turnover_ratio = row['Turnover_ratio'] / ref_turnover_ratio
            try:
                norm_volume = row['Volume'] / ref_volume
            except Exception, e:
                print '-------------', ref_date

            day_data = {'date': row.name, 'open': norm_open_price, 'close': norm_close_price, 'high': norm_high_price, 'low': norm_low_price, 'turnover_ratio': norm_turnover_ratio, 'volume': norm_volume}
            history_norm.append(day_data)

        for index, row in forecast.iterrows():
            norm_open_price = row['Open'] / ref_open_price
            norm_close_price = row['Close'] / ref_close_price
            norm_high_price = row['High'] / ref_high_price
            norm_low_price = row['Low'] / ref_low_price
            norm_turnover_ratio = row['Turnover_ratio'] / ref_turnover_ratio
            norm_volume = row['Volume'] / ref_volume

            day_data = {'date': row.name, 'open': norm_open_price, 'close': norm_close_price, 'high': norm_high_price, 'low': norm_low_price, 'turnover_ratio': norm_turnover_ratio, 'volume': norm_volume}
            forecast_norm.append(day_data)

        label = {'trade_date': ref_date, 'trade_price': buy_in_price,'history': history_norm, 'forecast': forecast_norm, 'class': sample_type}

        return label


    def doData(self, samples):
        data = []
        classes = []
        for x in samples:
            start_day_index = x['start']
            end_day_index = start_day_index + x['days'] #-self.sample_len_thre+1
            tmp_csv_content = self.csv_content.iloc[start_day_index : end_day_index]
            #filtered_csv_content = tmp_csv_content[(tmp_csv_content.Open==tmp_csv_content.Close==tmp_csv_content.High==tmp_csv_content.Low)==False]
            filtered_csv_content = tmp_csv_content.dropna()
            filtered_csv_content = filtered_csv_content[filtered_csv_content.Turnover_ratio>1e-6]
            filtered_csv_content = filtered_csv_content[filtered_csv_content.Volume>1e-6]
            for i in range(0, len(filtered_csv_content.index)-self.sample_len_thre, self.day_stride):
                history = filtered_csv_content.iloc[i+0 : i+self.history_days] 
                forecast = filtered_csv_content.iloc[i+self.history_days : i+self.history_days+self.forecast_days]
                sample_type = self.getSampleCls(history, forecast)
                d = self.normSample(history, forecast, sample_type)
                data.append(d)
                classes.append(sample_type)
            #for i in range(start_day_index, end_day_index, self.day_stride):
            #    history = self.csv_content.iloc[i+0 : i+self.history_days] 
            #    forecast = self.csv_content.iloc[i+self.history_days : i+self.history_days+self.forecast_days]
            #    sample_type = self.getSampleCls(history, forecast)
            #    d = self.normSample(history, forecast, sample_type)
            #    data.append(d)
            #    classes.append(sample_type)
        return data, classes

    def getSampleCls(self, history, forecast):
        cls = 1
        history_close_price = [float(x) for x in history['Close']]
        forecast_close_price = [float(x) for x in forecast['Close']]
        buy_in_price = ( float(history['High'][-1]) + float(history['Low'][-1]) ) / 2
        max_close_price_index, max_close_price_value = max(enumerate(forecast_close_price), key=operator.itemgetter(1))
        min_close_price_index, min_close_price_value = min(enumerate(forecast_close_price), key=operator.itemgetter(1))
        min_ratio = (min_close_price_value - buy_in_price) / buy_in_price
        max_ratio = (max_close_price_value - buy_in_price) / buy_in_price
        income_each_day = [(x - buy_in_price) for x in forecast_close_price]
        income_ratio_each_day = [(x / buy_in_price) for x in income_each_day]
        tmax_flag = False
        tmin_flag = False
        tmax_index = max_close_price_index
        tmax_ratio = max_ratio
        tmin_index = min_close_price_index
        tmin_ratio = min_ratio
        for i in xrange(self.forecast_days):
            if (i<max_close_price_index and income_ratio_each_day[i]>=self.tmax_thre):
                tmax_flag = True
                tmax_index = i
                tmax_ratio = income_ratio_each_day[i]
                break
        for i in xrange(self.forecast_days):
            if (i<min_close_price_index and income_ratio_each_day[i]<=self.tmin_thre):
                tmin_flag = True
                tmin_index = i
                tmin_ratio = income_ratio_each_day[i]
                break

        "calculate expect of income"
        pro_each_day = []
        for i in xrange(self.forecast_days-1):
            pro = math.pow(self.hold_pro, i) * self.sell_pro
            pro_each_day.append(pro)
        pro_each_day.append(pow(self.hold_pro, self.forecast_days-1))
        income_expect = 0
        for i in xrange(self.forecast_days):
            income_expect = income_expect + pro_each_day[i] * income_each_day[i]
        income_expect_ratio = income_expect / buy_in_price
        if (tmin_ratio < self.tmin_thre and tmin_index < tmax_index):
            return -1
        if income_expect_ratio <= self.low_ratio_thre1:
            cls = -1
        elif income_expect_ratio > self.low_ratio_thre1 and income_expect_ratio < self.up_ratio_thre1:
            cls = 0
        return cls

    def isNewStock(first_day):
        offset_day = first_day - trade_start_day
        if offset_day.days>0:
            return True
        return False


if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]
    extractor = SampleExtractor()
    extractor.loadDataFromFile(infile)
    samples = extractor.getDataSegment()
    data, label = extractor.doData(samples)

    rst_pd = pd.DataFrame(columns=['sample', 'class'])
    rst_pd['sample'] = data
    rst_pd['class'] = label
    #rst_pd.to_csv(infile + '.label.csv')
    rst_pd.to_csv(outfile)
