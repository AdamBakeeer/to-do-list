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
    
    form = NewAssessment(request.form)
    today = datetime.now().date()

    if form.validate_on_submit():
        print("Form validated successfully!")
    else:
        print("Form validation failed:", form.errors)
        

    if request.method == 'POST' and form.validate_on_submit():
        code = form.Code.data
        title = form.Title.data
        description = form.Description.data
        date = form.Date.data

        if date <= today:
            flash('Error: The date must be in the future', 'error')
            return render_template('New.html', title='New', form=form)

        
        existing_assessment = Assessment.query.filter_by(Code=code).first()
        if existing_assessment:
            flash('Error: The code already exists. Please use a unique code.', 'error')
            return render_template('New.html', title='New', form=form)

        
        new_assessment = Assessment(
            Code=code, Title=title, Date=date, Description=description
        )

        db.session.add(new_assessment)
        db.session.commit()
        flash('Assessment added successfully!', 'success')
        return redirect(url_for('index'))
  
        
    return render_template('New.html', title='New', form=form)