import pandas as pd
import numpy as np
import datetime
from config import Niguri
n = Niguri('Niguri.xlsx')
pd_date = pd.to_datetime('2020-02-01', format='%Y-%m-%d')
pd_date
n.stk
prev_stk = n.stk.loc[(pd_date - pd.DateOffset(months=1)), 'A']
prev_stk
if prev_stk == np.nan:
    prev_stk = 0

now_ws = n.ws.loc[pd_date,'A']
now_ws
if now_ws == np.nan:
    now_ws = 0

now_arrival = n.arrival.loc[pd_date,'A']
n.arrival.loc[pd_date,'A'].isnull()
np.isnan(now_arrival)
now_arrival = 0
if now_arrival == np.nan:
    now_arrival = 0
n.stk
n.new_stk('2020-04-01','A')
n.up_stk('2020-02-01')
value = prev_stk - now_ws + now_arrival
value
n.stk.index.tolist().index(pd.Timestamp('2020-02-01'))
n.stk
n.check_nan(value)
date1 = pd.to_datetime('2019-02-01')
date2 = pd.to_datetime('2020-05-01')
n.up_stk('2020-01-01')
n.stklvl
n.stk
n.sales.loc['2019-12-01':'2020-10-01','B'].mean()
n.sales.loc['2020-03-01':]

n.up_stklvl('2020-01-01')
n.up_stk('2020-01-01')
date
pd.date_range(1, periods = 10).tolist()
n.sales.loc[date1:date2, 'A']
n.calc_stklvl('2020-05-01','B')
n.stk.loc['2020-01-01']