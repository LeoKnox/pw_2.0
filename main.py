from flask import Flask, render_template, session
from flask_socketio import SocketIO
from mysqlconnection import connectToMySQL
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'make it so number one'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    mysql = connectToMySQL('pw2')
    player = mysql.query_db('SELECT * FROM pw2.Char WHERE idChar=1')
    session.name = 'Christmas Orc'
    print(player.Name)
    session['atk'] = 7
    session['def'] = 10
    session['agi'] = 6
    session['mag'] = 4
    session['luk'] = 4
    session['hp'] = 58
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    json['def']=7
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__=='__main__':
    socketio.run(app, debug=True)