import os
from pathlib import Path
from uuid import uuid4
from sqlalchemy import update
from sqlalchemy.exc import DataError, IntegrityError
from flask import request, render_template, redirect, send_from_directory, session, flash, make_response, url_for, g
from app import app, db, ALLOWED_EXTENSIONS
from .models import Posts, User
from .errors_handlers import page_not_found
from .utils import allowed_file

users = {}
UPLOAD_AVATARS_FOLDER = "avatars"

BASE_DIR = Path(__file__).resolve(strict=True).parent

## ALL USERS PAGE
@app.route('/users', methods=['GET'])
# @login_required
def all_user_list():
    if 'username' in session:
        try:
            # users = User.query.all()
            users = User.query.with_entities(User.id, User.username, User.avatar, User.about)
            user = User.query.filter_by(username=session.get('username')).first()
            db.session.commit()
        except Exception as err:
            app.logger.error(err)
            return page_not_found()
        else:
            data = {
                'users': users,
                'user': user
            }
            app.logger.info(f'users list requ - {data}')
            return render_template('users/list.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/user/<username>')
def show_user_profile(username):
    try:
        user = User.query.filter_by(username=username).first_or_404()
        posts = Posts.query.filter_by(owner=username).all()
        db.session.commit()
        app.logger.error(user)
    except Exception as err:
        app.logger.error(err)
        # username = ''
        return page_not_found()

    user.__dict__.pop('_password')
    user.__dict__.pop('_sa_instance_state', '')
    data = {
        'username': user.__dict__.get('username'),
        'user': user.__dict__,
        'posts': posts
    }
    app.logger.info(user.__dict__)
    return render_template('userpage.html', data=data)



@app.route('/edit', methods=['POST'])
def edit_profile():

    allowed_fields = ["avatar", "about",
                    "email",
                    "first_name","last_name",
                    "live_country","live_city",
                    ]

    # file = request.files['avatar']
    # if file.filename == '':
    #     flash('No selected file')
    #     return redirect(request.url)
    # if file and allowed_file(file.filename):
    #     # filename = secure_filename(file.filename)
    #     ext = file.filename.rsplit('.', 1)[1].lower()
    #     new_name = uuid4()
    #     file.filename = f"{new_name}.{ext}"
    #     file.save(os.path.join(os.path.join(BASE_DIR, 'static', UPLOAD_AVATARS_FOLDER), file.filename))

    if  'username' in session:
        # print(list(request.form))
        # app.logger.info('edit', request.form)
        user_data = {
            "avatar": request.form.get('avatar') ,
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "email": request.form.get('email'),
            "live_country": request.form.get('live_country'),
            "live_city": request.form.get('live_city'),
            "about": request.form.get('about'),
        }
        username = session.get('username')
        app.logger.info(f" user_data {user_data}")
        for key, value in user_data.items():
        #     if key == 'edit':
        #         continue
            if key == 'avatar' and value != "":
                file = request.files.get('avatar')
                if file and allowed_file(file.filename):
                    # filename = secure_filename(file.filename)
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    new_name = uuid4()
                    file.filename = f"{new_name}.{ext}"
                    file.save(os.path.join(os.path.join(BASE_DIR, 'static', UPLOAD_AVATARS_FOLDER), file.filename))
                    app.logger.info(f'{key} {file.filename} new file')

                    rows = User.query.filter_by(username=username).update({key: str(file.filename)})
                    db.session.commit()

            if key == 'email' and value != "":
                try:
                    rows = User.query.filter_by(username=username).update({key: value})
                    db.session.commit()
                except IntegrityError as err:
                    error = 'E-mail занят, укажите другой'
                    flash(error)
                    # return render_template('register.html', error=error)
                    return make_response(redirect(url_for('show_user_profile', username=session.get('username'), error=error)))

            if value != "" and key != 'avatar':
                app.logger.info(f'{key, value} not pustoe')
                try:
                    # db.update(User).where(User.username == session.get('username')).values(key=value)
                    rows = User.query.filter_by(username=username).update({key: value})
                    db.session.commit()
                # break
                except DataError:
                    flash('error')
                    resp = make_response(redirect(url_for('show_user_profile', username=session.get('username'))))
                    print('OSHIBKA')
                    return resp
                # else:
                #     return redirect(url_for('show_user_profile', username=session.get('username')))
        return redirect(url_for('show_user_profile', username=session.get('username')))
    else:
        return redirect(url_for("auth"))


@app.route('/avatars/<filename>')
def uploaded_avatars(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static', UPLOAD_AVATARS_FOLDER),
                               filename)



