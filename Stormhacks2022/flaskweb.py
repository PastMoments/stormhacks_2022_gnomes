from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import pandas as pd
import re
import sys
import numpy as np

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_53Ff3"F4QFdz\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'
var = None

@app.route("/")
def home():
    df_json = session.get("transactions")
    if df_json:
        df = pd.read_json(df_json, dtype=True)
        df = df.fillna(value=np.nan)
        return render_template('home.html', tables=[df.to_html(classes='data', na_rep='')], titles=df.columns.values)
    else:
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
    return redirect(url_for('home'))

def category_map(description):                                                                                                            
    description_category_map = {                                                                                                          
        r"(?i)Riot*Games": "Entertainment",                                                                                               
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
        r"(?i)Ramen": "Food",                                                                                                             
        r"(?i)DR": "Health",                                                                                                              
        r"(?i)Hair": "Health",                                                                                                            
                                                                                                                                          
    }                                                                                                                                     
                                                                                                                                          
    for search_term, category in description_category_map.items():                                                                        
        if(re.search(search_term, description)):                                                                                          
            return category                                                                                                               
                                                                                                                                          
    return "Other"
    

def add_categories(data_frame):
    data_frame["CATEGORIES"] = data_frame["DESCRIPTION"].map(category_map)


if __name__ == "__main__":
    app.run(debug=True)




