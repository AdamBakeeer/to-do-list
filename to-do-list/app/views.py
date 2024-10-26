from flask import render_template, flash
from app import app
from .forms import NewAssessment


@app.route('/')
def index():
    
    return render_template('home.html')

@app.route('/New', methods=['GET', 'POST'])
def New ():
    form = NewAssessment()
    return render_template('New.html', title='New', form=form)