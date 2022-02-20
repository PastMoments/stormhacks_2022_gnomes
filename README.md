Installing/running website (on windows):

first navigate to the location of the repository on cmd

installing:
**py -3 -m venv ./.venv
.venv\Scripts\activate
pip install -r requirements.txt


running:
'''
set FLASK_APP=flaskweb
set FLASK_ENV=development
flask run
'''
