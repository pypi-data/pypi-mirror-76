import pandas as pd
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(file):
    return '.' in file and file.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('disp_df',filename=filename))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def disp_df(filename):
    df = pd.read_csv("uploads/"+filename)
    header = df.columns
    record = df.values.tolist()
    return render_template('disp_df.html', header=header, record=record)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
    #app.run(host='0.0.0.0', port=5000)

'''
References
[1](https://flask.palletsprojects.com/en/1.1.x/)
[2](https://tkkm.tokyo/post-453/)
[3](https://tanuhack.com/df-to-web/)
[4](https://blog.codecamp.jp/programming-python-flask)
'''
