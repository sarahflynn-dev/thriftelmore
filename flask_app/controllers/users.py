from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models import register, reviews, items

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


# if user is logged in, go to dashboard
@app.route('/login')
def login():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('login.html')


# login user
@app.route('/login/user', methods=['POST'])
def login_user():
    one_user = register.User.get_by_email(request.form)
    if not one_user:
        flash('Password or username do not match our records', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(one_user.password, request.form['password']):
        flash('Password or username do not match our records', 'login')
        return redirect('/')
    session['logged_in_id'] = one_user.id
    return redirect('/success')

# create user


@app.route('/register')
def register_user():
    return render_template('/register.html')


@app.route('/create/user', methods=['POST'])
def validate_register():
    if not register.User.validate_user(request.form):
        return redirect('/login')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'date_of_birth': request.form['date_of_birth'],
        'username': request.form['username'],
        'password': hashed_pw,
    }
    one_user = register.User.save(data)
    session['logged_in_id'] = one_user
    # register.User.save(data) <-----
    return redirect('/success')


@app.route('/success')
def login_redirect():
    if 'logged_in_id' not in session:
        return redirect('/')
    data = {
        'id': session['logged_in_id']
    }
    print(data)
    return render_template('dashboard.html', all_posts=items.Items.get_all_items(), one_user=register.User.get_by_id(data))

# payment info


@app.route('/payment')
def payment():
    if 'logged_in_id' not in session:
        return redirect('/')
    return render_template('payment_info.html')

# logout


@app.route('/logout/user')
def logout():
    session.clear()
    return redirect('/')
