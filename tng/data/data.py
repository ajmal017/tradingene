import os
from time import time
import numpy as np
import pandas as pd
import datetime
import urllib.request
import json
from tng.algorithm_backtest.limits import instrument_ids

dt = np.dtype({
    'names': ['time', 'open', 'high', 'low', 'close', 'vol'],
    'formats':
    ['uint64', 'float64', 'float64', 'float64', 'float64', 'float64']
})
""" np.dtype: Numpy dtype of signle minute candle stored from history data.

    Single element of history consists of the following fields:
        time (uint64): Open time of a minute candle.
        open (float64): Open price of a minute candle.
        high (float64): The highest price of a minute candle.
        low (float64): The lowest price of a minute candle.
        close (float64): Close price of a minute candle.
        vol (float64): Volume of a minute candle.
"""


class Data:
    """ Class for loading instrument history. """

    def __init__(self):
        pass

    @classmethod
    def load_data(cls, filename, start_date, end_date):
        """ Loads file from the drive and returns history data. 
        
            Arguments:
                filename (str): Name of the asset. Its history will
                    be loaded from .csv file.
                start_date (datetime.datetime): From this timestamp data
                    will be loaded.
                end_date (datetime.datetime): Till this timestamp data
                    will be loaded.

            Returns:
                hist_data(np.record): Numpy array of minute candles.
        """

        def find_start_end(all_data, start_date, end_date):
            while True:
                start = all_data[all_data['time'] == start_date].index.values
                if len(start):
                    start = int(start)
                    break
                else:
                    #works only if the first candle is in start day -- correct
                    start_date += 100
            while True:
                end = all_data[all_data['time'] == end_date].index.values
                if len(end):
                    end = int(end)
                    break
                else:
                    end_date += 100
            return start, end

        start_date = int(start_date.strftime("%Y%m%d%H%M%S"))
        end_date = int(end_date.strftime("%Y%m%d%H%M%S"))
        req_start_date = start_date * 1000
        req_end_date = end_date * 1000
        if filename in instrument_ids.keys():
            instr_id = instrument_ids[filename]
        else:
            raise ValueError("Instrument {} was not found!".format(filename))
        url = "https://candles.tradingene.com/candles?instrument_id=" + \
              str(instr_id)+"&from="+str(req_start_date)+"&to="+str(req_end_date)

        # data = urllib.request.urlopen(url).read()
        # obj = json.loads(data)
        # np_data = np.empty(len(obj), dtype = dt)
        # for i, elem in enumerate(obj):
        #     np_data[i] = np.array([
        #         (int(elem['time'])//1000,
        #         float(elem['open']),
        #         float(elem['high']),
        #         float(elem['low']),
        #         float(elem['close']),
        #         float(elem['volume']))], dtype = dt)
        current_path = os.path.abspath(__file__)
        append_path = os.path.abspath(
            os.path.join(current_path, '../../history_data/')) + "/"
        extension = ".csv"
        all_data = pd.read_csv(append_path + filename + extension)
        start, end = find_start_end(all_data, start_date, end_date)
        hist_data = all_data.iloc[start:end]
        hist_data = hist_data[::-1]
        hist_data = hist_data.to_records(index=False)
        #np_data = pd.DataFrame(np_data[:-1][::-1]).to_records(index = False)
        
        # КОСТЫЛЬ!
        # for i in range(len(hist_data)):
        #     if hist_data[i][0] != np_data[i][0]:
        #         np_data = np.delete(np_data, i)
        return hist_data
        #return np_data