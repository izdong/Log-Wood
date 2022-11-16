# real
import numpy as np
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from sklearn.metrics import f1_score
from distutils import errors
from distutils.log import error
import altair as alt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode


# ---------------------------------pageconfig---------------------------------
st.set_page_config(
                    layout="wide",
                    page_icon="🌲",
                    page_title="Log Wood",
                    initial_sidebar_state="collapsed",
                    menu_items = None
                    )

#get and cache data
# @st.experimental_memo
# def get_data():
#     return pd.read_csv('/Users/DONG/Documents/Log Wood/Data/predictions_part_0.csv')
# df = get_data()
@st.cache(allow_output_mutation=True)
def fetch_data():  
    return pd.read_csv('/Users/DONG/Documents/Log Wood/Data/predictions_part_0.csv')

df = fetch_data()
dfn = df.drop(['int_class', 'precision'], axis=1)

# ---------------------------------data prepare---------------------------------

df['date'] = pd.to_datetime(df['input_date_cctv'], format = '%Y/%m/%d')
df.sort_values(by = ['date'])

df['day'] = df['date'].dt.day_name().str[:3]
mon = df['month'] = df['date'].dt.month_name().str[:3]



sort_date = df.sort_values(by='date')

# create data frame for prediction f1-score

f1 = f1_score(df['int_class'], df['precision'])
f1_df = pd.DataFrame({'pass': [f1], 'fail': [1 - f1]}, index = ['G'])


# ---------------------------------sidebar menu---------------------------------
# https://github.com/victoryhb/streamlit-option-menu
with st.sidebar:
    choose = option_menu("Log Wood", ["Overview", "Process", "Statistic"],
                         icons=['house', 'play', 'file-bar-graph'],
                         menu_icon="app-indicator", default_index=0,

    #                      styles={
    #     "container": {"padding": "5", "background-color": "#fafafa"},
    #     "icon": {"color": "orange", "font-size": "25px"}, 
    #     "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    #     "nav-link-selected": {"background-color": "#02ab21"},
    # }
    )

# ---------------------------------chart for display each tab---------------------------------
@st.cache #test with cache
def mo():
    month = px.histogram(sort_date, x = 'month', text_auto = True)
    return month.update_layout(bargap=0.2)
month = mo()

dow = px.histogram(df, x="day", category_orders=dict(day=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]), text_auto = True)

overall = px.histogram(sort_date, x = 'date', text_auto = True)
overall.update_layout(bargap = 0.15)

accuracy = px.pie(f1_df.T, values = 'G', hole = .4321, names = f1_df.T.index)

# Type = px.histogram(df, x = 'class', histnorm = 'percent', text_auto = True)


# ---------------------------------for statistic tab---------------------------------


# build grid option

gb = GridOptionsBuilder.from_dataframe(dfn)

#  Customize column

gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gb.configure_column("input_date_cctv", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd', pivot=True)
gb.configure_column("input_time_cctv", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='HH:mm:ss', pivot=True)

gb.configure_column("weigh_wood", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=1, aggFunc='sum')
gb.configure_column("correlation_class", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='avg')
gb.configure_column("cosine_class", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='avg')

# Customize pagination
# gb.configure_pagination(paginationAutoPageSize=True)

# multiselect
gb.configure_selection('multiple',use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)
# gb.configure_selection('multiple',rowMultiSelectWithClick=True, suppressRowDeselection=True)

# gb.configure_auto_height(autoHeight=True)
gb.configure_grid_options(domLayout='normal')
# Customize cell style
cellsytle_jscode = JsCode("""
function(params) {
    if (params.value == 'A') {
        return {
            'color': 'white',
            'backgroundColor': 'darkred'
        }
    } else {
        return {
            'color': 'black',
            'backgroundColor': 'white'
        }
    }
# };
""")


# --------------------------------- overview tab ---------------------------------




if choose == "Overview":
    
#  row 1

    container1 = st.container()
    col1, col2 = st.columns(2)

# column in row 1
    with container1:
        with col1:              #left
            st.markdown("<h4 style='text-align: center;'>Accuracy</h4>", unsafe_allow_html=True)
            accuracy
        with col2:

            # option = st.selectbox(
            # 'How would you like to display?',
            # (' Overall', 'Month', 'Day of Week'), index = 0)              #right
        
            # if option == ' Overall' :
            #     overall

            # elif option == 'Month' :
            #     mo()

            # elif option == 'Day of Week' :
            #     dow
            st.markdown("<h4 style='text-align: center;'>Statistic</h4>", unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["Overall", "Month", "Day of Week"])
            with tab1:
                overall
            with tab2:
                month
            with tab3:
                dow


#  row 2

    container2 = st.container()
    col3, col4 = st.columns(2)

#  columns in row 2
    with container2:
        with col3:              #left
            st.markdown('#')
            st.markdown('#')
            st.metric(label = 'Total', value = len(df.index))
            f12 = (f1 * 100)
            st.metric(label = 'correct (%)', value = round(f12, 2))
            st.metric(label = 'incorrect (%)', value = round((100-f12),2))

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
            </style>
            ''', unsafe_allow_html=True)


        with col4:              #right
            # st.markdown('% Type of Wood')
            # st.markdown("<h4 style='text-align: center;'>% Type of Wood</h>", unsafe_allow_html=True)
            
            tab1, tab2= st.tabs(["Percent", "Amount"])
            
            

            with tab1:
                Type = px.histogram(df, x = 'class', histnorm = 'percent', text_auto = True)
                Type
                
            with tab2:
                Type = px.histogram(df, x = 'class', histnorm = 'density', text_auto = True)
                Type
                
            



# --------------------------------- process tab ---------------------------------

# progress bar - description below 

# insert 3 photo 

# accuracy as text or some kind 




# --------------------------------- statistic tab ---------------------------------

# setting table
if choose == "Statistic":
    cols1, cols2 = st.columns(2)
    with cols1:
        setting_select = st.expander('setting')
    with setting_select:
        if setting_select:
            # fit_columns_on_grid_load = st.checkbox("Fit Grid Columns on Load")
            update_mode = st.selectbox("Update Mode", list(GridUpdateMode.__members__), index=len(GridUpdateMode.__members__)-11)
            update_mode_value = GridUpdateMode.__members__[update_mode]
            # grid auto chheck box
            grid_height = st.number_input("Grid height", min_value=200, max_value=800, value=300)
            fit_columns_on_grid_load = st.checkbox("Fit Grid Columns on Load", value = False)
            enable_pagination = st.checkbox("Enable pagination", value=False)
            if enable_pagination:
                st.subheader("Pagination options")
                paginationAutoSize = st.checkbox("Auto pagination size", value=True)

                if not paginationAutoSize:
                    sample_size = st.number_input("rows", min_value=10, value=30)
                    paginationPageSize = st.number_input("Page size", value=5, min_value=0, max_value=sample_size)
                    gb.configure_auto_height(autoHeight=True)


    if enable_pagination:
        if paginationAutoSize:
            gb.configure_pagination(paginationAutoPageSize=True)
        else:
            gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

    gridOptions = gb.build()

    grid_response = AgGrid(
        dfn, 
        gridOptions=gridOptions,
        height=grid_height, 
        width='100%',
        data_return_mode=DataReturnMode.AS_INPUT, 
        update_mode=update_mode_value,
        fit_columns_on_grid_load=fit_columns_on_grid_load,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        theme='streamlit'
        )

    dfr = grid_response['data']
    selected = grid_response['selected_rows']
    selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')





    with st.spinner("Displaying results..."):
        #displays the chart
        chart_data = dfr.loc[:,['weigh_wood','correlation_class','cosine_class']].assign(source='total')

        if not selected_df.empty :
            selected_data = selected_df.loc[:,['weigh_wood','correlation_class','cosine_class']].assign(source='selection')
            chart_data = pd.concat([chart_data, selected_data])

        chart_data = pd.melt(chart_data, id_vars=['source'], var_name="item", value_name="quantity")
        #st.dataframe(chart_data)
        chart = alt.Chart(data=chart_data).mark_bar().encode(
            x=alt.X("item:O"),
            y=alt.Y("sum(quantity):Q", stack=False),
            color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
        )

        st.header("Component Outputs - Example chart")
        st.markdown("""
        This chart is built with data returned from the grid. rows that are selected are also identified.
        Experiment selecting rows, group and filtering and check how the chart updates to match.
        """)

        st.altair_chart(chart, use_container_width=True)

        # st.subheader("Returned grid data:") 
        # #returning as HTML table bc streamlit has issues when rendering dataframes with timedeltas:
        # # https://github.com/streamlit/streamlit/issues/3781
        # st.markdown(grid_response['data'].to_html(), unsafe_allow_html=True)

        # st.subheader("grid selection:")
        # st.write(grid_response['selected_rows'])

        # st.header("Generated gridOptions")
        # st.markdown("""
        #     All grid configuration is done thorugh a dictionary passed as ```gridOptions``` parameter to AgGrid call.
        #     You can build it yourself, or use ```gridOptionBuilder``` helper class.  
        #     Ag-Grid documentation can be read [here](https://www.ag-grid.com/documentation)
        # """)
        # st.write(gridOptions)


