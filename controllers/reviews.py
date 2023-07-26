from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import register, reviews, items

#review page
@app.route('/review/item')
def review():
    if 'logged_in_id' not in session:
        return redirect ('/')
    return render_template('/review/item.html')

#leave review
@app.route('/leave/review', methods=['POST'])
def leave_review():
    if 'logged_in_id' not in session:
        return redirect ('/')
    reviews.Review.save(request.form)
    return redirect('/review/item')