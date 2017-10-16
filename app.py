import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

from forms import LoginForm, RegistrationForm, AccountForm, AccountFormEdit
from models import db, User, Account, migrate

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

# INITIALIZATION
Bootstrap(app)
db.app = app
db.init_app(app)
migrate.init_app(app)
mail = Mail(app)

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
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard', page_num=1))

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


@app.route('/dashboard/<int:page_num>')
@login_required
def dashboard(page_num):
    # list_of_accounts = Account.query.order_by(Account.id.desc()).all()
    # list_of_accounts = Account.query.order_by(Account.url).all()

    # list_of_accounts = Account.query.filter_by(user_id=current_user.id).all()
    list_of_accounts = Account.query.paginate(per_page=5, page=page_num, error_out=True)

    return render_template('dashboard.html',
                           name=current_user.username,
                           accounts=list_of_accounts)


@app.route('/dashboard/action')
@login_required
def dashboard_reveal():

    request_id = request.args.get('request_id')

    if request.args.get('action') == 'Reveal':
        pass_reveal = Account.query.filter_by(id=request_id).first()

        msg = Message("PM-APP-Reveal", sender="rgbosque@gmail.com",
                      recipients=['rodelbosque@prestige-alliance.com'])
        msg.body = "INFO: " + str(pass_reveal.password_used)
        mail.send(msg)
        return "<h1>Your password info was sent to your email!</h1>"
    elif request.args.get('action') == 'Edit':
        form = AccountFormEdit()
        account = Account.query.filter_by(id=request_id).first()
        id = account.id
        form.url.data = account.url
        form.username_used.data = account.username_used
        form.password_used.data = account.password_used

        return render_template('accountedit.html', form=form, id=id)
    elif request.args.get('action') == 'Delete':
        account = Account.query.filter_by(id=request_id).first()

        db.session.delete(account)
        db.session.commit()

        return redirect(url_for('dashboard', page_num=1))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()

    if form.validate_on_submit():
        today = datetime.datetime.today()

        new_account = Account(url=form.url.data,
                              username_used=form.username_used.data,
                              password_used=form.password_used.data,
                              date_created=today,
                              date_updated=today,
                              user_id=current_user.id)

        db.session.add(new_account)
        db.session.commit()

        return redirect(url_for('dashboard', page_num=1))

    return render_template('account.html', form=form)


@app.route('/account/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def account_edit(post_id):
    form = AccountFormEdit()

    if form.validate_on_submit():
        today = datetime.datetime.today()
        account = Account.query.filter_by(id=post_id).first()

        account.url = form.url.data
        account.username_used = form.username_used.data
        account.password_used = form.password_used.data
        account.date_updated = today

        db.session.commit()

        return redirect(url_for('dashboard', page_num=1))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=5000)
