import os
from app import app, socketio


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = bool(int(os.getenv('DEBUG', False)))
    socketio.run(app=app, host='0.0.0.0', port=port, debug=debug)
    # socketio.run()
	# app.run(host='0.0.0.0', port=port, debug=debug)

