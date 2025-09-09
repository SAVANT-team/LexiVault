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
from src.OutputGenerator import OutputGenerator
from src.configs import LANGUAGES

st.set_page_config(page_title='LexiVault Demo', page_icon=':book:', layout='wide')
st.markdown(
	"""
	<style>
	span[data-baseweb="tag"] {background-color: #4682B4 !important;}
	</style>
	""",
	unsafe_allow_html=True,
	)

# ===================
# Important variables
# ===================
language = ''
params = ['word']
corpus_uploaded = False

# =======================
# Interface: Page content
# =======================
st.header('🌱 User Workspace')
with st.expander(label='**🚀 Processing Wizard**', expanded=not corpus_uploaded):
    st.markdown(
        '''
		Thank you for contributing to LexiVault! Before you start, please make sure that your corpus is either a **.csv or .xlsx** 
        file with words listed in the first column, or a **.txt** raw text corpus (in line with [Brysbaert & New (2009)](https://pubmed.ncbi.nlm.nih.gov/19897807/). 
        It is recommended but not required that your corpus contains at least **16 million words**)
		'''
	)
    st.markdown(
        '''
        Please fill in the form below and update your corpus. Fields marked in :red[*] are mandatory.
        '''
    )

    # form to fill in
    col1, col2 = st.columns([1, 1])
    with col1:
        language = st.text_input('Language:red[*]:')
    with col2:
        parameters = st.multiselect(
            'Parameters:red[*]:',
            ['Word frequency', 'Morphological decomposition'],
            help="Choose which parameters you'd like to be able to query in the finished database."
        )
    corpus = st.file_uploader('Upload corpus:red[*]:', type=['txt', 'csv', 'xlsx'])
    submit = st.button('Submit')
    
    # ========================
    # Utils: Processing corpus
    # ========================
	# validate file submission; save & process
    run_wordfreq = False
    run_morph_decomp = False
    if 'Word frequency' in parameters:
        params.append('wordfreq')
        run_wordfreq = True
    if 'Morphological decomposition' in parameters:
        run_morph_decomp = True
    
    processor = InputProcessor(language, run_wordfreq, run_morph_decomp)
    filepath = ''
    if submit:
        if language is not None and parameters != [] and corpus is not None:
            # save file to temp
            filename = language + Path(corpus.name).suffix
            filepath = TEMP_DIR / filename
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
            corpus_uploaded = True
            
        else:
            st.error("Error submitting corpus. Please fill in all necessary fields.")

# ===========================================
# Interface: Generate temporary database here
# ===========================================

param_dict = {}
for p in params:
    param_dict[p] = 0

LANGUAGES[language] = {
    'filepath': '',
    'about': {
        'status': 0,
        'wordcount': 0,
        'sources': []
    },
    'parameters': param_dict
}

st.markdown(
    '''
    ### 🌿 Language Database
    After you submit the corpus, you will be able to search and query here. Please note that this function is
    temporary, and you will need to re-upload the corpus again after you close the session. If you would like to 
    add a persistent database to Language Databases, XXX
    '''
)
page = OutputGenerator(language)
page.run()