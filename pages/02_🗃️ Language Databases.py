import streamlit as st

### SET CONFIG
st.set_page_config(page_title="Language databases", page_icon=":card_file_box:", layout="wide")

st.markdown(
	"""
	<style>
	span[data-baseweb="tag"] {background-color: #4682B4 !important;}
	</style>
	""",
	unsafe_allow_html=True,
)

### CONTENT
st.header(":card_file_box: Language Databases")
st.markdown(
    """
        This is a guide to using language databases in LexiVault.
    """
)