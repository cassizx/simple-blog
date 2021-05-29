from app import app, db
from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, g, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DataError, IntegrityError
from .models import User
from .utils import ts, confirm_token, generate_confirmation_token
from .email_sender import send_email
from flask_bcrypt import generate_password_hash, check_password_hash


salt = app.config['SECURITY_PASSWORD_SALT']


@app.route('/account/create', methods=["GET", "POST"])
def create_account():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email = request.form.get('email')

        email_exists = db.session.query(
            db.session.query(User).filter_by(email=email).exists()
        ).scalar()
        if email_exists:
            error = 'Пользователь с таким email уже зарегистрирован'
            flash(error)
            return render_template('register.html', error=error)

        if password == password2 and password is not None:
            try:
                # is_ = User.query.filter_by(email=email).first().exists()
                # print(exists)
            #     if exists:
            #         app.logger.info(f" exists {exists}")
            # except Exception as err:
            #     print(err)
                user = User(
                    username = username,
                    password = password,
                    email=email
                )
                db.session.add(user)
                db.session.commit()
            except IntegrityError as err:
                # error = f'{err._message()} занят, выберете другой'
                error = 'E-mail/Username занят, укажите другой'
                flash(error)
                return render_template('register.html', error=error)
        else:
            error = 'Пароли не совпадают'
            flash(error)
            return render_template('register.html', error=error)

        token = generate_confirmation_token(email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('confirm.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(email, subject, html)


        error = 'Регистрация успешна'
        flash(error)
        return make_response(redirect(url_for('login', error=error)))


    return render_template("register.html")


# AUTH

@app.route('/', methods=['GET'])
def auth():
    error = None
    if 'username' in session:
        return redirect(url_for('show_user_profile', username=session.get('username')))
    else:
        return render_template('login.html', error=error)



def valid_login(username, password):
    if username and username != '' and password:
        try:
            user = User.query.filter_by(username=username).first() #.first_or_404()
            app.logger.debug(f'{user} -trying logging')
        except Exception as err:
            app.logger.debug(f'trying logging, error {err }')
            return False
        else:
            if user and user.is_correct_password(password):
                app.logger.debug(f'{user} is loggined')
                return True

    app.logger.debug(f'{username} - not  loggined')
    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # return str(request.__dict__)
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):

            session['username'] = request.form['username']

            resp = make_response(redirect(url_for('show_user_profile', username=request.form['username'])))
            resp.set_cookie('username', request.form['username'])
            return resp
        else:

            error = 'Invalid username or password'
            flash(error)
            return render_template('login.html', error=error)

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return redirect('/')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    try:
        session.pop('username', None)
        # request.
        resp = make_response(redirect(url_for('login')))
        resp.set_cookie('username', " ", max_age=0)
        return resp
    except Exception as err:
        app.logger.error(err)
        # return redirect('/')


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    user = User.query.filter_by(email=email).first_or_404()

    if user.is_email_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.is_email_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('login'))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'GET':
        return render_template('reset.html')

    if request.method == 'POST' and request.form.get('email') != '':
        return reset_password(request.form.get('email'))
    else:
        return render_template('404.html'), 404


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    if request.method == 'GET':
        return render_template('reset_with_token.html', token=token)

    try:
        return reset_with_token_(token)
    except Exception as err:
        app.logger.error(err)
        abort(404)


def reset_password(email):
    app.logger.error(f'{email} request for reset')
    user = User.query.filter_by(email=email).first()
    #     if not request.json or not 'firstName' or not 'lastName' in request.json:

    if user:
        subject = "Запрос сброса пароля"
        token = ts.dumps(email, salt=salt)
        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url)

        send_email(user.email, subject, html)
        print(recover_url)
        flash('Письмо для сброса пароля отправлено')
        return redirect(url_for('login'))
    else:
        flash(f'Пользователь с email {email} не найден. Проверьте корректность email.')
        return render_template('reset.html')


def reset_with_token_(token):

    email = ts.loads(token, salt=salt, max_age=86400)
    app.logger.error(email)
    # TODO Добавить обработку случая когда истёк срок
    # действия токена Signature age 512049 > 86400 seconds
    user = User.query.filter_by(email=email).first_or_404()
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if password1 == password2:
        user.password = generate_password_hash(password1).decode('utf-8')
        print('user.password', user.password)
        db.session.add(user)
        db.session.commit()
        flash('Пароль успешно изменён.')
        return redirect(url_for('login'))

    return redirect(url_for('create_account'))