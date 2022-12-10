from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

from config import Configuration

conf = Configuration()


class UploadForm(FlaskForm):
    model = SelectField('model', choices=conf.models, validators=[DataRequired()])
    # ↑ ↑ ↑ allow the user to choose btw diff classification models ↑ ↑ ↑ #
    warning = False  # used by the template "classification select upload" to show to the user an err msg if necessary
    warning_text = ""  # used by the template "classification select upload" to show to the user an err msg if necessary
    submit = SubmitField('Submit')  # see flask documentation about forms
