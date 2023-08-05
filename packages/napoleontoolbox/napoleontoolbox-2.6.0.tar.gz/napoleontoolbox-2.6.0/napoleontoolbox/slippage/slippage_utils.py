import datetime as dt
import pandas as pd
import requests
import json
import math
from dateutil import parser
from numba import jit
from numba import typed
import numpy as np


# CryptoCompare

def to_unix(s):
    if isinstance(s, str):
        dt_object = parser.parse(s)
    else:
        dt_object = s
    return int(dt_object.replace(tzinfo=dt.timezone.utc).timestamp())


def to_iso(ts):
    if type(ts) == str:
        ts = parser.parse(ts)
        return ts.replace(tzinfo=dt.timezone.utc).isoformat()
    else:
        return dt.datetime.utcfromtimestamp(ts).replace(tzinfo=dt.timezone.utc).isoformat()


def assess_rsp(response):
    if response.status_code != 200:
        raise RuntimeError('Bad gateway:', response.status_code)
    elif isinstance(response.json(), list) and len(response.json()) == 0:
        raise ValueError('No data')
    # elif response.json()['Response'] != 'Success':
    # raise RuntimeError(response.json()['Message'])


def extract_df(optype, precision, r):
    if optype == 'OHLC':
        try:
            tmp = r.json()['Data']['Data']
            return pd.DataFrame(tmp)
        except KeyError:
            print(r.json()['Message'])
    else:
        return pd.DataFrame(r.json()['Data'])


class CryptoCompare:
    def __init__(self, api_key=None, exchange=None):
        self.api_key = api_key
        self.e = exchange

    def get(self, optype, currency, startdate, enddate, precision):
        timedelta = to_unix(enddate) - to_unix(startdate)
        ts = to_unix(enddate)
        precision_dct = {'1h': 3600, 'hour': 3600, 'minute': 60}
        endpoint_dct = {'OHLC': {'url': 'https://min-api.cryptocompare.com/data/v2/histo{}'.format(precision),
                                 'params': {'fsym': currency, 'tsym': 'USD', 'limit': '2000', 'aggreggate': '1',
                                            'toTs': ts}},
                        'OBL2': {'url': 'https://min-api.cryptocompare.com/data/ob/l2/snapshot',
                                 'params': {'api_key', self.api_key}},
                        'HVOL': {'url': 'https://min-api.cryptocompare.com/data/symbol/histohour',
                                 'params': {'fsym': currency, 'tsym': 'USD', 'limit': '500', 'toTs': ts}}}

        if optype == 'OHLC' and precision == 'minute':
            endpoint_dct[optype]['params']['api_key'] = '{' + self.api_key + '}'

        runs, rest = divmod(timedelta / precision_dct[precision], int(endpoint_dct[optype]['params']['limit']))
        runs, rest = int(runs), str(int(math.ceil(rest)))
        output = pd.DataFrame()
        for run in range(runs):
            r = requests.request("GET", endpoint_dct[optype]['url'], params=endpoint_dct[optype]['params'])
            assess_rsp(r)
            output = pd.concat([output, extract_df(optype, precision, r)])
            endpoint_dct[optype]['params'].update({'toTs': output.time.min()})

        if rest != '0':
            endpoint_dct[optype]['params'].update({'limit': rest})
            print(endpoint_dct[optype]['params'])
            r = requests.request("GET", endpoint_dct[optype]['url'], params=endpoint_dct[optype]['params'])
            assess_rsp(r)
            output = pd.concat([output, extract_df(optype, precision, r)])

        output['timestamp'] = output.time.apply(lambda x: to_iso(x))
        output = output.set_index('timestamp', drop=True).sort_index().drop_duplicates()
        return output

