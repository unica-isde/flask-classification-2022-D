import redis
from flask import render_template, Flask, flash, request, redirect, url_for, send_from_directory
from rq import Connection, Queue
from rq.job import Job
import os
from app import app
from app.forms.upload_form import UploadForm
from ml.classification_utils import classify_image
from config import Configuration
import random
import string
from app.utils.clean_upload_utilities import delete_after_a_while
from werkzeug.utils import secure_filename

config = Configuration()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config.image_upload_extensions


def validate_filename(filename):
    filename_part = filename.rsplit('.', 1)
    current_filename = filename_part[0]
    extension = filename_part[1]
    while filename in os.listdir(config.upload_folder_path):
        filename = current_filename + random.choice(string.ascii_lowercase) + '.' + extension
    return filename


@app.route('/classifications_upload', methods=['GET', 'POST'])
def classifications_upload():
    """API for selecting a model, upload an image and running a
    classification job. Returns the output scores from the 
    model. It does the exact same thing of classification, but with an uploaded image"""
    form = UploadForm()
    if form.validate_on_submit():  # POST
        model_id = form.model.data
        filename = None
        # check if the post request has the file part (otherwise something went wrong, this should never happen)
        if 'file' not in request.files:
            form.warning = True
            form.warning_text = 'Upload error'
            return render_template('classification_select_upload.html', form=form)
        file = request.files['file']
        # If the user does not select a file, a warning is showed
        if file.filename == '':
            form.warning = True
            form.warning_text = '''You haven't uploaded any file'''
            return render_template('classification_select_upload.html', form=form)
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = validate_filename(filename)  # avoid overwriting existing files
                file.save(os.path.join(config.upload_folder_path, filename))  # then create job
            else:
                form.warning = True
                allowed_ext = str(config.image_upload_extensions)
                allowed_ext = allowed_ext.replace('[', '')
                allowed_ext = allowed_ext.replace(']', '')
                allowed_ext = allowed_ext.replace("'", "")
                form.warning_text = "Your file can't be computed. Allowed file extensions: " + allowed_ext
                return render_template('classification_select_upload.html', form=form)

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": filename,
                "uploaded": True
            })
            task = q.enqueue_job(job)

        delete_after_a_while(filename)

        # returns the image classification output from the specified model
        return render_template("classification_output_queue.html", uploaded=True, image_id=filename,
                               jobID=task.get_id())

    # image and model selector
    return render_template('classification_select_upload.html', form=form)


@app.route('/classifications_get_uploaded_<path:filename>')
def get_uploaded_image(filename):
    return send_from_directory(config.upload_folder_path, filename)
