from flask import render_template
from PIL import ImageEnhance

from app import app
from app.forms.transformation_form import TransformationForm
from config import Configuration
from ml.classification_utils import fetch_image

config = Configuration()


@app.route('/transformations', methods=['GET', 'POST'])
def transformations():
    """API for selecting an image and a transformation style and running a
    transformation job. Returns the output image from the
    transformation."""
    form = TransformationForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        color = form.color.data
        brightness = form.brightness.data
        contrast = form.contrast.data
        sharpness = form.sharpness.data

        my_custom_img = fetch_image(image_id)
        im_out = ImageEnhance.Color(my_custom_img).enhance(color)
        # im_out = ImageEnhance.Brightness(my_custom_img).enhance(brightness)
        # im_out = ImageEnhance.Contrast(my_custom_img).enhance(contrast)
        # im_out = ImageEnhance.Sharpness(my_custom_img).enhance(sharpness)
        im_out.save(config.image_folder_path + '/' + "custom_" + image_id)

        # returns the image transformation output from the specified transformation
        return render_template("transformation_output.html", image_id=image_id, custom_image="custom_" + image_id,
                               color=color,
                               brightness=brightness,
                               contrast=contrast, sharpness=sharpness)

    # otherwise, it is a get request and should return the
    # image and transformation selector
    return render_template("transformation_select.html", form=form)
