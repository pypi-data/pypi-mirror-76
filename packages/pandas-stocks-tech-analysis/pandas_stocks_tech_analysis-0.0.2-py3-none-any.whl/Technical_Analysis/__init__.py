from tqdm import tqdm
import pandas as pd
from nsepy import get_history
from datetime import datetime,date,timedelta
import os
import numpy as np
class technical_indicators:

    def __init__(self):
        pass

    def fetch_company_historical_price(self,symbol,start_date,end_date):
        """This is a function that fetch the data from BSE API.

        Parameters
        ----------
        symbol : type
            This is the company symbol.
        start_date : type
            This is starting date.
        end_date : type
            This is the Ending data.

        Returns
        -------
        type
            Return the stock data.

        """
        self.symbol,self.start_date,self.end_date = symbol,start_date,end_date
        # end_date = '2020-02-05'
        def change_value(Prev_Close,close):
            return np.round(((close - Prev_Close)*100)/Prev_Close,2)

        start = datetime.strptime(str(start_date),'%Y-%m-%d') - timedelta(200)
        end = datetime.strptime(str(end_date),'%Y-%m-%d')
        try:
            data = get_history(symbol= symbol, start=start, end=end)
            data = data.reset_index()
            data["Date"] = data["Date"].apply(lambda x:datetime.strftime(datetime.strptime(str(x),'%Y-%m-%d'),'%Y%m%d'))
            data['Change %'] = np.vectorize(change_value)(data['Prev Close'],data['Close'])
            return data
        except:
            print('not found data for company symbol ')
            return 0

    def rsi(self,data):
        """This is the that calculate the rsi .

        Parameters
        ----------
        data : type
            pass the stock data to calculate the rsi.

        Returns
        -------
        type
            Description of returned object.

        """
        # data = self.fetch_company_historical_price(self.symbol,self.start_date,self.end_date)
        close = data["Close"]
        delta = close.diff()


        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # Calculate the EWMA
        roll_up1 = up.ewm(span=14).mean()
        roll_down1 = down.abs().ewm(span=14).mean()

        # Calculate the RSI based on EWMA
        RS1 = roll_up1 / roll_down1
        RSI1 = 100.0 - (100.0 / (1.0 + RS1))
        data['rsi'] = RSI1
        return data


    def sma(self,data,day):
        """Short summary.

        Parameters
        ----------
        data : type
            Description of parameter `data`.
        day : type
            Description of parameter `day`.

        Returns
        -------
        type
            Description of returned object.

        """
        data['sma_{}'.format(day)] = data["Close"].rolling(int(day)).mean()
        return data

    def ema(self,data,day):
        """Short summary.

        Parameters
        ----------
        data : type
            Description of parameter `data`.
        day : type
            Description of parameter `day`.

        Returns
        -------
        type
            Description of returned object.

        """
        data['ema_{}'.format(day)] = pd.Series.ewm(data['Close'], span=int(day)).mean()
        return data




# b = technical_indicators()
# data = technical_indicators().fetch_company_historical_price('RELIANCE','2015-01-01','2020-01-01')
# data =  b.rsi(data)
# data =  b.sma(data,5)
# data =  b.ema(data,10)
