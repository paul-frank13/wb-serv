from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file
import numpy as np
import joblib
import os
import pandas as pd


app = Flask(__name__)
knn = joblib.load('knn.pkl')

@app.route('/')
def hello_world():
    return '<h3>Hello world!</h3>'


@app.route('/user/<username>')
def show_user(username):
    username = int(username) * int(username)
    return 'User {}'.format(username)


def print_average(arr):
    return 0 if not arr else sum(arr) / len(arr)


@app.route('/avg/<nums>')
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    nums = print_average(nums)
    return str(nums)


@app.route('/iris/<param>')
def iris(param):

    param = param.split(',')
    param = [float(num) for num in param]

    flowers_src = os.listdir(os.getcwd() + '/static')

    knn = joblib.load('knn.pkl')

    param = np.array(param).reshape(1, -1)
    predict = knn.predict(param)
    
    import random

    flower_src = flowers_src[random.randint(0,2)]

    return "<img src='/static/{}'>".format(flower_src)


@app.route('/iris_post', methods=["GET", "POST"])
def add_message():
    if request.method == 'POST':

        try:
            content = request.get_json()
            
            param = content['flower'].split(',')
            param = [float(num) for num in param]

            flowers_src = os.listdir(os.getcwd() + '/static')

            knn = joblib.load('knn.pkl')

            param = np.array(param).reshape(1, -1)
            predict = knn.predict(param)

            import random

            flower_src = flowers_src[random.randint(0,2)]

            predict = {'class':str(predict[0])}
        except:
            return redirect(url_for('bad_request'))

        return "<img src='/static/{}'>".format(flower_src)
    else:
        
        return 'GET'

@app.route('/badrequest400')
def bad_request():
    return abort(400)

from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

app.config.update(dict(
    SECRET_KEY="34",
    WTF_CSRF_SECRET_KEY="434"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():

        f = form.file.data  
        filename = str(form.name.data)
        # f.save(os.path.join(filename))

        df = pd.read_csv(f, header=None)

        predict = knn.predict(df)

        result = pd.DataFrame(predict)

        filename = filename + '.csv'
        result.to_csv(filename, header=None, index=False)

        return send_file(filename, 
                        mimetype='text/csv', 
                        attachment_filename=filename, 
                        as_attachment=True)

    return render_template('submit.html', form=form)

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename + 'uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File saved successfully!'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''