from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, asc, desc, inspect, update, desc
from app import app, socketio
from app import app, db
from .models import User, Messages, Direct_Messages
from flask import request, render_template, redirect, send_from_directory, session, url_for


# from flask_socketio import SocketIO, join_room, leave_room

users = {}

### CHAT
## https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d
@app.route('/chat/', methods=['GET'])
def get_chat_page():
    error = None
    if 'username' in session:
        message_history = Messages.query.all()
        db.session.commit()
        users = User.query.all()
        # user = User.query.with_entities(User.id, User.username, User.avatar)
        user = User.query.filter_by(username=session.get('username'))
        db.session.commit()
        data = {
                'users': users,
                'user': user
            }
        return render_template('chat/index.html', message_history=message_history, data=data)
    else:
        return redirect(url_for('login'))


@app.route('/chat/<username>', methods=['GET'])
def direct_message(username):
    error = None
    if 'username' in session:
        from_to = Direct_Messages.query.filter(and_(Direct_Messages.sender==session['username'], Direct_Messages.recipient==username))
        to_from = Direct_Messages.query.filter(and_(Direct_Messages.sender==username, Direct_Messages.recipient==session['username']))
        #.order_by(asc(Direct_Messages.sending_time))
        #.order_by(desc(Direct_Messages.sending_time))
        #from_to = Direct_Messages.query.filter_by(sender=session['username']) #, recipient=username)
        db.session.commit()

        message_history_ = []
        message_history_.extend(from_to)
        message_history_.extend(to_from)
        # users = User.query.all()
        users = User.query.with_entities(User.id, User.username, User.avatar)
        user = User.query.filter_by(username=session.get('username')).first()

        db.session.commit()
        data = {
                'users': users,
                'user': user
            }
        app.logger.info(f'message_history - { message_history_ }, session["username"]{ session["username"]}')

        return render_template('chat/direct.html', message_history=message_history_, data=data)
    else:
        return redirect(url_for('login'))

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# @socketio.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + ' has entered the room.', to=room)

# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', to=room)


@socketio.on('username')
def receive_username(username):
    users[username] = request.sid

@socketio.on('direct message') #, namespace='/direct_message'
def handle_direct_message(json):
    app.logger.debug('received my event: ' + str(json))
    if json.get('user_name', None):
        sender_ = json.get('user_name')
        recipient_=json.get('to_user')
        message = Direct_Messages(
                        sender=sender_,
                        recipient=recipient_,
                        text=json.get('message'))
        db.session.add(message)
        db.session.commit()
        print('recipient_', recipient_)
        recipient_session_id = users[sender_]
        print('recipient_session_id', recipient_session_id)
        print('users', users)
        json_ = {
            'sender': sender_,
            'text':json.get('message')
        }
        socketio.emit('direct message response', json_, room=users[recipient_])


def messageReceived():
    app.logger.debug('message was received!!!')


@socketio.on('my event', namespace='/public')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    app.logger.debug('received my event: ' + str(json))
    if json.get('user_name', None):
        message = Messages(sender=json.get('user_name'),
                           message_text=json.get('message'))
        db.session.add(message)
        db.session.commit()
    app.logger.debug('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

##