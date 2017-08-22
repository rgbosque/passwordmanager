import os
import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap

from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from forms import LoginForm, RegistrationForm, AccountForm
from models import db, User, Account

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'pm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'thisissecret'

Bootstrap(app)
# db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                print form.remember.data
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1> Invalid username or password </h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user has been created! </h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    # list_of_accounts = Account.query.order_by(Account.id.desc()).all()
    list_of_accounts = Account.query.order_by(Account.used_for).all()

    return render_template('dashboard.html',
                           name=current_user.username,
                           accounts=list_of_accounts)


@app.route('/dashboard/action')
@login_required
def dashboard_reveal():

    request_id = request.args.get('request_id')

    if request.args.get('action') == 'Reveal':
        return "<h1>" + request_id + "</h1>"
    elif request.args.get('action') == 'Edit':
        return "<h1> Edit Mode " + request_id + "</h1>"
    elif request.args.get('action') == 'Delete':
        return "<h1> Delete Mode " + request_id + "</h1>"


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()

    if form.validate_on_submit():
        today = datetime.datetime.today()

        new_account = Account(used_for=form.website.data,
                              username_used=form.username_used.data,
                              password_used=form.password_used.data,
                              date_created=today,
                              date_updated=today)

        db.session.add(new_account)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('account.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
