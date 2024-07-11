from controllers.app_controller import create_app
from flask_socketio import SocketIO
from controllers.real_time_controller import create_socketio_handlers
#from utils.create_db import create_db

if __name__ == "__main__":
    app, socketio, mqtt_client = create_app()
    create_socketio_handlers(socketio)
    #create_db(app)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True,  allow_unsafe_werkzeug=True)   