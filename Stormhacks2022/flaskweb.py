from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
import re

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
var = None

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('home', name = filename))


def category_map(description):
    description_category_map = {
        r"(?i)Riot*Games": "Entertainment",
        r"(?i)JUICE": "Food",
        r"(?i)UBER*EATS": "Food",
        r"(?i)UBER": "Transportation",
    }

    for search_term, category in description_category_map.items():
        if(re.search(search_term, description)):
            return category

    return "Unknown"
    

def add_categories(data_frame):
    data_frame["CATEGORIES"] = data_frame["DESCRIPTION"].map(category_map)



if __name__ == '__main__':

    app.run(debug=True)

    # changes directory to uploads folder
    curr_dir = os.chdir(os.getcwd() + "/uploads/")

    files = os.listdir(os.getcwd())
    recent_file = max(files, key=os.path.getctime)

    print(recent_file)

    # column names since the bank statements don't include them by default
    #colnames=['TIMESTAMP', 'DESCRIPTION', 'WITHDRAWALS', 'DEPOSITS'] 
    colnames=['TIMESTAMP', 'DESCRIPTION', 'AMOUNT'] 
    df = pd.read_csv('test.csv', sep=',', header=None, names=colnames)
    add_categories(df)
    print(df)
