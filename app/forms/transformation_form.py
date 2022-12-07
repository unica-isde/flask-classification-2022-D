from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


class TransformationForm(FlaskForm):
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    color = DecimalField('color', validators=[DataRequired()])
    brightness = DecimalField('brightness', validators=[DataRequired()])
    contrast = DecimalField('contrast', validators=[DataRequired()])
    sharpness = DecimalField('sharpness', validators=[DataRequired()])
    submit = SubmitField('Submit')
