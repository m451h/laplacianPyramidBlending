import os
from flask import Flask, request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from blend import blendTwoImages


UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        file1 = request.files['file1']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input1.png'))
        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input2.png'))
            
        return redirect('/blend')
    return '''
    <!doctype html><head>
    <title>Upload new File</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    </head>
    <h1 style="text-align:center">Upload new File</h1><br>
    <form style="text-align:center" method=post enctype=multipart/form-data>
    <div class="col-xs-3">
      <input type=file name=file class="form-control" id="customFile" ><br></div>
      <input type=file name=file1 class="form-control" id="customFile"><br>
      <input type=submit value=Blend class="btn btn-secondary">
    </form>
    '''


@app.route('/blend')
def blend():
    blendTwoImages()
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Pyramid_blending.jpg')
    return render_template("index.html", user_image = full_filename)




if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)