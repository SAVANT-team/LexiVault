import streamlit as st
import sys
from pathlib import Path

# resolve file paths
PROJ_ROOT = Path(__file__).resolve().parent.parent
TEMP_DIR = Path('./temp')
DB_DIR = Path('./db')
sys.path.append(str(PROJ_ROOT / 'src'))

# import stuff we wrote
from src.InputProcessor import InputProcessor

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
st.header('🌱 Workshop')
with st.expander(label='**🚀 Processing Wizard**', expanded=True):
    st.markdown(
        '''
		Thank you for contributing to LexiVault! Before you start, please make sure that your corpus meets the following requirements:
		'''
	)
    st.checkbox("Is either a **.csv or .xlsx** file with words listed in the first column, or a **.txt** raw text corpus "
    "(in line with [Brysbaert & New (2009)](https://pubmed.ncbi.nlm.nih.gov/19897807/) it is recommended but not required "
    "that your corpus contains at least **16 million words**).")
    st.markdown(
        '''
        Please upload your corpus and select which search parameters you'd like to have in your language database.
        '''
    )
    nlp_parameters = st.multiselect(
        'Parameters:',
        ['Word frequency', 'Morphological decomposition']
	)
    corpus = st.file_uploader('Choose a file:', type=['txt', 'csv', 'xlsx'])
    submit = st.button('Submit')
    
	# validate file submission; save & process
    run_wordfreq: bool = 'Word frequency' in nlp_parameters
    processor = InputProcessor(run_wordfreq)
    filepath = ''
    if submit and corpus is not None:
        # save file to temp
        filepath = TEMP_DIR / corpus.name
        with open(filepath, 'wb') as f:
            f.write(corpus.getbuffer())
        st.success(f'File saved to {filepath}')
        
		# now process
        if corpus.name.endswith('txt'):
            processor.process_txt(filepath)
        elif corpus.name.endswith('csv'):
            pass
        elif corpus.name.endswith('xlsx'):
            pass

        # save final csv file to /db
        #TODO