def binance_get(api, p, type_, start_time, end_time = None, symbol = None, aggreg = None):
  '''
  Accepted types: futures_funding, all_futures_orders, futures_klines (aggreg = 1H), spot_klines (aggreg = '1m', '1h')
  Accepted start_time, end_time: datetime ns
  '''

  from binance.client import Client
  import json
  import time

  client = Client(api, p)
  assert type_ in ['trade_history', 'futures_funding', 'futures_klines', 'wallet_history', 'spot_klines'], 'Wrong type_: trade_history, futures_funding, futures_klines, wallet_history available'
  if aggreg is not None:
    assert aggreg in ['1h', '1m'], 'Wrong aggreg_: 1m, 1h available'
    dct_cvt = {'1m': Client.KLINE_INTERVAL_1MINUTE, '1h':Client.KLINE_INTERVAL_1HOUR}
    aggreg = dct_cvt[aggreg]


  output = pd.DataFrame()
  if type_ == 'futures_funding' and symbol is not None:
    startTime = int(start_time.timestamp()*1000)
    endTime = int(end_time.timestamp()*1000)
    while startTime<endTime:
      time_col = 'fundingTime'
      try:
        output = pd.concat([output, pd.DataFrame(client.futures_funding_rate(symbol = symbol, startTime = startTime, endTime = endTime, limit = 1000))])
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
      endTime = output.loc[:,time_col].min()
  elif type_ == 'trade_history':
    print('Retrieving all orders in 3H slices. Stay put.')
    time_col = 'time'
    drange = list(pd.date_range(start_time, end_time, freq ='3H'))
    for _ in range(len(drange)-1):
      startTime = int(drange[_].timestamp()*1000)
      endTime = int(drange[_+1].timestamp()*1000)
      try:
        tmp = pd.DataFrame(client.futures_account_trades(limit = 1000, startTime = startTime, endTime = endTime))
        output = pd.concat([output, tmp])
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
        continue
    time.sleep(1)
  elif (type_ == 'futures_klines') and (symbol is not None) and (aggreg is not None):
    startTime = int(start_time.timestamp()*1000)
    endTime = int(end_time.timestamp()*1000)
    while startTime<endTime:
      time_col = 'time'
      try:
        output = pd.concat([output, pd.DataFrame(client.futures_klines(symbol = symbol, interval = aggreg, startTime = startTime, endTime = endTime, limit = 1000))])
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
      startTime = output.loc[:,0].max()
    output.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_vol', 'ntrades', 'takerbuy_base_asset_vol', 'takerbuy_quote_asset_vol', 'ignore']
  elif type_ == 'wallet_history':
    startTime = int(start_time.timestamp()*1000)
    endTime = int(end_time.timestamp()*1000)
    while startTime<endTime:
      time_col = 'time'
      try:
        output = pd.concat([output, pd.DataFrame(client.futures_income_history(startTime = startTime, endTime=endTime, limit = 1000))])
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
      startTime = output.loc[:,'time'].max()
  elif (type_ == 'spot_klines')  and (symbol is not None) and (aggreg is not None):
    startTime = int(start_time.timestamp()*1000)
    endTime = int(end_time.timestamp()*1000)
    while startTime<endTime:
      time_col = 'time'
      try:
        output = pd.concat([output, pd.DataFrame(client.get_historical_klines(symbol = symbol, interval = aggreg, start_str = startTime, end_str = endTime, limit = 500))])
      except json.decoder.JSONDecodeError:
        print('Could not convert to Json. Passing @time:', startTime)
      startTime = output.loc[:,0].max()
    output.columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_vol', 'ntrades', 'takerbuy_base_asset_vol', 'takerbuy_quote_asset_vol', 'ignore']
  else:
    print('Wrong param combination.')
    return
  output['ts'] = (output[time_col] / 1000).apply(lambda x: dt.datetime.utcfromtimestamp(x))
  output = output.sort_values(by='ts', ascending = True).drop_duplicates()
  print(type_, 'done. Shape:', output.shape)
  return output

# binance_get('wallet_history', dt.datetime(2020,1,15,0,0,0), end_time= dt.datetime(2020,5,19), symbol = 'ETHUSDT').drop_duplicates().head(50)

from numba import jit

