import pandas as pd
import numpy as np

class Niguri:
    """
    Class for Niguri file.

    Args: Excel file path as a string. 
    
    Notes: Excel file must have proper format in order to work this class.
    """
    def __init__(self, file):
        self.stk = pd.read_excel(file, sheet_name='STK', index_col=0)
        self.stklvl = pd.read_excel(file, sheet_name='STK_LVL', index_col=0)
        self.order = pd.read_excel(file, sheet_name='ORDER', index_col=0)
        self.properties = pd.read_excel(file, sheet_name='MTO_PROPERTIES', index_col=0)
        self.mtos = self.properties.columns.tolist()
        self.sales = pd.read_excel(file, sheet_name='WHOLESALES', index_col=0)
        self.arrival = pd.read_excel(file, sheet_name='ARRIVAL', index_col=0)

    def new_stk(self, date, model='all'):
        pd_date = pd.to_datetime(date, format='%Y-%m-%d')
        if pd_date <= self.stk.index[0]:
            pd_date=self.stk.index[1]

        if model == 'all':
            for el in self.mtos:
                prev_stk = self.stk.loc[(pd_date - pd.DateOffset(months=1)), el]
                
                if np.isnan(prev_stk):
                    prev_stk = 0

                now_sales = self.sales.loc[pd_date,el]
                if np.isnan(now_sales):
                    now_sales = 0

                now_arrival = self.arrival.loc[pd_date,el]
                now_arrival = 0
                if np.isnan(now_arrival):
                    now_arrival = 0

                self.stk.at[pd_date,el] = prev_stk - now_sales + now_arrival

            return self.stk.loc[pd_date]
        else:
            prev_stk = self.stk.loc[(pd_date - pd.DateOffset(months=1)), model]

            if np.isnan(prev_stk):
                prev_stk = 0

            now_sales = self.sales.loc[pd_date,model]
            if np.isnan(now_sales):
                now_sales = 0

            now_arrival = self.arrival.loc[pd_date,model]
            now_arrival = 0
            if np.isnan(now_arrival):
                now_arrival = 0

            self.stk.at[pd_date,model] = prev_stk - now_sales + now_arrival

            return self.stk.at[pd_date,model]
    
    def range_(self, date):
        range(self.stk.index.tolist().index(pd.Timestamp(date)),len(self.stk.index))

    def up_stk(self, start_date, model='all'):
        """Method to update stock of defined model.

        Args: Model name as string, start date as string in YYYY-MM-DD format.

        Returns: None.
        """
        for date in self.stk.loc[start_date:].index:
            self.new_stk(date, model)
    
    def calc_avg_sales(self, date, model):
        pd_date = pd.to_datetime(date)
        start_date = pd_date - pd.DateOffset(months=6)
        end_date = pd_date + pd.DateOffset(months=5)
        df = self.sales
        sales_mean = df.loc[start_date:end_date, model].mean()
        return sales_mean

    def calc_stklvl(self, date, model):
        self.up_stk(date) #Generates stock situation according to sales plan
        stk = self.stk.loc[date,model]
        avg_sales = self.calc_avg_sales(date, model)
        stklvl = stk/avg_sales
        self.stklvl.at[date,model] = stklvl

    def up_stklvl(self, start_date, model='all'):
        df = self.sales
        if model != 'all':
            for date in df.loc[start_date:].index:
                self.calc_stklvl(date, model)

        else:
            for mto in self.mtos:
                for date in df.loc[start_date:].index:
                    self.calc_stklvl(date, mto)
    
    def calc_order(self, date, model='all', stk_set= 2.5):
        pass