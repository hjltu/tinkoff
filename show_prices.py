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


"""
show_prices.py
Usage:
    ./show_prices.py
    ./show_prices.py 1 day
    ./show_prices.py 3 day
    ./show_prices.py 7 week
    ./show_prices.py 14 week
    ./show_prices.py 30 month 10 20
"""


import sys
from config import TOKEN, CURRENCY, TICKERS
from client import TinkoffAPIClient as TAC

def main(days=7, interval='week', min_diff=5, max_diff=15):
    print('Initialize client... ',end='')
    client = TAC(TOKEN, CURRENCY)
    print('done')
    print('Get prices... ', end='')
    p = client.get_price(TICKERS, days, interval)
    print('done')
    client.print_table(p, min_diff, max_diff)

if __name__=="__main__":
    arg=sys.argv[1:]
    if len(arg) == 2:
        main(int(arg[0]), arg[1])
    if len(arg) == 4:
        main(int(arg[0]), arg[1], int(arg[2]), int(arg[3]))
    if len(arg) != 2 and len(arg) != 4:
        print(__doc__)
        main()
