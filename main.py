from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('javaClient.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received event: ' + str(json))

    if(json['data'] == "start recording"):
        print("Start Record")
        socketio.emit('my_message', "Start Session")


    if(json['data'] == "end recording"):
        print("End Record")
        socketio.emit('my_message', "End Session")



if __name__ == '__main__':
    socketio.run(app, debug=True)