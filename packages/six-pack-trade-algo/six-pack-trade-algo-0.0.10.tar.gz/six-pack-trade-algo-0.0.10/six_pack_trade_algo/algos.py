import pandas as pd
import ta
from ta.utils import dropna
from datetime import datetime, timedelta
import time
import pickle

try:
    from .util import AlgoLogger
except:
    from util import AlgoLogger
#
#
#       Classes in algos
#
#           Algo
#           AlgoBb
#           AlgoRsi
#           AlgoRsiBb
#




class Algo:
    
    class Memory:
        def __init__(self, tickers, wallet, positions):
            self.tickers = tickers
            self.wallet = wallet
            self.positions = positions

    def __init__(self, data_path, data_source, GUID, wallet, tickers, tick_period):
        self.log = AlgoLogger(data_path=data_path)
        self.log.set_name(GUID)
        self.data_source = data_source
        self.GUID = GUID
        self.wallet = wallet
        self.tickers = tickers
        self.tick_period = tick_period
        self.test_mode = True
        self.positions = {}
        for t in self.tickers:
            self.positions[t] = 0
        self.mem_file = data_path + "algo_mem/{}.pkl".format(GUID)

    def _buy(self, ticker, quantity, price):
        price = float(self._get_last_trade(ticker))*float(quantity)
        if self.wallet > price:
            # orders = self.data_source.list_orders
            # for order in orders:
            #     qty = self.positions[ticker]
            #     self.positions[ticker] -= quantity
            #     self.wallet += price

            if not self.test_mode:
                self.data_source.submit_order(
                ticker=ticker,
                quantity=quantity,
                side='buy',
                type='limit',
                limit_price=self._get_last_trade(ticker),
                time_in_force='gtc'
                )
            self.positions[ticker] += quantity
            self.wallet -= price
            self.log.trade("Wallet Value: {}       -{}".format(self.wallet, price))
        else:
            self.log.warn(" ! NOT ENOUGH MONEY ! Wallet Value: {}".format(self.wallet))

    def _sell(self, ticker, quantity, price):
        price = float(self._get_last_trade(ticker))*float(quantity)
        
        if self.positions[ticker] >= quantity:
            if not self.test_mode:
                self.data_source.submit_order(
                ticker=ticker,
                quantity=quantity,
                side='sell',
                type='limit',
                limit_price=self._get_last_trade(ticker),
                time_in_force='gtc'
                )
            self.positions[ticker] -= quantity
            self.wallet += price
            self.log.trade("Wallet Value: {}       +{}".format(self.wallet, price))
        else:
            self.log.warn(" ! NOT ENOUGH SHARES ! Wallet Value: {}".format(self.wallet))
            
    def _get_last_trade(self, ticker):
        return float(self.data_source.get_last_trade(ticker)["price"])

    def save_algo(self):
        try:
            if self.test_mode: raise Exception("Test mode on. No Saving.")
            fs = open(self.mem_file ,"wb")
            to_save = self.Memory(self.tickers, self.wallet, self.positions)
            pickle.dump(to_save,fs)
            fs.close()
        except Exception as e:
            self.log.error("Cannot save algo: ")
            self.log.error(e)

    def load_algo(self):
        if "test" in self.GUID.lower():
            self.log.warn("Running test algo. Ignoring .pkl save...")
            return
        try:
            fs = open(self.mem_file ,"rb")
            from_save = pickle.load(fs)
            if self.tickers != from_save.ticker:
                raise Exception("Incompatable ticker found in mem. Resetting...")
            self.wallet = from_save.wallet
            self.positions = from_save.positions
            self.log.info("Found Memory||     wallet:{}".format(self.wallet))
            fs.close()
        except Exception as e:
            self.log.warn("Cannot load algo. Creating a mem file...")
            self.save_algo()
    
    def run(self):
        self.log.info("STARTED ALGO:  " + self.GUID)
        if not bool(self.data_source.get_clock()["is_open"]):
            self.log.warn("Market is closed")
        else:
            self.log.info("Market is open")
        self.load_algo()
        self.log.output()
        
    def run_end(self):
        self.log.info("Market is closed. Saving wallet data...")
        self.save_algo()
        self.log.output()

