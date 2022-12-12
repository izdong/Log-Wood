import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from modules.formater import Title, Footer
from modules.importer import DataImport
from PIL import Image

# Title page and footer
title = "Process"
t = Title().page_config(title)
f = Footer()

# Import data
df = DataImport().fetch_and_clean_data()

# Clean
df = df.drop(['int_class', 'precision', 'image_hash', 'date'], axis=1)
df = df.tail(1)

# create container
a = 1
container_data = st.container()
with container_data:
    st.write(df)
    container_head = st.container()
    col1, col2, col3 = st.columns(3)
    with container_head:
        with col1:
            st.metric('Type','1')

        with col2:
            st.metric('Confidence (%)',f'{a}%')

        with col3:
            st.metric('Overall Confidence',f'{a}%')

        # with col3:
            # st.metric()
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


container1 = st.container()
col1, col2, col3= st.columns(3)

with container1:
    with col1:
        image = Image.open('images/f.jpg')
        n_image = image.resize((1280,800))
        st.image(n_image,caption='Front View')
        st.write("<h4 style='text-align: center;'>Front</h4>", unsafe_allow_html=True)
    with col2:
        image = Image.open('images/s.jpg')
        n_image = image.resize((1280,800))
        st.image(n_image, caption='Side View')
        st.write("<h4 style='text-align: center;'>Side</h4>", unsafe_allow_html=True)
    with col3:
        image = Image.open('images/b.jpg')
        n_image = image.resize((1280,800))
        st.image(n_image, caption='Back View')
        st.write("<h4 style='text-align: center;'>Back</h4>", unsafe_allow_html=True)

# container2 = st.container()
# with container2:
#     col1, col2, col3 = st.columns(3)
#     with col2:
#         st.image('images/s.jpg', caption='Side View')
#         st.write("<h4 style='text-align: center;'>Side</h4>", unsafe_allow_html=True)

# container4 = st.container()

