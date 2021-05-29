# Альтернативой socketio.run(app)является использование gunicorn в качестве веб-сервера с помощью eventlet или
#  gevent worker. Для этого варианта необходимо установить eventlet или gevent в дополнение к gunicorn.
#  Командная строка, запускающая сервер eventlet через gunicorn:
# https://flask-socketio.readthedocs.io/en/latest/
gunicorn --worker-class eventlet -w 1 module:app
# gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 module:app