class AlgoBb(Algo):
    
    def __init__ (self, data_path, data_source,  GUID, wallet, ticker, tick_period, algo_params):
        super().__init__(data_path, data_source, GUID,  wallet, ticker, tick_period)
        self.points = algo_params[0]
        self.stddev = algo_params[1]
        self.buy_percent = algo_params[2]
        self.sell_percent = algo_params[3]
        self.buy_qty = {}
        self.init_buy_price = {}
        self.init_buy = {}
        for t in ticker:
            self.buy_qty[t] = int( (wallet*self.buy_percent) / float(self._get_last_trade(t)))
            if self.buy_qty[t] < 1:
                self.buy_qty[t] = 1
            self.init_buy_price[t] = 0
            self.init_buy[t] = True

    def run(self, return_dict):
        super().run()
        trades = {}
        while bool(self.data_source.get_clock()["is_open"]):
            for t in self.tickers:
                try:
                    trades[t] += [self._get_last_trade(t)]
                except Exception as e:
                    trades[t] = [self._get_last_trade(t)]
                try:
                    if len(trades[t]) > self.points:
                        if self.test_mode: time.sleep(1)
                        trades_df = pd.DataFrame(trades[t],columns=['intraday'])
                        bollingerBands = self.generateBollingerBands(trades_df['intraday'])
                        try:
                            self.trade(t, bollingerBands)
                        except Exception as e:
                            self.log.error("Trade error: {}, {}".format(t, e))
                    else:
                        self.log.info("Init trades {}: {}".format(t, 100*len(trades[t])/30))
                except Exception as e:
                    self.log.error("dataframe issue?: {}".format(e))
            self.log.output()
            if self.test_mode:
                time.sleep(0.5)
            else:
                time.sleep(30)
        super().run_end()
        return_dict[self.GUID] = (self.wallet, self.positions)

    
    def generateBollingerBands(self, df):
        bollingerBands = ta.volatility.BollingerBands(df, n = self.points, ndev=self.stddev)
        return bollingerBands

        

    def trade(self, ticker, bollingerBands):
        if(bollingerBands.bollinger_hband_indicator().tail(1).iloc[0]):
            self.log.info("Current BB: {}  is above the high band".format(ticker))
            self.sell_proportional(ticker)
        elif(bollingerBands.bollinger_lband_indicator().tail(1).iloc[0]):
            self.log.info("Current BB: {}  is below the low band".format(ticker))
            self.buy_shares(ticker)
        else:
            self.log.info("Current BB: {}  is inbetween bollinger bands".format(ticker))

    # try to sell off % of current holdings unless you've made a high percentage then sell off all. Ride the wave of high prices for a couple extra ticks
    def sell_proportional(self, ticker):
        ba_pos = self.data_source.get_position(ticker)
        try:
            if int(ba_pos["qty"]) <= 30:
                qty = int(ba_pos["qty"])
            else:
                qty = int(float(ba_pos["qty"])*(self.sell_percent))
            self.log.info("Sell Partial: {}".format(qty))
            self._sell(ticker, qty, 0)
        except Exception as e:
            self.log.error("Sell proportional error: {} ".format(e))
            
    def buy_shares(self, ticker):

        # Make sure that the current wallet value - (buy price * qty + 1%)  > 25,000
        balance = float(self.data_source.get_account()["cash"])
        total_cost = float(self._get_last_trade(ticker)) * self.buy_qty[ticker]
        if (balance - (total_cost * 1.01)> 25000.0):
            self._buy(ticker, self.buy_qty[ticker],0)
            self.log.info("BUY {}".format(self.buy_qty[ticker]))
        else:
            try:
                self.log.info("Can't buy more. BAL / COST  : {} / {}".format(balance,total_cost))
            except Exception as e:
                self.log.error("ALGO BB buy_shares: {}".format(e))


