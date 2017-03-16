content = """#coding=utf-8

from kuanke.user_space_api import *

class trade_stat():
    def __init__(self):
        self.trade_total_count = 0
        self.trade_success_count = 0
        self.statis = {'win': [], 'loss': []}
        
    def reset(self):
        self.trade_total_count = 0
        self.trade_success_count = 0
        self.statis = {'win': [], 'loss': []}
    
    # 记录交易次数便于统计胜率
    # 卖出成功后针对卖出的量进行盈亏统计
    def watch(self, stock, sold_amount, avg_cost, cur_price):
        self.trade_total_count += 1
        current_value = sold_amount * cur_price
        cost = sold_amount * avg_cost

        percent = round((current_value - cost) / cost * 100, 2)
        if current_value > cost:
            self.trade_success_count += 1
            win = [stock, percent]
            self.statis['win'].append(win)
        else:
            loss = [stock, percent]
            self.statis['loss'].append(loss)
        
    def report(self, context):
        cash = context.portfolio.cash
        totol_value = context.portfolio.portfolio_value
        position = 1 - cash/totol_value
        log.info("收盘后持仓概况:%s" % str(list(context.portfolio.positions)))
        log.info("仓位概况:%.2f" % position)
        self.print_win_rate(context.current_dt.strftime("%Y-%m-%d"), context.current_dt.strftime("%Y-%m-%d"), context)

    # 打印胜率
    def print_win_rate(self, current_date, print_date, context):
        if str(current_date) == str(print_date):
            win_rate = 0
            if 0 < self.trade_total_count and 0 < self.trade_success_count:
                win_rate = round(self.trade_success_count / float(self.trade_total_count), 3)

            most_win = self.statis_most_win_percent()
            most_loss = self.statis_most_loss_percent()
            starting_cash = context.portfolio.starting_cash
            total_profit = self.statis_total_profit(context)
            if len(most_win)==0 or len(most_loss)==0:
                return

            print "-"
            print '------------绩效报表------------'
            print '交易次数: {0}, 盈利次数: {1}, 胜率: {2}'.format(self.trade_total_count, self.trade_success_count, str(win_rate * 100) + str('%'))
            print '单次盈利最高: {0}, 盈利比例: {1}%'.format(most_win['stock'], most_win['value'])
            print '单次亏损最高: {0}, 亏损比例: {1}%'.format(most_loss['stock'], most_loss['value'])
            print '总资产: {0}, 本金: {1}, 盈利: {2}, 盈亏比率：{3}%'.format(starting_cash + total_profit, starting_cash, total_profit, total_profit / starting_cash * 100)
            print '--------------------------------'
            print "-"

    # 统计单次盈利最高的股票
    def statis_most_win_percent(self):
        result = {}
        for statis in self.statis['win']:
            if {} == result:
                result['stock'] = statis[0]
                result['value'] = statis[1]
            else:
                if statis[1] > result['value']:
                    result['stock'] = statis[0]
                    result['value'] = statis[1]

        return result

    # 统计单次亏损最高的股票
    def statis_most_loss_percent(self):
        result = {}
        for statis in self.statis['loss']:
            if {} == result:
                result['stock'] = statis[0]
                result['value'] = statis[1]
            else:
                if statis[1] < result['value']:
                    result['stock'] = statis[0]
                    result['value'] = statis[1]

        return result

    # 统计总盈利金额    
    def statis_total_profit(self, context):
        return context.portfolio.portfolio_value - context.portfolio.starting_cash"""

# 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    #write_file('tradestat.py', content)
    g.tmp = get_price('000004.XSHE', '2011-01-01 10:00:00', '2016-01-01 10:00:00')
    g.count = 0

# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    #print g.tmp[g.count]
    #df = get_price('000004.XSHE', '2011-01-01 10:00:00', '2017-01-01 10:00:00')[g.count:g.count+1]
    df = get_price('000505.XSHE', end_date=context.current_dt, count=1)
    q = query(valuation).filter(valuation.code == '000505.XSHE')
    dff = get_fundamentals(q, context.current_dt)
    turnover_ratio = dff['turnover_ratio'][0]
    open_price = df['open'][0]
    close_price = df['close'][0]
    high_price = df['high'][0]
    low_price = df['low'][0]
    volume = df['volume'][0]
    money = df['money'][0]
    print str(open_price) + " " + str(close_price) + " " + str(high_price) + " " + str(low_price) + " " + str(volume) + " " + str(turnover_ratio) + " " + str(money)
    g.count = g.count + 1
    
