import streamlit as st

import pandas as pd
import os
import re

from datetime import datetime

from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from utils.charmap import CharMapper

st.set_page_config(page_title='LexiVault Demo', page_icon=':book:', layout='wide')


st.markdown(
	"""
	<style>
	span[data-baseweb="tag"] {background-color: #4682B4 !important;}
	</style>
	""",
	unsafe_allow_html=True,
	)
# color options for blue 
# Cerulean #0492C2
# Aegean #1F456E
# Stone #59788E
# Steel #4682B4

# ==================================================================
# UTILS
# ==================================================================

def cleanLemmas(text):
	if '_' in text:
		return text[:-2]
	else:
		return text

def ppMillion(text):
	raw_freq = float(text)
	ppmil_freq = raw_freq / 470.73 # total freq bnTenTen21 is 470,732,738 words https://www.sketchengine.eu/bntenten-bengali-corpus/#toggle-id-1
	return round(ppmil_freq, 3)

def mapSearchModeToColumn(smode):
	#st.write('Inside map func with mode=' + smode)
	col_name = 'word'
	options_lst = ['Word','Lemma']
	colname_lst = ['word','lemma']
	for i in range(0,len(options_lst)):
		if smode.strip() == options_lst[i].strip():
			col_name = colname_lst[i]
	#st.write('Final mapped value of column=' + col_name)
	return col_name


# ==================================================================
# LOADING THE LEXICON FROM CSV
# ==================================================================
@st.cache_data(experimental_allow_widgets=True)
def load_lexicon():
	fpath = os.path.join(os.path.join(os.getcwd(),'lexivault_db'),'bangla_streamlit.csv')
	dflx = pd.read_csv(fpath,sep='\t',encoding='utf-8',low_memory=False)
	#dflx = dflx.fillna('')
	dflx['wordfreq'] = dflx['wordfreq'].map(ppMillion)
	#dflx['stemfreq'] = dflx['stemfreq'].map(ppMillion)
	#return dflx.drop(columns=temp_drop_cols)
	return dflx

df_lex = load_lexicon()


# ===========================================================
# FUNCTIONALITY
# ===========================================================



def buildQueryStr(searchStr):

	#pos_list=['Foo','Bar']

	#df.query("POS == @pos_list")


	return None

def getResults(keyword, searchmode, postags, exactMatch):
	#keyword_bw = ARtoBW(keyword)
	#query_str = buildQueryStr()
	#results_ = df_lex
	keyword_ = keyword
	pos_filter = postags
	searchCol = searchmode

	if exactMatch:
		#results = df_lex.query("{0} == @keyword_".format(searchCol))
		results = df_lex.query("{0} == @keyword_".format(searchCol))
	else:
		#results = df_lex.query("{0}.str.contains(@keyword_,na=False)".format(searchCol))
		results = df_lex.query("{0}.str.contains(@keyword_)".format(searchCol))

	return results #pd.DataFrame()

def runSubmit():
	if st.session_state['input_word_bangla'] is None and st.session_state['input_file_bangla'] is None:
		st.warning('Please enter a keyword or upload a file to search')
	else:
		# ##################
		# Step 1: get the input
		# if there's a file - use that, otherwise default to the text area
		input_list = [] # this can be one item from the text area or many from the file
		if not(st.session_state['input_file_bangla'] is None):
			dfinput=pd.read_csv(input_f, sep=" ", header=None)
			input_list.extend(dfinput[dfinput.columns[0]].values.tolist())
		else:
			tokenized = str(st.session_state['input_word_bangla']).strip().split()
			input_list.extend(tokenized)

		input_wrd = '\t|\t'.join(input_list)
		search_col_name = mapSearchModeToColumn(searchMode)
		exact_match = st.session_state['strict_search']
		
		#pos_choices = st.session_state['pos_lst']
		#if len(pos_choices) == 0:
		#	pos_choices = df_lex['pos'].unique().tolist()
		

		#st.write('keyword(s) = ' + input_wrd)
		#st.write('search_by_value = ' + search_col_name)
		#st.write('POS selection:', pos_choices)
		#input_wrd = input_list[0]
		#st.write('starting with => ' + input_wrd)

		# ##################
		# Step 2: run the search query
		resultsDict = {}
		for item in input_list:
			#st.write('an item:::::' + item) 
			item_results_df = getResults(item, search_col_name, [], exact_match)
			if len(item_results_df.index) != 0:
				resultsDict[item] = item_results_df

		# ##################
		# Step 3: display the result in table and the export button
		if len(resultsDict) == 0:
			st.warning('No matches found!')
		else:
			# build master DF with first column containing the search keywords and concatenate all in one table before displaying
			concat_dfs = []
			for item in resultsDict:
				resultsDict[item].insert(0,'SearchKey',item)
				concat_dfs.append(resultsDict[item])

			preFilterResultsDF = pd.concat(concat_dfs)
			
			# drop columns user filtered out for results display
			if len(col_filter) > 0:
				final_filter = ['SearchKey']+col_filter
				masterResultsDF = preFilterResultsDF[final_filter]
			else:
				masterResultsDF = preFilterResultsDF

			st.markdown('---')
			timestampStr = datetime.now().strftime("%Y%m%d_%H%M%S")
			fname='lexivault_bangla_'+timestampStr+'.csv'
			st.download_button('Export as .csv', masterResultsDF.to_csv(index=False).encode('utf-8'),file_name=fname,key='download_csv')

			gd = GridOptionsBuilder.from_dataframe(masterResultsDF)
			gd.configure_pagination(enabled=True)
			gd.configure_default_column(editable=True, groupable=True)

			gd.configure_selection(selection_mode='multiple',use_checkbox=False)
			gridoptions = gd.build()

			grid_table = AgGrid(
				masterResultsDF, 
				gridOptions=gridoptions,
				fit_columns_on_grid_load=True,
				update_mode=GridUpdateMode.SELECTION_CHANGED,
				theme='streamlit')


