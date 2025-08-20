# LexiVault: Guide for devs

## How it works
### Database creation:
- User-submitted data undergoes processing and ends up a ```.csv``` file in ```/temp_db```
- A function converts this ```.csv``` file into a ```.py``` file

### Database query:

## Directory structure
```
/LexiVault
├─Home.py                       # entry point: page to run
├─src/                          # source code: functions for building & querying language databases
│   ├── function_lib.py         # library of functions for extracting metrics
│   ├── input_processing.py     # functions for processing user input
├─pages/                        # user-facing pages
├─lexivault_db/                 # source dbs for languages in pages
├─temp_db/                      # temporary storage for user-submitted corpuses
├─utils/
├─img/
```