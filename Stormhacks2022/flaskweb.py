from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

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



if __name__ == '__main__':

    app.run(debug=True)

    # changes directory to uploads folder
    curr_dir = os.chdir(os.getcwd() + "/uploads/")

    files = os.listdir(os.getcwd())
    recent_file = max(files, key=os.path.getctime)

    print(recent_file)

    df = pd.read_csv('test.csv', sep=',', header=None)
    print(df)
