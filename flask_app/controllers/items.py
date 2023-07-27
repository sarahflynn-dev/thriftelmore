from flask_app import app
from flask import render_template, redirect, request, session, flash

# from flask_app.models.user import User
# from flask_app.models.review import Review
# from flask_app.models.item import Items
from flask_app.models import register, reviews, items
from flask_app.controllers import users
from werkzeug.utils import secure_filename
import os
import re


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# add to my items


@app.route('/add/to/my/cart', methods=['POST'])
def add_item():
    if 'logged_in_id' not in session:
        return redirect('/')
    item_data = {
        'id': id
    }
    user_data = {
        'id': session['logged_in_id']
    }
    return redirect('/success')


# my cart
@app.route('/my_cart')
def view_cart():
    if 'logged_in_id' not in session:
        return redirect('/')
    render_template('/view/cart.html')

# my sale items


@app.route('/my_items')
def my_sale_items():
    # check if 'logged_in_id' is in the session
    if 'logged_in_id' not in session:
        print("No logged_in_id in session")  # Debug print
        return redirect('/')
    print("Logged in id:", session['logged_in_id'])  # Debug print

    data = {
        'id': session['logged_in_id']
    }

    # Fetch items and user from the database
    my_items = items.Items.get_all_items_by_user(data)
    one_user = register.User.get_by_id(data)

    # Debug prints
    print("My items:", my_items)
    print("One user:", one_user)

    return render_template('dashboard.html', my_items=my_items, one_user=one_user)


# post new sale items


@app.route('/new/item')
def new_item():
    if 'logged_in_id' not in session:
        return redirect('/')
    return render_template('/new_item.html')


@app.route('/post/new/item', methods=['POST'])
def post_new_item():
    if 'logged_in_id' not in session:
        return redirect('/')

    # check if the post request has the file part
    if 'item_picture' not in request.files:
        flash('No file part')
        return redirect('/new/item')

    file = request.files['item_picture']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect('/new/item')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        form_data = request.form.to_dict()
        form_data['user_id'] = session['logged_in_id']
        # Save the filename instead of the file
        form_data['item_picture'] = filename

        if not items.Items.validate_item(form_data):
            return redirect('/new/item')

        items.Items.save_item(form_data)
        return redirect('/my_items')


# edit sale items
@app.route('/edit/items')
def edit_item():
    if 'logged_in_id' not in session:
        return redirect('/')
    return render_template('edit/items.html')


@app.route('/update/items', methods=['POST'])
def update_item():
    if 'logged_in_id' not in session:
        return redirect('/')
    items.Items.update_item(request.form)
    return redirect('/my_items')

# delete sale item


@app.route('/delete/item', methods=['POST'])
def delete_item():
    items.Items.delete_item(request.form)
    return redirect('my_items')
