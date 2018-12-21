from flask import Flask, render_template, session
from flask_socketio import SocketIO
from mysqlconnection import connectToMySQL
import json, random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'make it so number one'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    mysql = connectToMySQL('pw2')
    player = mysql.query_db('SELECT * FROM monster')
    mysql = connectToMySQL('pw2')
    dungeon = mysql.query_db('SELECT * FROM dungeon')
    session['name'] = 'Christmas Elf'
    session['atk'] = 7
    session['def'] = 10
    session['agi'] = 6
    session['mag'] = 4
    session['luk'] = 4
    session['hp'] = 5
    session['mname'] = player[0]['name']
    session['mhp'] = player[0]['hp']
    session['mac'] = player[0]['ac']
    session['special'] = player[0]['special']
    session['room']=0
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    mysql = connectToMySQL('pw2')
    dungeon = mysql.query_db('SELECT * FROM dungeon')
    if json['message']=='attack':
        x=random.randint(5,15)
        session['mhp'] = session['mhp']-x
        json['def']=session['mhp']
        json['message']='You did '+str(x)+' damage!'
    if json['message']=='move':
        session['room']=1
    json['stat']= "You are in a "+dungeon[session['room']]['type']+" you see a "+dungeon[session['room']]['special']
    socketio.emit('my response', json, callback=messageReceived)

if __name__=='__main__':
    socketio.run(app, debug=True)