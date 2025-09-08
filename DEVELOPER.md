# LexiVault: Dev Guide
## How It Works
## Running Instructions
On MacOS, after you download the repository, run the following code to start:
```bashrc
python3 -m venv venv
source ven/bin/activate
pip install -r requirements.txt
streamlit run Home.py
```
## Directory Structure
```bashrc
/LexiVault
├─Home.py                   # app entry point
├─pages/                    # pages in the sidebar
├─db/                       # language databases underlying the pages
├─src/                      # source code: functions for building & querying language databases
│   ├─func_lib/             # source code for NLP functions
│   ├─InputProcessor.py     # class for generating csv file in db/ from user upload
│   ├─OutputGenerator.py    # class for generating interface in page/ from csv file in /db
├─temp/                     # temporary storage for inputs & outputs
```
## Yawen's Notes to Self
Things Yawen often forgets.
```bashrc
tree -I venv
```