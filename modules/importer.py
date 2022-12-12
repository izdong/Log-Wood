import pandas as pd
import streamlit as st

class DataImport:
    """"
    Import data from CSV file on Google Cloud
    """
    def __init__(self):
        pass

    @st.experimental_memo(ttl=60*60) # ttl of one hour to keep memory in cache
    def fetch_and_clean_data(_self):
        data_path = 'data/data2.csv'
        df = pd.read_csv(data_path).replace("'","", regex=True)
        # df.input_date_cctv = pd.to_datetime(df.input_date_cctv, format = '%d/%m/%Y')
        df['date'] = pd.to_datetime(df['input_date_cctv'], format = '%d/%m/%Y')
        # df['day'] = df['date'].dt.day_name().str[:3]
        # df['month'] = df['date'].dt.month_name().str[:3]
        df = df.sort_values(by = ['date'])
        return df



# @st.cache(allow_output_mutation=True)
# def fetch_data():  
#     return pd.read_csv('data/data.csv')

# df = fetch_data()
# dfn = df.drop(['int_class', 'precision'], axis=1)

# # ---------------------------------data prepare---------------------------------

# df['date'] = pd.to_datetime(df['input_date_cctv'], format = '%Y/%m/%d')
# df.sort_values(by = ['date'])

# df['day'] = df['date'].dt.day_name().str[:3]
# mon = df['month'] = df['date'].dt.month_name().str[:3]



# sort_date = df.sort_values(by='date')

# # create data frame for prediction f1-score

# f1 = f1_score(df['int_class'], df['precision'])
# f1_df = pd.DataFrame({'pass': [f1], 'fail': [1 - f1]}, index = ['G'])