from flask import render_template, flash
from app import app


@app.route('/')
def index():
    
    return render_template('home.html')

@app.route('/New')
def New ():
    return render_template('New.html')