import numpy as np
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from sklearn.metrics import f1_score
import altair as alt
import datetime
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from modules.formater import Title, Footer
from modules.importer import DataImport


# Title page and footer
title = "TEST69"
t = Title().page_config(title)
f = Footer()


# Import data
df = DataImport().fetch_and_clean_data()
df['day'] = df['date'].dt.day_name().str[:3]
df['month'] = df['date'].dt.month_name().str[:3]

f1 = f1_score(df['int_class'], df['precision'])
f1_df = pd.DataFrame({'pass': [f1], 'fail': [1 - f1]}, index = ['G'])
sort_date = df.sort_values(by='date')
total = len(df)
first_date = df.date.dt.date.min()
today_date = (datetime.datetime.today() - datetime.timedelta(hours=6)).date() # streamlit runs on UTC, showing missing date for next day before collect
date_count = pd.DataFrame(df.date.dt.date.value_counts())
missing_dates = list(pd.date_range(start=first_date, end=today_date).difference(date_count.index))
daily = df.date.dt.date
daily = daily.value_counts().rename_axis('Date').reset_index(name='Transactions')
daily = daily.sort_values(by='Date', ascending=False)
delta_days = (today_date - (first_date - datetime.timedelta(days=2))).days # first day was actually day prior but UTC
t_day = round(len(df)/delta_days, 1)
try:
    t_today = daily[daily.Date == datetime.date.today()]  #transaction today
    t_today = t_today['Transactions'].fillna(0).iloc[0]
except IndexError: #Error when coming to new day and no values for new day
    try:
        t_today = daily[daily.Date == datetime.date.today() - datetime.timedelta(days=1)]
        t_today = today['Transactions'].fillna(0).iloc[0]
    except:
        t_today = 0 # kept getting index error on live dashboard
delta = 100 * (t_today - t_day) / t_day
delta = round(delta,1)
t_yest = total - t_today
t_all_delta = ((total - t_yest) * 100) / t_yest
t_all_delta = round(t_all_delta,1)


col1, col2 = st.columns(2)
with col1:
    st.markdown("<h4 style='text-align: center;'>Accuracy</h4>", unsafe_allow_html=True)
    pie = px.pie(f1_df.T, values = 'G', hole = .4321, names = f1_df.T.index)
    pie.update_layout(height=250) 
    st.plotly_chart(pie, use_container_width=True,height=250)
    st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
    ) # hide up arrow st.mertric{delta}
    st.metric('Total',total,f'{t_all_delta}%')
    f12 = (f1 * 100)
    st.metric('correct (%)',round(f12, 2))
    st.metric('incorrect (%)',round((100-f12),2))

    # center style
    st.markdown('''
    <style>
    /*center metric label*/
    [data-testid="stMetricLabel"] > div:nth-child(1) {
        justify-content: center;
    }

    /*center metric value*/
    [data-testid="stMetricValue"] > div:nth-child(1) {
        justify-content: center;
    }

    /*center metric value*/
    [data-testid="stMetricDelta"] > div:nth-child(2) {
        justify-content: center;
    }
    </style>
    ''', unsafe_allow_html=True)

with col2:
    container1 = st.container()
    with container1:
        st.markdown("<h4 style='text-align: center;'>Transaction</h4>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Overall", "Month", "Day of Week"])
        with tab1:
            overall = px.histogram(sort_date, x = 'date', text_auto = True)
            overall.update_layout(bargap = 0.15, height=300)
            st.plotly_chart(overall, use_container_width=True,height=300)

        with tab2:
            month = px.histogram(sort_date, x = 'month', text_auto = True)
            month.update_layout(bargap=0.2, height=300)
            st.plotly_chart(month, use_container_width=True,height=300)

        with tab3:
            dow = px.histogram(df, x="day", category_orders=dict(day=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]), text_auto = True)
            dow.update_layout(height=300) 
            st.plotly_chart(dow, use_container_width=True,height=300)
    container2 = st.container()
    with container2:
        st.markdown("<h4 style='text-align: center;'>Wood Type</h4>", unsafe_allow_html=True)
        tab1, tab2= st.tabs(["Percent", "Amount"])

        with tab1:
            Type = px.histogram(df, x = 'class', histnorm = 'percent', text_auto = True)
            Type.update_layout(height=300)
            st.plotly_chart(Type, use_container_width=True,height=300)
            
        with tab2:
            Type = px.histogram(df, x = 'class', histnorm = 'density', text_auto = True)
            Type.update_layout(height=300)
            st.plotly_chart(Type, use_container_width=True,height=300)