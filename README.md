Installing/running website (on windows):

first navigate to the location of the repository on cmd

installing:
```
py -3 -m venv ./.venv
.venv\Scripts\activate
pip install -r requirements.txt
```

running:
```
set FLASK_APP=flaskweb
set FLASK_ENV=development
flask run
```

![image](https://user-images.githubusercontent.com/3858420/154854406-26fb62c3-f366-4933-a2fa-6cdc3559daab.png)
![image](https://user-images.githubusercontent.com/3858420/154854370-8b2af44f-b653-482d-abaf-4494f8b1da04.png)
