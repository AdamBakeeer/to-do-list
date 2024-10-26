from flask import render_template, flash, request, redirect, url_for
from app import app, db
from .forms import NewAssessment
from datetime import datetime
from app.models import Assessment
from sqlalchemy.exc import IntegrityError


@app.route('/')
def index():
    
    return render_template('home.html')

@app.route('/New', methods=['GET', 'POST'])
def New ():
    form = NewAssessment()

    if form.validate_on_submit():
        code = form.Code.data
        title = form.Title.data
        description = form.Description.data
        date = form.Date.data
        
        new_assessment = Assessment(
            Code=code, Title=title, Date=datetime.strptime(date, '%Y-%m-%d'), Description=description
        )

        try:
            db.session.add(new_assessment)
            db.session.commit()
            flash('Assessment added successfully!', 'success')
            return redirect(url_for('index'))  
        except IntegrityError:
            db.session.rollback() 
            flash('Assessment with this code already exists. Please use a different code.', 'error')
    return render_template('New.html', title='New', form=form)