from flask import render_template

from app import app
from app.forms.histogram_form import HistogramForm
from config import Configuration
from ml.classification_utils import fetch_image

import matplotlib.pyplot as plt
import numpy as np
import imageio.v3 as iio

config = Configuration()


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    """API for selecting an image.
    Returns the output histogram from the image.
    """

    form = HistogramForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data

        im = iio.imread(config.image_folder_path + '/' + image_id)
        # calculate mean value from RGB channels and flatten to 1D array
        vals = im.mean(axis=2).flatten()
        # calculate histogram
        counts, bins = np.histogram(vals, range(257))
        # plot histogram with 255 bins
        plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
        plt.title("Image Histogram")
        plt.xlabel("bin value")
        plt.ylabel("pixel count")
        plt.xlim([-0.5, 255.5])
        plt.savefig(config.image_folder_path + '/' + "my_histogram.png")

        # returns the image histogram output from the specified image
        return render_template("histogram_output.html", image_id=image_id, histogram="my_histogram.png")

    # otherwise, it is a get request and should return the
    # image selector
    return render_template('histogram_select.html', form=form)
