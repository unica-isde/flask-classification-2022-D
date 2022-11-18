import redis
from flask import render_template, Flask, flash, request, redirect, url_for
from rq import Connection, Queue
from rq.job import Job

import os

from app import app
from app.forms.upload_form import UploadForm
from ml.classification_utils import classify_image
from config import Configuration

from werkzeug.utils import secure_filename

config = Configuration()

appl = Flask(__name__)
appl.config['UPLOAD_FOLDER'] = config.upload_folder_path


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.image_upload_extensions


@app.route('/classifications_upload', methods=['GET', 'POST'])
def classifications_upload():
    """API for selecting a model and upload an image and running a
    classification job. Returns the output scores from the 
    model."""
    form = UploadForm()
    if form.validate_on_submit():  # POST
        model_id = form.model.data
        filename = None
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            form.warning = True
            # return redirect(request.url)
            return render_template('classification_select_upload.html', form=form)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            form.warning = True
            return redirect(request.url)
            # return render_template('classification_select_upload.html', form=form)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": filename
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        # return render_template("classification_output_queue.html", image_id=None, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_select_upload.html', form=form)
