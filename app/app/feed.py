from flask import session
from .models import Posts, User
from app import app, db
from sqlalchemy import  desc  # or_, and_, asc, desc, inspect, update, desc
from flask import request, render_template, redirect, send_from_directory, session, url_for


@app.route('/feed', methods=['GET'])
def show_feed():
    if 'username' in session:
        posts = Posts.query.order_by(desc(Posts.created_at)).all()
        db.session.commit()
        users = User.query.all()
        user = User.query.filter_by(username=session.get('username')).first()
        db.session.commit()
        data = {
                'users': users,
                'user': user
            }
        return render_template('feed/feed-main.html', posts=posts, data=data)
    else:
        return redirect(url_for("auth"))

###