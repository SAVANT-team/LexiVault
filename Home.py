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


st.header("Welcome to LexiVAULT! :book:")

col1, col2 = st.columns(2)

with col1:
	
	lexivault_logo = Image.open('lexivault-logo.png')
	st.image(lexivault_logo, caption=None, width=400)

with col2:
	st.markdown(
		"""
		**LexiVAULT** is a collection of morphologically parsed Lexical Stimulus Databases for low-or-no resource languages 
		modeled after similar resources that have facilitated research on well-studied languages such as English and Dutch 
		(eg. the CELEX database, Baayen et al. 1995, and the English Lexicon Project, Balota et al. 2007).\\
		\\
		Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse in lectus quam. Aliquam tempus enim in odio elementum semper. 
		Suspendisse ut elementum turpis, sed eleifend lectus. Phasellus dapibus egestas neque, id fermentum nunc. In eu tortor leo. 
		Nulla ornare sit amet odio vitae molestie. Cras tincidunt mi purus, in convallis nulla scelerisque a. Duis vel ante sagittis lectus mollis aliquet et sit amet mi.
		"""
	)

st.write("---")

col3, col4 = st.columns([1,4], gap="small")
with col3:
	savant_logo = Image.open('img/savant-logo.png')
	st.image(savant_logo, caption=None, width=200)

with col4:
	st.markdown(
		"""
		The development of this tool falls within a wider research context studying the **S**ystematicity **a**nd **V**ariation 
		in Word Structure Processing Across Languages through **a** **N**euro-**T**ypology Approach, 
		a.k.a. The [SAVANT](https://savant.qmul.ac.uk/) Project.\\
		\\
		Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse in lectus quam. Aliquam tempus enim in odio elementum semper. 
		Suspendisse ut elementum turpis, sed eleifend lectus. Phasellus dapibus egestas neque, id fermentum nunc. In eu tortor leo.
		Nulla ornare sit amet odio vitae molestie. Cras tincidunt mi purus, in convallis nulla scelerisque a. Duis vel ante sagittis lectus mollis aliquet et sit amet mi.\\
		Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse in lectus quam. Aliquam tempus enim in odio elementum semper. 
		Suspendisse ut elementum turpis, sed eleifend lectus. Phasellus dapibus egestas neque, id fermentum nunc. In eu tortor leo.
		Nulla ornare sit amet odio vitae molestie. Cras tincidunt mi purus, in convallis nulla scelerisque a. Duis vel ante sagittis lectus mollis aliquet et sit amet mi.
		"""
	)

st.write("---")

with st.expander(label="**CONTACT US**", expanded=True):
	st.markdown(
		"""
		This is placeholder area for contact e-mails in the long run \\
		- For general inquiries, contact J. Doe at [so-and-so@address.com](https://www.google.com)
		- To contribute to the databases, contact S. Smith this person at [add-more@data.com](https://www.google.com)
		- To report issues, contact J.S. Shmoe at [dont-know@dontcare.com](https://www.google.com)
		"""
		)
