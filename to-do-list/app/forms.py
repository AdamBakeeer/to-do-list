from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import DateField
from wtforms.validators import DataRequired

class NewAssessment(FlaskForm):
    Code = StringField('Module Code', validators=[DataRequired()])
    Title= StringField('Assessmen Title', validators=[DataRequired()])
    Date = DateField('Date', validators=[DataRequired()])
    Description = TextAreaField('Description', validators=[DataRequired()])