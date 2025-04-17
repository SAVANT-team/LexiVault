import streamlit as st

### SET CONFIG
st.set_page_config(page_title="Language databases", page_icon=":gear:", layout="wide")

st.markdown(
	"""
	<style>
	span[data-baseweb="tag"] {background-color: #4682B4 !important;}
	</style>
	""",
	unsafe_allow_html=True,
)

### CONTENT
st.header(":gear: Admin Instructions")

st.markdown(
	"""
		This guide walks you through how to turn submitted data into a new LexiVault page, using the tools built into this dashboard.
	"""
)

with st.expander(label="**Instructions**", expanded=True):
	st.markdown(
			"""
				After someone submits data through the **Workshop** page, there will be a **.csv** file stored in the `temp_db` folder. For each one of these files, follow the steps below to turn it into a LexiVAULT page—
			"""
	)
	st.markdown(
			"""
			1. Upload the csv file from `temp_db` into the **🚀 Create a new page** section below; follow instructions given.  
			"""
	)
	st.markdown(
			"""
			2. This will give you a downloadable .py file.  
			"""
	)
	st.markdown(
			"""
			3. You may then move the .py into the `pages` folder—this will create a new page in LexiVault for that language.
			"""
	)
	st.markdown(
			"""
			4. For organization's sake, please move the csv file from `temp_db` to `lexivault_db`.  
			"""
	)

with st.expander(label="**🚀 Create a new page**", expanded=True):
    st.write("placeholder")