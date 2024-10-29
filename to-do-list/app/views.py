from flask import render_template, flash, request, redirect, url_for
from app import app, db
from .forms import NewAssessment
from datetime import datetime
from app.models import Assessment
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import HiddenField


@app.route('/')
def index():
    new_assessment = Assessment.query.filter_by(Complete=False).first()
    old_assessment = Assessment.query.filter_by(Complete=True).first()

    message1 = None
    if not new_assessment:
        message1 = "No new assessment available"

    message2 = None
    if not old_assessment:
        message2 = "No completed assessment"

    
    rows = Assessment.query.all()

    return render_template('home.html', rows=rows, message1=message1, message2=message2)

@app.route('/current', methods=['GET', 'POST'])
def current():
    rows = Assessment.query.all()

    
    return render_template('current.html', rows=rows)



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

        
        existing_assessment = Assessment.query.filter_by(Code=code, Title=title).first()
        if existing_assessment:
            flash('Error: An Assessment with this code and title already exists', 'error')
            return render_template('New.html', title='New', form=form)
        
        new_assessment = Assessment(
            Code=code, Title=title, Date=date, Description=description
        )

        db.session.add(new_assessment)
        db.session.commit()
        flash('Assessment added successfully!', 'success')
        return redirect(url_for('index'))
  
        
    return render_template('New.html', title='New', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    assessment = Assessment.query.get_or_404(id)
    form = NewAssessment(obj=assessment)
    today = datetime.now().date()

    if request.method == 'POST' and form.validate_on_submit():
        
        date = form.Date.data
        code = form.Code.data 
        title = form.Title.data

        if date <= today:
            flash('Error: The date must be in the future', 'error')
            return render_template('New.html', title='New', form=form)
        
        existing_assessment = Assessment.query.filter_by(Code=code, Title=title).first()
        if existing_assessment:
            flash('Error: An Assessment with this code and title already exists', 'error')
            return render_template('New.html', title='New', form=form)
        

        form.populate_obj(assessment)
        db.session.commit()
        flash('Assessment updated successfully!', 'success')  
        return redirect(url_for('index'))
        
    return render_template('edit.html', assessment=assessment, form=form)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    assessment = Assessment.query.filter_by(id=id).first()

    if assessment:
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted sucessfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('current.html, assessment=assessment')

@app.route('/complete/<int:id>', methods=['GET', 'POST'])
def complete(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.Complete = True
    db.session.commit()
    flash("Assessment marked as complete!", 'success')
    return redirect(url_for('index'))

@app.route('/unfinish/<int:id>', methods=['GET', 'POST'])
def unfinish(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.Complete = False
    db.session.commit()
    flash("Assessment marked as un-finished!", 'success')
    return redirect(url_for('index'))


