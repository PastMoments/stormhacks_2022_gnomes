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
            print(filename)
            f.save(filename)

            # column names since the bank statements don't include them by default
            colnames=['TIMESTAMP', 'DESCRIPTION', 'WITHDRAWALS', 'DEPOSITS', 'BALANCE']
            df = pd.read_csv(filename, sep=',', header=None, names=colnames)
            add_categories(df)

            session["transactions"] = df.to_json(orient='table')
        else:
            session["transactions"] = ""

    return redirect(url_for('correct_categories'))

@app.route('/correction')
def correct_categories():
    if not session.get("transactions"):
        return redirect(url_for('home'))

    df_json = session.get("transactions")
    if df_json:
        df = pd.read_json(df_json, orient='table')
        df = df.fillna(value=np.nan)

        others = df.copy()
        others = others[others["CATEGORIES"] == "Other"]


        
        dropdown ='<div class="drop"> \
        <form action="404" method="get"><select name="dropselect"> \
        <option value="Other">Other</option> \
        <option value="Food">Food</option> \
        <option value="Entertainment">Entertainment</option> \
        <option value="Health">Health</option> \
        <option value="Housing">Housing</option> \
        <option value="Delivery">Delivery</option> \
        <option value="Income">Income</option> \
</select> \
</form> \
</div>'

        others = others.assign(CATEGORIES=dropdown)

    htmlothers = [others.to_html(classes='table', na_rep='', border=0, index=False, escape=False,)]
    print(htmlothers)
    print(others.columns.values)
    return render_template('correction.html', tables=htmlothers, titles=others.columns.values)

# pre-process data for the withdrawal and deposit plots
def data_for_graph(df, col):  # col = df.columns[n]
    sum = 0
    result = []

    for i in range(len(df)):
        df[col] = df[col].fillna(0)
        sum += df.loc[i, col]
        result.append(sum)

    return result

@app.route('/dashboard')
def dashboard():
    df_json = session.get("transactions")
    if df_json:
        df = pd.read_json(df_json, orient='table')
        df = df.fillna(value=np.nan)

        chogama = df.copy()
        chogama = chogama.fillna(value=0)

        chogama['DEPOSITS'] = chogama['DEPOSITS'].astype(str)
        chogama['WITHDRAWALS'] = chogama['WITHDRAWALS'].astype(str)
        chogama['DEPOSITS'] = pd.to_numeric(chogama['DEPOSITS'].str.replace(',', ''))
        chogama['WITHDRAWALS'] = pd.to_numeric(chogama['WITHDRAWALS'].str.replace(',', ''))

        # line graph related
        for i in range(len(df) - 1):
            wd_total = 0
            dp_total = 0

            if chogama['TIMESTAMP'][i] == chogama['TIMESTAMP'][i + 1]:
                wd_total = chogama['WITHDRAWALS'][i] + chogama['WITHDRAWALS'][i + 1]
                dp_total = chogama['DEPOSITS'][i] + chogama['DEPOSITS'][i + 1]
                chogama.at[i + 1, 'WITHDRAWALS'] = wd_total
                chogama.at[i + 1, 'DEPOSITS'] = dp_total

        chogama.drop_duplicates(subset=['TIMESTAMP'], keep='last', inplace=True)
        chogama = chogama.reset_index(drop=True)

        x_axis = []
        balance = []

        for i in range(len(chogama)):
            x_axis.append((chogama.loc[i, chogama.columns[0]]).strftime('%D'))
            balance.append(chogama.loc[i, chogama.columns[4]])

        # type = list
        wd = data_for_graph(chogama, chogama.columns[2])
        dp = data_for_graph(chogama, chogama.columns[3])

        chogama = chogama.reset_index()


        pie_categories = {}
        for index, row in chogama.iterrows():
            if not pie_categories.get(row['CATEGORIES']):
                pie_categories[row['CATEGORIES']] = 0
            pie_categories[row['CATEGORIES']] += row['WITHDRAWALS']

        pie_category, pie_data = zip(*pie_categories.items())
        pie_data = map(round, pie_data)


        return render_template('dashboard.html', pie_data=pie_data, pie_category=pie_category, x_axis=x_axis, balance=balance, withdrawal=wd,
                               deposit=dp)
    else:
        return redirect(url_for('home'))


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
        r"(?i)DHL": "Delivery",
        r"(?i)Home": "Housing",
        r"(?i)Landmark": "Entertainment",
        r"(?i)Steam": "Entertainment",
        r"(?i)Ra-men": "Food",
        r"(?i)DR": "Health",
        r"(?i)Hair": "Health",
        r"(?i)Happymeat": "Income",
        r"(?i)Interest": "Income",
        r"(?i)WPS": "Income",
        r"(?i)Rent": "Housing",

    }

    for search_term, category in description_category_map.items():
        if(re.search(search_term, description)):
            return category

    return "Other"


def add_categories(data_frame):
    data_frame["CATEGORIES"] = data_frame["DESCRIPTION"].map(category_map)

if __name__ == "__main__":
    app.run(debug=True)
