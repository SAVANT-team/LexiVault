import sys
import streamlit as st
from pathlib import Path

# import functions
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.input_processing import InputProcessor

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
st.header(":seedling: LexiVault Workshop: Add a new language database")
with st.expander(label="**Instructions**", expanded=True):
    st.markdown(
        """
			Thank you for contributing to LexiVAULT! Please make sure your keyword file meets the following requirements 🌟:
		"""
	)
    st.checkbox("Is either a **.csv or .xlsx** file with words listed in the first column, or a **.txt** raw text corpus "
    "(in line with [Brysbaert & New (2009)](https://pubmed.ncbi.nlm.nih.gov/19897807/) it is recommended but not required "
    "that your corpus contains at least **16 million words**).")

### variables for storing data from uploaded file
output_dir = Path(__file__).resolve().parents[1] / "temp_db/in"

with st.expander(label="**🚀 Processing Wizard**", expanded=True):
    st.markdown(
        """
        Please select which attributes you'd like in your language database and upload your corpus here. 
        After you hit the Submit button, a database will be generated.
        """
    )
    options = st.multiselect(
         "Desired attributes:",
         ["Word frequency", "Morphological decomposition"]
    )
    data = st.file_uploader("Choose a file:", type=["txt", "csv", "xlsx"])
    submit = st.button("Submit")

    if submit and data is not None:
        # for txt files
        if data.name.endswith("txt"):
            # output directory path + file path = save path
            updated_filename = "temp_" + data.name
            save_path = output_dir / updated_filename

            # actually save file in that path
            with open(save_path, "wb") as f:  # write bytes
                f.write(data.getbuffer())
            st.success(f"Text file saved to {save_path}")

            # process
            processor = InputProcessor(save_path)
            processor.process()

        # TODO files that are not txt files
        else:
            print("not a txt file")