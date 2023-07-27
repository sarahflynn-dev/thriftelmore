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

#add to my items
@app.route('/add/to/my/cart', methods=['POST'])
def add_item():
    if 'logged_in_id' not in session:
        return redirect('/')
    item_data = {
        'id':id
    }
    user_data= {
        'id' : session['logged_in_id']
    }
    return redirect('/success')


#my cart
@app.route('/my_cart')
def view_cart():
    if 'logged_in_id' not in session:
        return redirect('/')
    render_template('/view/cart.html')

#my sale items
@app.route('/my_items')
def my_sale_items():
    if 'logged_in_id' not in session:
        return redirect('/')
    data = {
        'id': session['logged_in_id']
    }
    return render_template('dashboard.html', my_items=items.Items.get_all_items(),one_user=register.User.get_by_id(data))

#post new sale items
@app.route('/new/item')
def new_item():
    if 'logged_in_id' not in session:
        return redirect ('/')
    return render_template('/new_item.html')

@app.route('/post/new/item', methods=['POST'])
def post_new_item():
    if 'logged_in_id' not in session:
        return redirect ('/')
    items.Items.save_item(request.form)
    return redirect('/my_items')

#edit sale items
@app.route('/edit/items')
def edit_item():
    if 'logged_in_id' not in session:
        return redirect ('/')
    return render_template('edit/items.html')

@app.route('/update/items', methods=['POST'])
def update_item():
    if 'logged_in_id' not in session:
        return redirect ('/')
    items.Item.update_item(request.form)
    return redirect ('/my_items')

#delete sale item
@app.route('/delete/item', methods=['POST'])
def delete_item():
    items.Item.delete_item(request.form)
    return redirect ('my_items')

