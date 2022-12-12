import streamlit as st
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


import streamlit as st
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

class Title(object):
    """"
        # Update title and favicon of each page
        # ⚠️ IMPORTANT: Must call page_config() as first function in script 
        # """
    def __init__(self):

        self.img = "images/1.png"
    
    def page_config(self, title):
        self.title = title
        st.set_page_config(
                            layout="wide",
                            page_title='log wood ' + self.title,
                            # page_icon='https://www.ace-energy.co.th/themes/default/assets/static/images/logo-ace.png',
                            page_icon=self.img,
                            initial_sidebar_state="expanded",
                            
                            )
        st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

class Footer:
    def __init__(self):
        style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>

        """
        st.markdown(style, unsafe_allow_html=True)