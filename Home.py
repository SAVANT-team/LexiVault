import streamlit as st
from PIL import Image

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


st.header("Welcome to LexiVault! :book:")

col1, col2 = st.columns([1,3], gap="medium")

with col1:
	lexivault_logo = Image.open('img/lexivaultlogo.png')
	st.image(lexivault_logo, caption=None, width=360)

with col2:
	st.markdown("**LexiVault** is a collection of morphologically parsed Lexical Stimulus Databases for low-or-no resource languages modeled after similar resources that have facilitated research on well-studied languages such as English and Dutch (eg. the CELEX database, Baayen et al. 1995, and the English Lexicon Project, Balota et al. 2007).")
	st.markdown("This project is designed to support stimuli creation for psycholinguistic experiments with single word-based paradigms. The data within is thus focused on lexical and sublexical statistics, including morpheme frequency and phonotactic probability.")
	st.markdown("LexiVault is a work in progress. Currently we are developing lexicons for Bangla, Slovenian, Bosnian-Croatian-Serbian, and different dialects of Arabic. Check out the template page and contact us if you are interested in joining LexiVault and contributing your language lexicons!")

st.write("---")

col3, col4 = st.columns([1,3], gap="medium")
with col3:
	savant_logo = Image.open('img/savant-logo.png')
	st.image(savant_logo, caption=None, width=360)

with col4:
	st.markdown("The development of this tool falls within a wider research context studying the **S**ystematicity **a**nd **V**ariation in Word Structure Processing Across Languages through **a** **N**euro-**T**ypology Approach, a.k.a. The [SAVANT](https://savant.qmul.ac.uk/) Project.")
	st.markdown("This project's goals are to leverage the diversity of the  languages of the world-- with respect to their morphological structure, phonological transparency, sublexical syntactic operations, and writing systems-- to investigate how language is stored and processed in the mind and brain.")
	st.markdown("Support for development of LexiVault is gratefully acknowledged through the United Kingdom Economic and Social Research Council (ESRC) ES/V000012/1")

st.write("---")

with st.expander(label="**CONTACT US**", expanded=True):
	st.info('  For general inquiries or contributions to the repository, get in touch with us through the project [GitHub Page](https://github.com/SAVANT-team/LexiVault)',icon="✉️")
	#st.markdown(
	#	"""
	#	- For general inquiries or contributions to the repository, get in touch with us through nyuad.savant@nyu.edu
	#	- To naviga the repository, get in touch with us through nyuad.savant@nyu.edu
	#	"""
	#	)
