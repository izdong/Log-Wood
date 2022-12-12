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
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>

        """
        st.markdown(style, unsafe_allow_html=True)

# class Footer:
    """"
    Creates a clickable footer image with link
    source: https://discuss.streamlit.io/t/st-footer/6447
    """

    # def __init__(self):
    #     self.url = "https://www.ace-energy.co.th/"
    #     self.img = '/Users/Dong/Documents/Logwood/apps/Log-Wood/images/ace.png'   #"https://www.ace-energy.co.th/themes/default/assets/static/images/logo-ace.png"

    # def image(self, src_as_string, **style):
    #     return img(src=src_as_string, style=styles(**style))

    # def link(self, link, text, **style):
    #     return a(_href=link, _target="_blank", style=styles(**style))(text)

    # def layout(self, *args):
    #     style = """
    #     <style>
    #         MainMenu {visibility: hidden;}
    #         footer {visibility: hidden;}
    #         .stApp { bottom: 0px; }
    #     </style>
    #     """

    #     style_div = styles(
    #         position="fixed",
    #         right=0,
    #         bottom=0,
    #         height="150px",
    #         margin=px(0, 100, 0, 0),
    #         text_align="center",
    #         opacity=.7,
    #     )

    #     body = p()
    #     foot = div(
    #         style=style_div
    #     )(
    #         body
    #     )

    #     st.markdown(style, unsafe_allow_html=True)
    #     for arg in args:
    #         if isinstance(arg, str):
    #             body(arg)
    #         elif isinstance(arg, HtmlElement):
    #             body(arg)
    #     st.markdown(str(foot), unsafe_allow_html=True)

    # def footer(self):
    #     myargs = [
    #         self.link(self.url, self.image(self.img,)),
    #     ]
    #     self.layout(*myargs)