class AlgoRsi(Algo):
    # The algo will attempt to spend roughly this percent of its buying power on shares per trade.
    # EX:    wallet = 5,000; buy percent= .15; BA is trading at 280. Thus the algo will buy 2 shares per trade.
    #        15% of 5000 = 750 
    #        int(750/280)= 2
    
    def __init__ (self, data_path, data_source, GUID, wallet, tickers, tick_period, algo_params):
        super().__init__(data_path, data_source,  GUID, wallet, tickers, tick_period)
        self.RSIs = pd.DataFrame(columns=['time', 'rsi'])
        self.rsi_high = float(algo_params[0])
        self.rsi_low = float(algo_params[1])
        self.buy_percent = float(algo_params[2])
        self.sell_percent = float(algo_params[3])
        self.buy_qty = {}
        self.init_buy_price = {}
        self.init_buy = {}
        self.prev_rsi = {}
        self.period = 5
        for t in tickers:
            self.buy_qty[t] = int( (wallet*self.buy_percent) / float(self._get_last_trade(t)))
            if self.buy_qty[t] < 1:
                self.buy_qty[t] = 1
            self.init_buy_price[t] = 0
            self.init_buy[t] = True
            self.prev_rsi[t] = 0

    def run(self, return_dict):
        super().run()
        trades = {}
        while bool(self.data_source.get_clock()["is_open"]):
            for t in self.tickers:
                
                try:
                    trades[t] += [self._get_last_trade(t)]
                except Exception as e:
                    trades[t] = [self._get_last_trade(t)]

                try:
                    if len(trades[t]) > self.period:
                        trades_df = pd.DataFrame(trades[t],columns=['intraday'])
                        
                        trades_df = self.generateRsiIndicator(trades_df['intraday'])

                        try:
                            self.trade(t, trades_df.tail(1).iloc[0])
                        except Exception as e:
                            self.log.error("Trade error: {}, {}".format(t, e))
                            
                        del trades[t][0]
                        
                    else:
                        self.log.info("Init trades {}: {}".format(t,100*len(trades[t])/self.period))
                except Exception as e:
                    self.log.error("dataframe issue?: {}".format(e))
            self.log.output()
            self.data_source.step(self.tick_period)
        super().run_end()
        return_dict[self.GUID] = (self.wallet, self.positions)

    
    def generateRsiIndicator(self, column):
        # rsi = ta.momentum.rsi(column, n = 1)
        rsi = ta.momentum.rsi(column, n = self.period)
        self.graph_rsi(rsi)
        return rsi
        # TODO: try adding mfi instead of rsi
        
    def graph_rsi(self, rsi):
        # f = plt.figure()
        # rsi_graph = f.add_subplot('rsi')
        # rsi.dropna()
        # rsi.plot(kind='line')
        # plt.show()
        # plt.hide()
        # time = int((datetime.today() ).strftime('%Y%m%d'))
        # new_row = {'time':time, 'rsi':rsi}
        # RSIs.append(new_row)
        # RSIs.plot(x='time',y='rsi',kind='line')
        # plt.show()
        # plt.close()
        pass
        
    def trade(self, ticker, cur_rsi):
        self.log.info("Current RSI: {}      {}".format(cur_rsi, cur_rsi-self.prev_rsi[ticker]))
        self.prev_rsi[ticker] = cur_rsi
        if cur_rsi > self.rsi_high:
            # sell_all_shares()
            self.sell_proportional(ticker)
        if cur_rsi < self.rsi_low:
            self.buy_shares(ticker)
    
    # try to sell of % of current holdings unless you've made a high percentage then sell off all. Ride the wave of high prices for a couple extra ticks
    def sell_proportional(self, ticker):
        ba_pos = self.data_source.get_position(ticker)
        # if (not algo_mem.init_buy and float(ba_pos.current_price)/float(algo_mem.init_buy_price) >= 1.05):
        #     log.info("Sell All : {}".format(ba_pos.qty))
        #     # sell_all_shares()
        
        # TODO: this
        # self.sell_clear_orders(ticker)
        
        try:
            if int(ba_pos["qty"]) <= 30:
                qty = int(ba_pos["qty"])
                self.log.info("Sell Remaining: {}".format(qty))
            else:
                qty = int(float(ba_pos["qty"])*(self.sell_percent))
                self.log.info("Sell Partial: {}".format(qty))
            self._sell(ticker, qty, 0)
        except Exception as e:
            self.log.error("Sell proportional error: {} ".format(e))
            
    def sell_clear_orders(self, ticker):
        self.log.info("sell_clear_orders")
        orders = self.data_source.list_orders(ticker)
        self.log.info(orders)
        
        
    def sell_all_shares(self, ticker):
        ba_pos = self.data_source.get_position(ticker)
        try:
            self._sell(ticker, ba_pos["qty"], 0)
            self.init_buy[ticker] = True
        except Exception as e:
            self.log.error("Sell all shares error: {} ".format(e))
    
    def buy_shares(self, ticker):
        if self.init_buy[ticker]:
            self.init_buy[ticker] = False
            self.init_buy_price[ticker] = float(self._get_last_trade(ticker))
        
        # Make sure that the current wallet value - (buy price * qty + 1%)  > 25,000
        balance = float(self.data_source.get_account()["cash"])
        total_cost = self.init_buy_price[ticker] * self.buy_qty[ticker]
        if (balance - (total_cost * 1.01)> 25000.0):
            self._buy(ticker, self.buy_qty[ticker],0)
            self.log.info("BUY {}".format(self.buy_qty[ticker]))
        else:
            try:
                self.log.info("Can't buy more. BAL / COST  : {} / {}".format(balance,total_cost))
            except Exception as e:
                self.log.error("ALGO RSI buy_shares: {}".format(e))



