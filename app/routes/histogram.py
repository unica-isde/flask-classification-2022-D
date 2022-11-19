from flask import render_template

from app import app
from app.forms.histogram_form import HistogramForm
from config import Configuration

config = Configuration()


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    """API for selecting an image.
    Returns the output histogram from the image.
    """
    form = HistogramForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.dat


        # returns the image histogram output from the specified image
        # return render_template('classification_output.html', image_id=image_id, results=result_dict)
        return render_template("histogram_output.html", image_id=image_id)

    # otherwise, it is a get request and should return the
    # image selector
    return render_template('histogram_select.html', form=form)
