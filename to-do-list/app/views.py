from flask import render_template, flash, request, redirect, url_for
from app import app, db
from .forms import NewAssessment
from datetime import datetime
from app.models import Assessment
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import HiddenField


# Route for the index page that displays all assessments
@app.route('/')
def index():
    # Retrieve the first new and completed assessments
    new_assessment = Assessment.query.filter_by(Complete=False).first()
    old_assessment = Assessment.query.filter_by(Complete=True).first()

    # Set messages if no assessments are found
    message1 = None
    if not new_assessment:
        message1 = "No new assessment available"

    message2 = None
    if not old_assessment:
        message2 = "No completed assessment"

    # Retrieve all assessments for display
    rows = Assessment.query.all()

    # Render the home page with assessment data
    return render_template(
        'home.html',
        rows=rows,
        message1=message1,
        message2=message2,
        title='All Assessments'
    )


# Route for displaying current assessments
@app.route('/current', methods=['GET', 'POST'])
def current():
    # Retrieve all current assessments
    rows = Assessment.query.all()

    # Set message if no assessments are in progress
    message = None
    if not rows:
        message = "No assessments in progress"

    # Render the current assessments page
    return render_template(
        'current.html',
        rows=rows,
        message=message,
        title='Current Assessments'
    )


# Route for creating a new assessment
@app.route('/New', methods=['GET', 'POST'])
def New():
    form = NewAssessment(request.form)  # Instantiate the form
    today = datetime.now().date()  # Get today's date

    # Validate form submission
    if form.validate_on_submit():
        print("Form validated successfully!")
    else:
        print("Form validation failed:", form.errors)

    # Handle POST request for form submission
    if request.method == 'POST' and form.validate_on_submit():
        code = form.Code.data
        title = form.Title.data
        description = form.Description.data
        date = form.Date.data

        # Validate that the date is in the future
        if date <= today:
            flash('Error: The date must be in the future', 'error')
            return render_template(
                'New.html',
                title='New Assessment',
                form=form
            )

        # Check if an assessment with the same code and title already exists
        existing_assessment = Assessment.query.filter_by(
            Code=code,
            Title=title
        ).first()

        if existing_assessment:
            flash(
                'Error: An Assessment with this code and title already exists',
                'error')

            return render_template(
                'New.html',
                title='New Assessment',
                form=form
            )

        # Create a new assessment and save it to the database
        new_assessment = Assessment(
            Code=code, Title=title, Date=date, Description=description
        )

        db.session.add(new_assessment)
        db.session.commit()
        flash('Assessment added successfully!', 'success')
        return redirect(url_for('index'))

    # Render the new assessment form
    return render_template('New.html', title='New Assessment', form=form)


# Route for editing an existing assessment
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Retrieve the assessment by ID
    assessment = Assessment.query.get_or_404(id)
    # Pre-fill the form with existing data
    form = NewAssessment(obj=assessment)
    today = datetime.now().date()

    # Handle POST request for form submission
    if request.method == 'POST' and form.validate_on_submit():

        date = form.Date.data
        code = form.Code.data
        title = form.Title.data

        if date <= today:
            flash('Error: The date must be in the future', 'error')
            return render_template(
                'edit.html',
                title='Edit Assessment',
                form=form
            )

        # Check for existing assessments with the same code and title
        existing_assessment = Assessment.query.filter_by(
            Code=code,
            Title=title).filter(
            Assessment.id != id).first()

        if existing_assessment:
            flash(
                'Error: An Assessment with this code and title already exists',
                'error')

            return render_template(
                'edit.html',
                title='Edit Assessment',
                form=form
            )

        # Populate the assessment object with form data
        form.populate_obj(assessment)
        db.session.commit()  # Commit changes to the database
        flash('Assessment updated successfully!', 'success')
        return redirect(url_for('index'))

    # Render the edit assessment form
    return render_template('edit.html', assessment=assessment, form=form)


# Route for deleting an assessment
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # Retrieve the assessment by ID
    assessment = Assessment.query.filter_by(id=id).first()

    if assessment:
        # Delete the assessment from the database
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted sucessfully!', 'success')
        return redirect(url_for('index'))

    # If the assessment is not found, render current assessments page
    return render_template('current.html, assessment=assessment')


# Route for marking an assessment as complete
@app.route('/complete/<int:id>', methods=['GET', 'POST'])
def complete(id):
    # Retrieve the assessment by ID
    assessment = Assessment.query.get_or_404(id)
    assessment.Complete = True  # Update the completion status
    db.session.commit()  # Commit changes to the database
    flash("Assessment marked as complete!", 'success')
    return redirect(url_for('index'))


# Route for marking an assessment as unfinished
@app.route('/unfinish/<int:id>', methods=['GET', 'POST'])
def unfinish(id):
    # Retrieve the assessment by ID
    assessment = Assessment.query.get_or_404(id)
    assessment.Complete = False  # Update the completion status
    db.session.commit()  # Commit changes to the database
    flash("Assessment marked as un-finished!", 'success')
    return redirect(url_for('index'))
