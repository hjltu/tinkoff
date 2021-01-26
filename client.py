#!/usr/bin/env python3
# 22jan21 hjltu@ya.ru
# Copyright (c) 2020 hjltu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


try:
    from openapi_client import openapi
except Exception as e:
    raise SystemExit('Import Error: ' + str(e) + '. Exit')
from datetime import datetime, timedelta
from pytz import timezone
from config import Style


ERR_NO_DATA = 'ERR: {} no data for {}'


class TinkoffAPIClient():
    """
    https://github.com/Awethon/open-api-python-client
    """

    def __init__(self, token, currency='USD'):
        self._client = openapi.sandbox_api_client(token)
        # register new client
        self._client.sandbox.sandbox_register_post()
        # clear all orders
        self._client.sandbox.sandbox_clear_post()
        # remove balance
        self._client.sandbox.sandbox_remove_post()

        self.all_instruments = self.get_all_instruments(currency)


    def get_instrument(self, ticker='NOK'):
        """
        Input: str, ticker
        Output: dict, instrument,
            e.g: ticker = 'T'
                {'currency': 'USD',
                'figi': 'BBG000BSJK37',
                'isin': 'US00206R1023',
                'lot': 1,
                'min_price_increment': 0.01,
                'name': 'AT&T',
                'ticker': 'T',
                'type': 'Stock'}
        """
        stock = self._client.market.market_stocks_get()
        for i in stock.payload.instruments:
            if i.ticker == ticker:
                return i


    def get_all_instruments(self, currency='USD'):
        """
        Input:
            currency: USD, EUR, RUB
        Output:
            dict of all instruments {ticker: figi}, eg {'TSLA': 'BBG000N9MNX3', ...}
        """
        stock = self._client.market.market_stocks_get()
        all_instruments = {}
        for i in stock.payload.instruments:
            if currency and i.currency == currency:
                all_instruments.update({i.ticker : i.figi})
        return all_instruments


    def get_price(self, my_instruments: list, depth=1, timeframe='day'):
        """
        Print table of prices(h,o,c,l)
        Input:
            my_instrument: list of tickers ('TSLA', 'AMZN',...)
            depth: int, days, e.g 7 for week,
            interval: candles interval, day, week, month,
            min_diff: open - close,
            max_diff: ,
            show: print table
        Output:
            dict of prices, {
                            timeframe: timefframe,
                            tickers': {
                                ticker: {
                                    date: {
                                        high:h,
                                        open:o,
                                        close:c,
                                        low:l},
                                    next date, ...},
                                next ticker, ...}}
        """
        now=datetime.utcnow()
        res=''
        price ={'timeframe': timeframe, 'tickers': {}}
        for k,v in self.all_instruments.items():
            if k in set(my_instruments):
                res = self._client.market.market_candles_get(
                    figi=v, _from=(now-timedelta(days=depth)).isoformat()+'Z',
                    to=now.isoformat()+'Z', interval=timeframe)
                #print('res:', res)
                if res.status == 'Ok':
                    candles = res.payload.candles
                    if len(candles) == 0:
                        price['tickers'].update({k: ERR_NO_DATA.format(now, k)})
                        continue
                    else:
                        price['tickers'].update({k: {}})
                    for i in range(len(candles)):
                        try:
                            candle_date = candles[i].time.strftime("%d%b")
                            price['tickers'][k].update({candle_date: {
                                'high': candles[i].h,
                                'open': candles[i].o,
                                'close': candles[i].c,
                                'low': candles[i].l}})
                        except Exception as e:
                            print("ERR:",e)
        return price


    def print_table(self, price: dict, min_diff=5, max_diff=15):
        """
        Input:
            interval: candles interval, day, week, month,
            dict of prices: discribed in get_price()
            min_diff: diff between open and close prices in candles,
            max_diff: diff between high and low prices in candles,
        """
        timeframe = price['timeframe']
        print(Style.BOLD + f'{timeframe}\tname\thigh\topen\tclose\tlow\tname\tcl-op\thi-lw' + Style.RESET)
        count = 0
        for ticker,data in price['tickers'].items():
            try:
                for date, candle in data.items():
                    h = candle['high']
                    o = candle['open']
                    c = candle['close']
                    l = candle['low']
                    if count%2 == 0:
                        print(f"{date}\t{Style.YELLOW}{ticker}\t{h:.1f}\t{o:.1f}\t{c:.1f}\t{l:.1f}\t{ticker}{Style.RESET}", end='')
                    else:
                        print(f"{date}\t{Style.WHITE}{ticker}\t{h:.1f}\t{o:.1f}\t{c:.1f}\t{l:.1f}\t{ticker}{Style.RESET}", end='')
                    body = (c - o) / ((o + c) / 200)
                    if body < -min_diff:
                        print(Style.LIGHT_BLUE, end='')
                    if body < -max_diff:
                        print(Style.SELECT, end='')
                    if body > min_diff:
                        print(Style.LIGHT_GREEN, end='')
                    if body >= max_diff:
                        print(Style.SELECT, end='')
                    print(f"\t{body:.1f} %", end='')
                    print(Style.RESET, end='')
                    wick = (h - l) / ((h + l) / 200)
                    if wick > max_diff*2:
                        print(Style.LIGHT_RED, end='')
                    print(f"\t{wick:.1f} %", end='')
                    print(Style.RESET, end='')
                    print('')
            except:
                    print(Style.LIGHT_RED + str(data) + Style.RESET)
                    continue
            count +=1
