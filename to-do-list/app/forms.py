from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms import DateField, BooleanField, HiddenField
from wtforms.validators import DataRequired


class NewAssessment(FlaskForm):
    Code = StringField('Module Code', validators=[DataRequired()])
    Title = StringField('Assessment Title', validators=[DataRequired()])
    Date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    Description = TextAreaField('Description', validators=[DataRequired()])
    Complete = BooleanField('Complete')
    submit = SubmitField('Add Assessment')
