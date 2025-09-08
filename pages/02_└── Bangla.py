import streamlit as st

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
st.header("Welcome to LexiVault! :book:")