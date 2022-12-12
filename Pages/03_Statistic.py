import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from modules.formater import Title, Footer
from modules.importer import DataImport

# Title page and footer
title = "Statistic"
t = Title().page_config(title)
f = Footer()

# Import data
df = DataImport().fetch_and_clean_data()
df.input_date_cctv = pd.to_datetime(df.input_date_cctv, format = '%d/%m/%Y')
# dfn = df.drop(['int_class', 'precision','date'], axis=1)
gb = GridOptionsBuilder.from_dataframe(df)
# df.date(1)

#  Customize column

gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
gb.configure_column("input_date_cctv", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd/MM/yyyy', pivot=True)
# gb.configure_column("input_date_cctv", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
gb.configure_column("input_time_cctv", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='HH:mm:ss', pivot=True)
gb.configure_column("weigh_wood", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=1, aggFunc='sum')
gb.configure_column("correlation_class", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='avg')
gb.configure_column("cosine_class", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='avg')
gb.configure_column('input_date_cctv', headerCheckboxSelection = True)
gb.configure_column('site', headerCheckboxSelection = True)


gb.configure_side_bar()
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
cols1, cols2 = st.columns(2)
with cols1:
    setting_select = st.expander('setting')
with setting_select:
    if setting_select:
        # fit_columns_on_grid_load = st.checkbox("Fit Grid Columns on Load")
        update_mode = st.selectbox("Update Mode", list(GridUpdateMode.__members__), index=len(GridUpdateMode.__members__)-10)
        update_mode_value = GridUpdateMode.__members__[update_mode]
        # grid auto chheck box
        grid_height = st.number_input("Grid height", min_value=200, max_value=600, value=600)
        fit_columns_on_grid_load = st.checkbox("Fit Grid Columns on Load", value = False)
        enable_pagination = st.checkbox("Enable pagination", value=False)
        if enable_pagination:
            st.subheader("Pagination options")
            paginationAutoSize = st.checkbox("Auto pagination size", value=True)

            if not paginationAutoSize:
                # sample_size = st.number_input("rows", min_value=10, value=30)
                paginationPageSize = st.number_input("Page size", value=5, min_value=0, max_value=500)
                gb.configure_auto_height(autoHeight=True)


if enable_pagination:
    if paginationAutoSize:
        gb.configure_pagination(paginationAutoPageSize=True)
    else:
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

gridOptions = gb.build()

grid_response = AgGrid(
    df, 
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
selected_df = pd.DataFrame(selected)#.apply(pd.to_numeric, errors='coerce')

with st.spinner("Displaying"):
    chart_data = dfr.loc[:,['site','correlation_class','cosine_class']].assign(source='total')

    if not selected_df.empty :
        # selected_data = selected_df.loc[:,['site']].assign(source='selection')
        # chart_data = pd.concat([chart_data, selected_data])
        fig = px.histogram(selected_df, x = 'site', text_auto = True)
        st.plotly_chart(fig, use_container_width=True)




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