def trades_to_arr(df):
  # btcusdt = 1
  # ethusdt = -1
  # buy = 1
  # sell = 0
  # limit = 1
  # market = 0
  # sell = -1
  # buy = 1
  df[['price', 'qty', 'realizedPnl', 'quoteQty', 'commission', 'time']] = df[['price', 'qty', 'realizedPnl', 'quoteQty', 'commission', 'time']].astype(float)
  df = df.replace('SELL', -1).replace('BUY', 1).replace('ETHUSDT', -1).replace('BTCUSDT',1)
  df['maker'] = df.maker.apply(lambda x: 0 if x == False else 1)
  df = df[['symbol','side', 'price', 'qty', 'realizedPnl', 'quoteQty', 'commission', 'time', 'maker']].copy()
  df = df.astype(float)
  d = typed.Dict()
  for i, k in enumerate(df.columns):
    d[k] = i
  return df.values, d

@jit(nopython =True)
def get_qtraded(arr, d):
  qtraded_ETH = []
  qtraded_BTC = []
  for i in range(arr.shape[0]):
    if arr[i, d['symbol']] == -1:
      qtraded_ETH.append(arr[i, d['qty']])
      qtraded_BTC.append(0.)
    else:
      qtraded_BTC.append(arr[i, d['qty']])
      qtraded_ETH.append(0.)
  qtraded_BTC = np.array(qtraded_BTC)
  qtraded_ETH = np.array(qtraded_ETH)
  return qtraded_BTC, qtraded_ETH

@jit(nopython =True)
def get_sizes(arr, d):
  size_ETH = []
  size_BTC = []
  for i in range(arr.shape[0]):
    if arr[i, d['symbol']] == -1:
      size_ETH.append(arr[i, d['quoteQty']])
      size_BTC.append(0)
    else:
      size_BTC.append(arr[i, d['quoteQty']])
      size_ETH.append(0)
  return np.array(size_BTC), np.array(size_ETH)
  pass

@jit(nopython =True)
def get_senses(arr, d):
  sens_ETH = []
  sens_BTC = []
  for i in range(arr.shape[0]):
    if (arr[i, d['symbol']] == -1) and (arr[i, d['side']] == 1):
      sens_ETH.append(1.)
      sens_BTC.append(0.)
    elif (arr[i, d['symbol']] == -1) and (arr[i, d['side']] == -1):
      sens_ETH.append(-1.)
      sens_BTC.append(0.)
    elif (arr[i, d['symbol']] == 1) and (arr[i, d['side']] == 1):
      sens_BTC.append(1.)
      sens_ETH.append(0.)
    elif (arr[i,d['symbol']] == 1) and (arr[i, d['side']] == -1):
      sens_BTC.append(-1.)
      sens_ETH.append(0.)
    else:
      sens_BTC.append(0)
      sens_ETH.append(0)
  return np.array(sens_BTC), np.array(sens_ETH)

@jit(nopython =True)
def get_markets(arr, d):
    markets_BTC = []
    markets_ETH = []
    for i in range(arr.shape[0]):
      if (arr[i, d['symbol']] == -1) and (arr[i, d['maker']] == 0):
        markets_ETH.append(arr[i, d['qty']])
        markets_BTC.append(0)
      elif (arr[i, d['symbol']] == 1) and (arr[i, d['maker']] == 0):
        markets_BTC.append(arr[i, d['qty']])
        markets_ETH.append(0)
      else:
        markets_BTC.append(0)
        markets_ETH.append(0)
    return np.array(markets_BTC), np.array(markets_ETH)

@jit(nopython=True)
def _merge_update(arr, d, arrays:list, names:list):
  if len(arrays) != len(names):
    return None
  else:
    last_idx = arr.shape[1] +1
    for a in arrays:
      t = a.reshape(-1,1)
      arr = np.hstack((arr, t))
    for _ in names:
      d[_] = int(last_idx)
      last_idx +=1
  return arr, d

