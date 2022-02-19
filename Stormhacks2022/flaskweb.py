from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
var = None

@app.route("/")
def home():
    #return render_template('home.html')
    return render_template('test.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('home', name = filename))

def category_map(description):
    pass
    

def add_categories(data_frame):
    data_frame["CATEGORIES"] = data_frame["DESCRIPTION"].map(lambda x: f"{x} shea")


if __name__ == '__main__':

    app.run(debug=True)

    # changes directory to uploads folder
    ref_dir = os.getcwd()

    curr_dir = os.chdir(ref_dir + "/uploads/")

    files = os.listdir(os.getcwd())
    recent_file = max(files, key=os.path.getctime)

    print(recent_file)

    # column names since the bank statements don't include them by default
    # colnames=['TIMESTAMP', 'DESCRIPTION', 'WITHDRAWALS', 'DEPOSITS']
    colnames=['TIMESTAMP', 'DESCRIPTION', 'AMOUNT']
    df = pd.read_csv('test.csv', sep=',', header=None, names=colnames)
    add_categories(df)
    print(df)

    prev_dir = os.chdir(ref_dir + "/templates")
    html_file = os.listdir(os.getcwd())
    print(html_file)

    result = df.to_html()
    text_file = open("test.html", "w")
    text_file.write(result)
    text_file.close()




