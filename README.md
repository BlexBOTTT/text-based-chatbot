# SFAC-LP Admission chatbot
A WIP text-based chatbot made with RASA framework via python

aims to be conversational

5/15/2014 TEST CHATBOT

# Configurations:
    This rasa project is supported with:
    - Python Version:   3.8.10
    - Rasa Version:     3.6.20

    - Python Version:   3.10.11
    - pip version:      23.0.1
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

.venv\Scripts\activate

- rasa train

# command to talk to the chatbot in the CLI (command line interface)
- rasa shell

# default command for conversing with the chatbot in the web's chat widget
rasa run --enable-api
rasa run --enable-api --cors "*"
# command if has multiple models saved and want to slect a particular .tar.gz one
rasa run --enable-api --cors "*" --model <path>

# Installation problems
- FOR FiRTST time installing rasa:
    - if errors are:
        "subprocess-exited-with-error", "metadata-generation-failed", and
        "mattermostwrapper" issue:
        ```
        pip install setuptools==58.0.4
        pip install mattermostwrapper==2.2
        pip install rasa
        rasa --version
        ```

- if c:\users\USER\cbproject\rasa-env\lib\site-packages\rasa\core\channels\socketio.py:236: 
    _RuntimeWarning: coroutine ‘AsyncServer.enter_room’ was never awaited_
    - try this below:![async_236_warning](docs/images/async_236_warning.png)
    

- if Powershell's "ExecutionPolicy" (which usually trying to use venv in powershell):
    ![Execution policy](docs/images/execution_policy.png)
    - try this below:
        - open windows powershell and execute `Get-ExecutionPolicy`
        - if the response was `Restricted`, 
        - `apply `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
        - then press `Y`
        - recheck the VSCode's terminal window and retry `.\venv\Scripts\Activate` in the terminal, and see if it works and see if `(venv)` appeared so it may look like "`(venv) PS C:\Users\USER\Documents\admi-chatbot>`".
        - if you want to revert to old changes, type:
            - `Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser`, then press `Y`




        
