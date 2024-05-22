import streamlit as st
import pandas as pd
import os

from datetime import datetime

from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder



st.set_page_config(page_title='Lex App Demo', page_icon=':book:', layout='wide')

# ==================================================================
# LOADING THE LEXICON FROM CSV
# ==================================================================
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_lexicon():
	fpath = os.path.join(os.path.join(os.getcwd(),'lex_db'),'MSA_formatted.csv')
	dflx = pd.read_csv(fpath,sep=',',encoding='utf-8',low_memory=False)
	#df_slice = dflx.iloc[:10000]
	temp_drop_cols = ['lex.ar','diac.ar', 'stem.ar','root.ar','pattern.ar']
	return dflx.drop(columns=temp_drop_cols)

df_lex = load_lexicon()


# ===========================================================
# FUNCTIONALITY
# ===========================================================

def buildQuery():
	return None


# ===========================================================
# INTERFACE : SEARCH FORM
# ===========================================================


formContainer = st.container()
formContainer.header('Search Parameters')

col1, col2, col3, col4 = formContainer.columns((2,2,1,1))

with col1:
	searchMode = st.selectbox(label='Search By',options=['Orthographic Form (e.g. yaktub)','Lemma (e.g. katab)','Stem (e.g. ktub)','Root (e.g. k.t.b)','Pattern (e.g. ya12u3)'])
	file_ = st.file_uploader(label='',key='input_file',accept_multiple_files=False, type=['.xlsx','.xls','.csv','.txt'])
with col2:
	input_ = st.text_input(label='Text input',help='single entry search',placeholder='yaktub')
	pos_ = st.multiselect(
		label='Part-of-Speech (POS):',
		options=df_lex['pos'].unique(),
		default=['noun','verb','adj','adv'],
		help='filter results by part-of-speech (POS) tag'
		)
with col3:
	freq_min = st.number_input(label='Frequency Range: MINIMUM',min_value=df_lex['freq'].min(),max_value=df_lex['freq'].max(),value=df_lex['freq'].min())
	freq_max = st.number_input(label='Frequency Range: MAXIMUM',min_value=df_lex['freq'].min(),max_value=df_lex['freq'].max(),value=df_lex['freq'].max())

with col4:
	searchButton = st.button('Search', key='submit_btn',disabled=True)

# ===========================================================
# INTERFACE: TABLE
# ===========================================================
st.markdown('---')
bodyContainer = st.container()
col1_, col2_ = bodyContainer.columns((5,1))

with col1_:
	gd = GridOptionsBuilder.from_dataframe(df_lex)
	gd.configure_pagination(enabled=True)
	gd.configure_default_column(editable=True, groupable=True)

	gd.configure_selection(selection_mode='multiple',use_checkbox=False)
	gridoptions = gd.build()

	grid_table = AgGrid(df_lex, 
		gridOptions=gridoptions,
		fit_columns_on_grid_load=True,
		update_mode=GridUpdateMode.SELECTION_CHANGED,
		theme='fresh')
with col2_:
	timestampStr = datetime.now().strftime("%Y%m%d_%H%M%S")
	fname='lexivault_'+timestampStr+'.csv'
	st.download_button('Export as .csv', df_lex.to_csv().encode('utf-8'),file_name=fname,key='download_csv')