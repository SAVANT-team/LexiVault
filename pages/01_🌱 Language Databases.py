import streamlit as st
import sys
from pathlib import Path

# resolve project root
PROJ_ROOT = Path(__file__).resolve().parent.parent
TEMP_DIR = Path('./temp')
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
st.header('🗃️ Language Databases')
with st.expander(label='**🚀 Processing Wizard**', expanded=True):
    st.markdown(
        '''
		Please upload your corpus and select which attributes you'd like to have in your language database.
		'''
	)
    nlp_attributes = st.multiselect(
        'Attributes:',
        ['Word frequency', 'Morphological decomposition']
	)
    corpus = st.file_uploader('Choose a file:', type=['txt', 'csv', 'xlsx'])
    submit = st.button('Submit')
    
	# validate file submission; save & process
    run_wordfreq: bool = 'Word frequency' in nlp_attributes
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