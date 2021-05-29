import os
from uuid import uuid4
from sqlalchemy.exc import DataError, IntegrityError
from .models import Posts
from app import app, db, ALLOWED_EXTENSIONS
from sqlalchemy import  desc  # or_, and_, asc, desc, inspect, update, desc
from flask import request, render_template, redirect, send_from_directory, session, flash, make_response, url_for
from .utils import allowed_file



@app.route('/post/create', methods=['POST'])
def create_post():
    # if 'file' not in request.files:
    #     flash('No file part')
    #     return redirect(request.url)

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        ext = file.filename.rsplit('.', 1)[1].lower()
        new_name = uuid4()
        file.filename = f"{new_name}.{ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
        app.logger.info(file)
        try:
            new_posts = Posts(
                owner = session['username'],
                body = request.form['body'],
                image_url = file.filename
            )
            db.session.add(new_posts)
            db.session.commit()
        except DataError:
            flash('error')
            resp = make_response(redirect(url_for('show_user_profile', username=session.get('username'))))
            return resp
        else:
            return redirect(url_for("auth"))

    flash(f'Недопустимое расширение файла, выберите файл с расширением { ALLOWED_EXTENSIONS }')
    resp = make_response(redirect(url_for('show_user_profile', username=session.get('username'))))
    return resp
    # show_user_profile(session['username'])
### END POSTS