# ===========================================================
# INTERFACE : SEARCH FORM
# ===========================================================

with st.expander(label="**ABOUT: Bangla Lexicon**", expanded=True):
	st.markdown(
		"""
  		This lexicon is under construction, procedding a 570M word corpus (possibly reduced after further processing) consisting of the following:  
      		📚  Bengali TenTen Web & Wikipedia Corpus 2021 Ed. (Jakubíček et al., 2013; Suchomel, 2020)  
      		📚  Wikipedia & News (Kunchukuttan et al., 2020)  
      		Search Parameters:  
      		🔠  **word** **:blue[=]** the wordform  
      		🔢  **wordfreq** **:blue[=]** ppm frequency of the wordform  
      		🔠  **lemma** **:blue[=]** the lemma  
      		🔠  **pos** **:blue[=]** the part-of-speech  
		"""
		)

if 'is_expanded' not in st.session_state:
	st.session_state['is_expanded'] = True
expander_ = st.expander(label="**Bangla: Search & Filter**", expanded=st.session_state['is_expanded'])

with expander_:
	formContainer = st.container()

	col1, col2, col3, col4 = formContainer.columns((2,1,1,2))

	with col1:
		input_ = st.text_input(label = 'Input SearchKey', key='input_word_bangla', help='single entry search',placeholder='search')
		input_f = st.file_uploader(label='Upload SearchKey File (one per line)',key='input_file_bangla',help='multiple entry search',accept_multiple_files=False, type=['.txt','.csv'])
		#file_ = st.file_uploader(label='',key='input_file',accept_multiple_files=False, type=['.xlsx','.xls','.csv','.txt'])
	with col2:
		searchMode = st.selectbox(label='Search By',options=['Word','Lemma'])
		strictSearch = st.checkbox(label='Only show _**EXACT**_ matches', value=False, key='strict_search',help='check the box for an exact keyword match, leave it unchecked for any results close to your keyword')
		
		
		#pos_ = st.multiselect(
		#	label='Filter by Part-of-Speech (POS):',
		#	key='pos_lst',
		#	options=df_lex['pos'].unique(),
		#	default=df_lex['pos'].unique(),
		#	help='filter results by part-of-speech (POS) tag'
		#	)
		
	with col3:
		st.write("Frequency **Parts Per Million**")
		freq_min = st.number_input(label='MINIMUM',min_value=df_lex['wordfreq'].min(),max_value=df_lex['wordfreq'].max(),value=df_lex['wordfreq'].min())
		freq_max = st.number_input(label='MAXIMUM',min_value=df_lex['wordfreq'].min(),max_value=df_lex['wordfreq'].max(),value=df_lex['wordfreq'].max())

	with col4:
		col_filter = st.multiselect(
			label='Results columns to appear:',
			options=df_lex.columns.values.tolist(),
			default=df_lex.columns.values.tolist(),
			help='filter columns you wish to appear in the results table'
			)

	searchButton = st.button('SEARCH', key='submit_btn')


if searchButton:
	runSubmit()
	st.session_state['is_expanded'] = False