@jit(nopython=True)
def numba_compute(arr, d):
  arrays = []
  a, b = get_qtraded(arr,d)
  arrays.extend([a,b])
  a, b = get_sizes(arr,d)
  arrays.extend([a,b])
  a, b = get_senses(arr,d)
  arrays.extend([a,b])
  a, b = get_markets(arr,d)
  arrays.extend([a,b])
  names = ['traded_xbt', 'traded_eth', 'size_xbt', 'size_eth', 'sens_trade_xbt', 'sens_trade_eth', 'markets_BTC', 'markets_ETH']
  arr, d = _merge_update(arr, d, arrays, names)
  return arr, d

def wh_to_arr(df):
  # Funding fees = 0
  # Trading fees = 1
  # Transfer = 2
  # Real Pnl = 3
  # USDT = 0
  # BNB = 1
  df[['income', 'time']]  = df[['income', 'time']].astype(float)
  df = df.replace('ETHUSDT', -1).replace('BTCUSDT',1).replace('FUNDING_FEE', 0).replace('COMMISSION', 1).replace('TRANSFER',2).replace('REALIZED_PNL', 3).replace('BNB',1).replace('USDT', 0)
  df = df[['symbol', 'incomeType', 'income', 'asset', 'time']].copy()
  #df = df.replace({'(.*?)':0}, regex=True)
  df = df.astype(float)
  d = typed.Dict()
  for i, k in enumerate(df.columns):
    d[k] = i
  return df.values, d

@jit(nopython=True)
def get_fees(arr, d):
  funding_fees_eth = []
  funding_fees_xbt = []
  trading_fees_eth = []
  trading_fees_xbt = []
  trading_fees_xbt_usd = []
  trading_fees_eth_usd = []
  realized_pnl = []
  transfers_au = []
  transfers_bnb = []
  fold = [funding_fees_eth,funding_fees_xbt,trading_fees_xbt_usd, trading_fees_eth, trading_fees_eth_usd, trading_fees_xbt, realized_pnl, transfers_au, transfers_bnb]

  for i in range(arr.shape[0]):
    if (arr[i, d['symbol']] == -1) and (arr[i, d['incomeType']] == 0):
      funding_fees_eth.append(arr[i, d['income']])
    elif (arr[i, d['symbol']] == -1) and (arr[i, d['incomeType']] == 1) and (arr[i,d['asset']] == 1):
      trading_fees_eth.append(arr[i, d['income']])
    elif (arr[i, d['symbol']] == -1) and (arr[i, d['incomeType']] == 1) and (arr[i,d['asset']] == 0):
      trading_fees_eth_usd.append(arr[i, d['income']])
    elif (arr[i, d['symbol']] == 1) and (arr[i, d['incomeType']] == 0):
      funding_fees_xbt.append(arr[i, d['income']])
    elif (arr[i, d['symbol']] == 1) and (arr[i, d['incomeType']] == 1) and (arr[i, d['asset']] == 1):
      trading_fees_xbt.append(arr[i, d['income']])
    elif (arr[i, d['symbol']] == 1) and (arr[i, d['incomeType']] == 1) and (arr[i, d['asset']] == 0):
      trading_fees_xbt_usd.append(arr[i, d['income']])
    elif (arr[i, d['incomeType']] == 3):
      realized_pnl.append(arr[i, d['income']])
    elif (arr[i, d['incomeType']] == 2) and (arr[i, d['asset']] == 0):
      transfers_au.append(arr[i, d['income']])
    elif (arr[i, d['incomeType']] == 2) and (arr[i, d['asset']] == 1):
      transfers_bnb.append(arr[i, d['income']])
    for _ in fold:
        if len(_) < i+1:
          _.append(0)
  fold_a = []
  for _ in fold:
    fold_a.append(np.array(_))
  return fold_a

@jit(nopython=True)
def numba_compute_fees(arr, d):
  arrays= get_fees(arr, d)
  names = ['funding_fees_eth','funding_fees_xbt','trading_fees_xbt_usd', 'trading_fees_eth', 'trading_fees_eth_usd', 'trading_fees_xbt', 'realized_pnl', 'transfers_au', 'transfers_bnb']
  arr, d = _merge_update(arr, d, arrays, names)
  return arr, d