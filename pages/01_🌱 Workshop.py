import streamlit as st

### SET CONFIG
st.set_page_config(page_title="Workshop", page_icon=":seedling:", layout="wide")

st.markdown(
	"""
	<style>
	span[data-baseweb="tag"] {background-color: #4682B4 !important;}
	</style>
	""",
	unsafe_allow_html=True,
)

### ================================================
### INTERFACE / CONTENT
### ================================================
st.header(":seedling: LexiVAULT Workshop: Add a new language database")
with st.expander(label="**Instructions**", expanded=True):
    st.markdown(
        """
			Thank you for contributing to LexiVAULT! Please make sure your keyword file meets the following requirements 🌟:
		"""
	)
    st.checkbox("Contains at least **16 million words**, in line with [Brysbaert & New (2009)](https://pubmed.ncbi.nlm.nih.gov/19897807/)")
    st.checkbox("Is either a **.csv or .xlsx** file with words listed in the first column, or a **.txt** raw text corpus")
    st.markdown(
        """
			Post processing, you will have a searchable corpus with the following features: TODO
		"""
	)

### process corpus
# set up state tracking for which step you are on
if 'step' not in st.session_state:
    st.session_state.step = 1

total_steps = 5

with st.expander(label="**🚀 Processing Wizard**", expanded=True):
    st.progress(st.session_state.step/total_steps)
    
	### STEP 1: upload file
    if st.session_state.step == 1:
        st.markdown(
            """
				### Step 1: Upload file  
			"""
		)
        st.markdown(
            """
				After this step, your corpus will be read into a PD dataframe with attribute wordfreq for each word. If you your data contains lemma or stem for each word, frequencies for these will also be generated.
			"""     
		)
        st.markdown(
            """
        		You may have to click on the "next" button twice to go forward.
			"""
		)
        data = st.file_uploader("Choose a file:", type=["txt", "csv", "xlsx"])
        
    ### STEP 2: text processing
    if st.session_state.step == 2:
        st.markdown(
            """
				### Step 2: Text processing
			"""
		)
        st.markdown(
            """
        		Unfortunately the back & next buttons are somewhat finicky, so please double-check before you move on—you may not be able to go back.  
			"""
		)
        
    ### STEP 3: speech data processing
    if st.session_state.step == 3:
        st.markdown(
            """
				### Step 3: Speech data processing 
			"""
		)
        st.markdown(
            """
        		Unfortunately the back & next buttons are somewhat finicky, so please double-check before you move on—you may not be able to go back.  
			"""
		)
        
    ### STEP 4: behavioural data processing
    if st.session_state.step == 4:
        st.markdown(
            """
				### Step 4: Behavioral data processing
			"""
		)
        st.markdown(
            """
        		Unfortunately the back & next buttons are somewhat finicky, so please double-check before you move on—you may not be able to go back.  
			"""
		)
        
    ### STEP 5: describe your corpus
    if st.session_state.step == 5:
        st.markdown(
            """
				### Step 5: Summary
			"""
		)
        st.markdown(
            """
        		Unfortunately the back & next buttons are somewhat finicky, so please double-check before you move on—you may not be able to go back.  
			"""
		)
    
	### BUTTONS
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        back_clicked = st.button("<Back", disabled=st.session_state.step <= 1)
    with col2:
        next_clicked = st.button("Next >", disabled=st.session_state.step >= total_steps)
    with col3:
        st.write("")
        
	# this logic is outside layout block due to state management quirks
    if back_clicked:
        st.session_state.step -= 1
    if next_clicked:
        st.session_state.step += 1

### ================================================
### FUNCTIONALITY
### ================================================