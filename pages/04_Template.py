import streamlit as st

import pandas as pd
import os
import re

from datetime import datetime

from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder


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

# 992,960,152

def ppMillion(text):
	raw_freq = float(text)
	ppmil_freq = raw_freq / 992960152 # total freq in COCA for template sample db, based on https://www.wordfrequency.info/files.asp
	return round(ppmil_freq, 3)

def mapSearchModeToColumn(smode):
	#st.write('Inside map func with mode=' + smode)
	col_name = 'word'
	options_lst = ['Word (e.g. having)','Lemma (e.g. have)']
	colname_lst = ['word','lemma']
	for i in range(0,len(options_lst)):
		if smode.strip() == options_lst[i].strip():
			col_name = colname_lst[i]
	#st.write('Final mapped value of column=' + col_name)
	return col_name

def mapLabeltoPOS(chosen_labels):
	
	pos_list = []
	label_lst = ["art","prep","verb","conj","inf","pron","det","not","adv","noun","ex","num","adj","inter"]
	colname_lst = ["a","i","v","c","t","p","d","x","r","n","e","m","j","u"]
	for x in chosen_labels:
		for i in range(0,len(label_lst)):
			if x.strip() == label_lst[i].strip():
				pos_list.append(colname_lst[i])
	#st.write('Final mapped value of column=' + col_name)
	return pos_list


# ==================================================================
# LOADING THE LEXICON FROM CSV
# ==================================================================
@st.cache_data(experimental_allow_widgets=True)
def load_lexicon():
	fpath = os.path.join(os.path.join(os.getcwd(),'lexivault_db'),'eng_streamlit.csv') # MSA_formatted.csv
	dflx = pd.read_csv(fpath,sep='\t',encoding='utf-8',low_memory=False)
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
	keyword_ = keyword
	pos_filter = postags
	searchCol = searchmode

	if exactMatch:
		results = df_lex.query("{0} == @keyword_ & pos == @pos_filter".format(searchCol))
	else:
		results = df_lex.query("{0}.str.contains(@keyword_) & pos == @pos_filter".format(searchCol))

	return results #pd.DataFrame()

def runSubmit():
	if st.session_state['input_word_template'] is None and st.session_state['input_file_template'] is None:
		st.warning('Please enter a keyword or upload a file to search')
	else:
		# ##################
		# Step 1: get the input
		# if there's a file - use that, otherwise default to the text area
		input_list = [] # this can be one item from the text area or many from the file
		if not(st.session_state['input_file_template'] is None):
			dfinput=pd.read_csv(input_f, sep=" ", header=None)
			input_list.extend(dfinput[dfinput.columns[0]].values.tolist())
		else:
			tokenized = str(st.session_state['input_word_template']).strip().split()
			input_list.extend(tokenized)

		input_wrd = '\t|\t'.join(input_list)
		search_col_name = mapSearchModeToColumn(searchMode)
		pos_choices = mapLabeltoPOS(st.session_state['pos_lst'])
		exact_match = st.session_state['strict_search']
		if len(pos_choices) == 0:
			pos_choices = df_lex['pos'].unique().tolist()
		#st.write('keyword(s) = ' + input_wrd)
		#st.write('search_by_value = ' + search_col_name)
		#st.write('POS selection:', pos_choices)
		#input_wrd = input_list[0]
		#st.write('starting with => ' + input_wrd)

		# ##################
		# Step 2: run the search query
		resultsDict = {}
		for item in input_list:
			item_results_df = getResults(item, search_col_name, pos_choices, exact_match)
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
				resultsDict[item].insert(0,'Keyword',item)
				concat_dfs.append(resultsDict[item])

			preFilterResultsDF = pd.concat(concat_dfs)
			
			# drop columns user filtered out for results display
			if len(col_filter) > 0:
				final_filter = ['Keyword'].extend(col_filter)
				masterResultsDF = preFilterResultsDF[final_filter]
			else:
				masterResultsDF = preFilterResultsDF

			st.markdown('---')
			timestampStr = datetime.now().strftime("%Y%m%d_%H%M%S")
			fname='lexivault_template_'+timestampStr+'.csv'
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

		# ####################
		# Step 4: clear session states for next search



# ===========================================================
# INTERFACE : SEARCH FORM
# ===========================================================

with st.expander(label="**How to Add a New Language**", expanded=True):
	st.markdown(
		"""
		To contribute a lexical database to LexiVault, you should start with:  
    		📚  A minimum 16M word content-corpus, following Brysbaert & New (2009)  
      		Generate a dataset for Lexivault with:  
      		✅  A unique word list with frequencies  
		✅  Character bi-and-tri-grams with frequencies  
  		✅  Grapheme-to-phoneme transcription  
    		✅  Phoneme-by-phoneme surprisal (Hale, 2001)  
      		If your language has reliable morphosyntactic processing & annotation tools available, you may also include:  
  		⭐  Part-of-speech tagging  
    		⭐  Morpheme frequencies and morpheme-to-word transition probability measures ❕:red[_requires stemming_]  
      		If you're interested in developing a psycholinguistically relevant lexicon for your language of interest and contributing that lexicon to LexiVault, contact us for assistance and also check out the project [GitHub](https://github.com/SAVANT-team/LexiVault) for helpful scripts and tips to accomplish the above.
		"""
		)

if 'is_expanded' not in st.session_state:
	st.session_state['is_expanded'] = True
expander_ = st.expander(label="**Template: Search & Filter**", expanded=st.session_state['is_expanded'])

with expander_:
	formContainer = st.container()

	col1, col2, col3, col4 = formContainer.columns((1,1,1,1)) # inside columns() set ratio sizes (2,1,1,2)

	with col1:
		input_ = st.text_input(label = 'Input Keyword', key='input_word_template', help='single entry search',placeholder='search')
		input_f = st.file_uploader(label='Upload Keyword File (one keyword per line)',key='input_file_template',help='multiple entry search',accept_multiple_files=False, type=['.txt','.csv'])
	with col2:
		strictSearch = st.checkbox(label='Only show _**EXACT**_ matches', value=False, key='strict_search',help='check the box for an exact keyword match, leave it unchecked for any results close to your keyword')
		searchMode = st.selectbox(label='Search By',options=['Word (e.g. having)','Lemma (e.g. have)'])
		pos_ = st.multiselect(
			label='Filter by Part-of-Speech (POS):',
			key='pos_lst',
			options=['adj','adv','art','conj','det','ex','inf','inter','not','noun','num','prep','pron','verb'],
			default=['adj','adv','art','conj','det','ex','inf','inter','not','noun','num','prep','pron','verb'],
			help='filter results by part-of-speech (POS) tag'
			)
	with col3:
		st.write("Frequency")
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



