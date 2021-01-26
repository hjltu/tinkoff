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


# Tinkoff API token
TOKEN = ''

# currency for tickers
CURRENCY = 'USD'

# Company ticker names
TICKERS = (
    'AAL','AAN','AES','MEI','NOK','OII','FSLR','LPL','CMCSA')

class Style():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BLACK = '\033[30m'
    ORANGE = '\033[33m'
    LIGHT_RED = '\033[91m'
    RED = '\033[31m'
    LIGHT_GREEN = '\033[92m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    LIGHT_BLUE = '\033[94m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    SELECT = '\033[7m'
    BG_GREEN = '\033[102m'
    BG_BLUE = '\033[104m'
    BG_RED = '\033[101m'
    RESET = '\033[0m'

