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
        image_id = form.image.data
        my_image = fetch_image(image_id)

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

        my_histogram = "my_histogram.png"

        # returns the image histogram output from the specified image
        # return render_template('classification_output.html', image_id=image_id, results=result_dict)
        return render_template("histogram_output.html", image_id=image_id)

    # otherwise, it is a get request and should return the
    # image selector
    return render_template('histogram_select.html', form=form)
