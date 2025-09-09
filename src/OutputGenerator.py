'''
INPUT: .csv file in /db
OUTPUT: .py streamlit interface file that can be put in /pages
'''
import streamlit as st
from src.configs import LANGUAGES

class OutputGenerator:
    def __init__(self, lang_key: str):
        self.lang_key = lang_key
        self.lang_configs = LANGUAGES[lang_key]

    def render_about(self):
        about_configs = self.lang_configs['about']

        # info about the corpus itself
        status = ''
        if about_configs['status'] == 'constructed':
            status = f'was constructed from a'
        else:
            status = f'is under construction. Currently it has a'
        sources = ''
        for source in about_configs['sources']:
            sources += f'<br>📚 {source}'
        
        st.markdown(
            f'''This lexicon {status} {about_configs['wordcount']} word corpus that consists of the following:{sources}''',
            unsafe_allow_html=True,
        )
        
        # info about the search parameters
        parameters = ''
        st.markdown(
            f'''This corpus contains the following search parameters: {parameters}''',
            unsafe_allow_html=True
        )

        return

    def run(self):
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
        st.header(self.lang_key)
        with st.expander(label='**🧭 About the Lexicon**', expanded=True):
            self.render_about()
        with st.expander(label='**🔍 Search & Filter**', expanded=True):
            pass