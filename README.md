# SFAC-LP Admission chatbot
A WIP text-based chatbot made with RASA framework via python

aims to be conversational

5/15/2014 TEST CHATBOT

# Configurations:
    This rasa project is supported with:
    - Python Version:   3.8.10 (In blexbottt's R5-3600/B450M desktop)
    - Rasa Version:     3.6.20

# CHECKLIST (say DONE if completed)
- Connect to website (html-php)
    - configure dataset in the front-end
- MongoDB (Knowledge Management/Base??)
- BERT
- NLPaug (for data augmentation)
- ~~LLM integration via OpenAI?~~
    # What about the dataset? is it:
    - For college-related only?
    - K-12?
    - Or, Both K-12 and College?

# Commands:

Activate venv - python 3.8.10

venv\Scripts\activate

- rasa train
- rasa shell

rasa run --enable-api 
rasa run --enable-api --cors "*"

rasa run -m models --enable-api --cors "*"

rasa run --enable-api --cors "*" --model <path>

rasa run --enable-api --cors "*" --port 5005

# Installation problems
- if "mattermostwrapper" issue:
    - pip install setuptools==58.0.4
    - pip install rasa
    - rasa --version

- if c:\users\user\cbproject\rasa-env\lib\site-packages\rasa\core\channels\socketio.py:236: 
    _RuntimeWarning: coroutine ‘AsyncServer.enter_room’ was never awaited_
    - try this below:![async_236_warning](https://github.com/user-attachments/assets/dbbd79ad-8974-40f4-a95b-156eda87b33c)

        
