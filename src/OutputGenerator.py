'''
INPUT: .csv file in /db
OUTPUT: .py streamlit interface file that can be put in /pages
'''
import streamlit as st
from src.configs import LANGUAGES, PARAMETERS

class OutputGenerator:
    def __init__(self, lang_key: str, has_title: bool = False):
        self.lang_key = lang_key
        self.has_title = has_title

        # get configs for the specified language
        self.lang_configs = LANGUAGES[lang_key]
        self.params = list(self.lang_configs['parameters'].keys())

        # csv
        self.df_lex = self.load_lexicon()

    def load_lexicon(self):
        pass

    # ===================================
    # Interface: Rendering about + search
    # ===================================
    def render_param_def(self, param):
        # sometimes there is a custom parameter definition; load it if it exists
        if self.lang_configs['parameters'][param] != 0:
            return self.lang_configs['parameters'][param]
        return PARAMETERS[param]
        
    def render_about(self, note=''):
        '''
        rendering the about section; optional parameter for a note to be displayed beneath the about-the-corpus section
        '''
        about_configs = self.lang_configs['about']

        # info about the corpus itself
        if about_configs['status'] == 0:
            pass
        else:
            status = 'was constructed from a'
            if about_configs['status'] == 'under construction':
                status = f'is under construction. Currently it has a'
            sources = '<br>'.join([f'📚 {s}' for s in about_configs['sources']])
            st.markdown(
                f'''This lexicon {status} {about_configs['wordcount']} word corpus that consists of the following:<br>{sources}<br>{note}''',
                unsafe_allow_html=True,
            )
        
        # info about the search parameters
        params = '<br>'.join([f'🔠 **{p}** :blue[=] {self.render_param_def(p)}' for p in self.lang_configs['parameters']])
        st.markdown(
            f'''This corpus contains the following search parameters:<br>{params}''',
            unsafe_allow_html=True
        )

    def run(self):
        '''
        rendering the interface for the language based on the /db csv file
        '''
        st.set_page_config(page_title='LexiVault Demo', page_icon=':book:', layout='wide')
        st.markdown(
            """
            <style>
            span[data-baseweb="tag"] {background-color: #4682B4 !important;}
            </style>
            """,
            unsafe_allow_html=True,
            )

        # =======================
        # Interface: Page content
        # =======================
        if self.has_title: st.header(self.lang_key)
        with st.expander(label=f'**🧭 About the Lexicon**: {self.lang_key}', expanded=True):
            self.render_about()
        with st.expander(label=f'**🔍 Search & Filter**: {self.lang_key}', expanded=True):
            pass