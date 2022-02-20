from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import pandas as pd
import re
import sys
import numpy as np

import datetime

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = b'_53Ff3"F4QFdz\n\xec]/'
var = None

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(filename)

            # column names since the bank statements don't include them by default
            colnames=['TIMESTAMP', 'DESCRIPTION', 'WITHDRAWALS', 'DEPOSITS', 'BALANCE']
            df = pd.read_csv(filename, sep=',', header=None, names=colnames)
            add_categories(df)

            session["transactions"] = df.to_json()
        else:
            session["transactions"] = ""

    return redirect(url_for('correct_categories'))

@app.route('/correction')
def correct_categories():
    return render_template('correction.html')

# pre-process data for the withdrawal and deposit plots
def data_for_graph(df, col):    # col = df.columns[n]
    data = {
        "Timestamp": df[df.columns[0]],
        col: []
    }
    sum = 0

    for i in range(len(df)):
        df[col] = df[col].fillna(0)
        sum += df.loc[i, col]
        data[col].append(sum)

    result = pd.DataFrame(data)
    return result

@app.route('/dashboard')
def dashboard():
    df_json = session.get("transactions")
    if df_json:
        df = pd.read_json(df_json, dtype=True)
        df = df.fillna(value=np.nan)

        pie_data = [2,10,4]

        x_axis = []
        y_axis = []
        # wd = data_for_graph(df, df.columns[2])
        # dp = data_for_graph(df, df.columns[3])
        for i in range(len(df)):
            x_axis.append((df.loc[i, df.columns[0]]).strftime('%D'))
            y_axis.append(df.loc[i, df.columns[4]])

        return render_template('dashboard.html', pie_data=pie_data, x_axis=x_axis, y_axis=y_axis, tables=[df.to_html(classes='data', na_rep='')], titles=df.columns.values)
    else:
        return render_template('home.html')


def category_map(description):
    description_category_map = {
        r"(?i)Riot*": "Entertainment",
        r"(?i)JUICE": "Food",
        r"(?i)UBER*EATS": "Food",
        r"(?i)UBER": "Transportation",
        r"(?i)DD": "Food",
        r"(?i)DOORDASH": "Food",
        r"(?i)Spotify": "Entertainment",
        r"(?i)\w*Market": "Food",
        r"(?i)DHL": "Devliery",
        r"(?i)Home": "Housing",
        r"(?i)Landmark": "Entertainment",
        r"(?i)Steam": "Entertainment",
        r"(?i)Ra-men": "Food",
        r"(?i)DR": "Health",
        r"(?i)Hair": "Health",
        r"(?i)Happymeat": "Income",
        r"(?i)Interest": "Income",
        r"(?i)WPS": "Income",

    }

    for search_term, category in description_category_map.items():
        if(re.search(search_term, description)):
            return category

    return "Other"


def add_categories(data_frame):
    data_frame["CATEGORIES"] = data_frame["DESCRIPTION"].map(category_map)

if __name__ == "__main__":
    app.run(debug=True)
