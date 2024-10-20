from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import DateField
from wtforms.validators import DataRequired

class CalculatorForm(FlaskForm):
    Title= StringField('Title', validators=[DataRequired()])
    Code = StringField('Code', validators=[DataRequired()])
    Date = DateField('Date', validators=[DataRequired()])
    Description = StringField('Description', validators=[DataRequired()])