class AlgoRsiBb(Algo):
        
    def __init__ (self, data_path, data_source, GUID,  wallet, tickers, tick_period, algo_params):
        super().__init__(data_path, data_source, GUID,  wallet, tickers, tick_period)
        self.points = int(algo_params[0])
        self.stddev = float(algo_params[1])
        self.rsi_high = float(algo_params[2])
        self.rsi_low = float(algo_params[3])
        self.buy_percent = float(algo_params[4])
        self.sell_percent = float(algo_params[5])
        self.bollinger_indicator = {}
        self.buy_qty = {}
        self.init_buy_price = {}
        self.init_buy = {}
        self.prev_rsi = {}
        for t in tickers:
            self.buy_qty[t] = int( (wallet*self.buy_percent) / float(self._get_last_trade(t)))
            if self.buy_qty[t] < 1:
                self.buy_qty[t] = 1
            self.init_buy_price[t] = 0
            self.init_buy[t] = True
            self.bollinger_indicator[t] = "Middle"

    def run(self, return_dict):
        super().run()
        trades = {}
        while bool(self.data_source.get_clock()["is_open"]):
            for t in self.tickers:
                try:
                    trades[t] += [self._get_last_trade(t)]
                except Exception as e:
                    trades[t] = [self._get_last_trade(t)]
                try:
                    if len(trades[t]) > self.points:
                        trades_df = pd.DataFrame(trades[t],columns=['intraday'])
                        rsi = self.generateRsiIndicator(trades_df['intraday'])
                        bollingerBands = self.generateBollingerBands(trades_df['intraday'])
                        try:
                            self.trade(t, bollingerBands, rsi)
                        except Exception as e:
                            self.log.error("Trade error: {}, {}".format(t, e))
                    else:
                        self.log.info("Init trades {}: {}".format(t, 100*len(trades[t])/self.points))
                except Exception as e:
                    self.log.error("dataframe issue?: {}".format(e))
            self.log.output()
            self.data_source.step(self.tick_period)
        super().run_end()
        return_dict[self.GUID] = (self.wallet, self.positions)

    
    def generateBollingerBands(self, df):
        bollingerBands = ta.volatility.BollingerBands(df, n = self.points, ndev=self.stddev)
        return bollingerBands
  
    def generateRsiIndicator(self, df):
        rsi = ta.momentum.rsi(df, n = self.points)
        return rsi

    def trade(self, ticker, bollingerBands, rsi):
        if(bollingerBands.bollinger_hband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is above bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Above"  
        elif(bollingerBands.bollinger_lband_indicator().tail(1).iloc[0]):
            self.log.info("Current RSI_BB: {}  is below bollinger bands".format(ticker))
            self.bollinger_indicator[ticker] = "Below"
        else:
            self.log.info("Current RSI_BB: {}  is inbetween bollinger bands; Checking RSIs : {} ".format(ticker, rsi.tail(1).iloc[0]))
            if ((rsi.tail(1).iloc[0] > 50) and (self.bollinger_indicator[ticker] == "Below")) or (rsi.tail(1).iloc[0] > self.rsi_high):
                self.buy_shares(ticker)
            elif ((rsi.tail(1).iloc[0] < 50) and (self.bollinger_indicator[ticker] == "Above")) or (rsi.tail(1).iloc[0] > self.rsi_low):
                self.sell_proportional(ticker)
            self.bollinger_indicator[ticker] = "Middle"

    # try to sell off % of current holdings unless you've made a high percentage then sell off all. Ride the wave of high prices for a couple extra ticks
    def sell_proportional(self, ticker):
        try:
            self.log.info("sell_proportional {}".format(ticker))
            pos = self.data_source.get_position(ticker)
            if pos["qty"] == 0:
                self.log.info("sell_proportional no shares to sell")
                return
            if int(pos["qty"]) <= 30:
                qty = int(pos["qty"])
            else:
                qty = int(float(pos["qty"])*(self.sell_percent))
            self._sell(ticker, qty, 0)
            self.log.info("SELL Partial {} shares of {}".format(qty, ticker))
        except Exception as e:
            self.log.error("sell_proportional error: {} ".format(e))
            
    def buy_shares(self, ticker):
        try:
            self.log.info("buy_shares {}".format(ticker))
            # Make sure that the current wallet value - (buy price * qty + 1%)  > 25,000
            balance = float(self.data_source.get_account()["cash"])
            total_cost = float(self._get_last_trade(ticker)) * self.buy_qty[ticker]
            if (balance - (total_cost * 1.01)> 25000.0):
                self._buy(ticker, self.buy_qty[ticker],0)
                self.log.info("BUY {} shares of {}".format(self.buy_qty[ticker], ticker))
            else:
                raise Exception("Not enough wallet value. Cost:{} / Balance:{}".format(total_cost, balance))
        except Exception as e:
            self.log.info("buy_shares error: {}".format(e))
            
                        

