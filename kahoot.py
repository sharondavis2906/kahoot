# Kahoot server

from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app)

pinname = '1234'
gamename = ''
numplayers = 0

players = ['','','','','']



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/join')
def join():
    return render_template('join.html')


@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/wait')
def wait():
    return render_template('wait.html')

@app.route('/nickname')
def nickname():
    return render_template('nickname.html')


@app.route('/start')
def start():
    return render_template('start.html')


# Message from HTML/JS after pressing Game Exit on Start page
@socketio.on('gameexit', namespace='/start')
def receive_message_from_user_start(message):
    print('USER MESSAGE EXIT GAME FROM START: {}'.format(message))

    global numplayers
    global players
    numplayers = 0

    for x in range (0,4):
      players[x]=''

      
    emit('redirect from flask to start', {'url': url_for('index')})



# Message from HTML/JS after pressing Game Start on Start page
@socketio.on('gamestart', namespace='/start')
def receive_message_from_user_start(message):
    print('USER MESSAGE START GAME FROM START: {}'.format(message))
     
    global gamename 
    global pinname
    
    emit('redirect from flask to start', {'url': url_for('question',game=gamename,pin=pinname)})




# Message from HTML/JS after selecting a game 
@socketio.on('game selected', namespace='/')
def receive_message_from_user(message):
    print('USER MESSAGE FROM INDEX: {}'.format(message))
    
    global gamename
    gamename = message
    
    #emit('from flask', message.upper())
 
    #emit('from flask', message,broadcast=True,include_self=False,namespace='/start')   
    #emit('from flask', message,namespace='/start')
    
 
    
    #uu = "?game=" + message
       
    # Sends /start?game=message&players='0'&pin='1234' (no players when moving from index to start)  
    
    global pinname
    global numplayers
    
    emit('redirect from flask to index', {'url': url_for('start',game=gamename,players=numplayers,pin=pinname,player1=players[0],player2=players[1],player3=players[2],player4=players[3],player5=players[4])})
    #emit('redirect from flask', {'url': uu})


# Message from HTML/JS after entering PIN in Join 
@socketio.on('gamepin', namespace='/join')
def receive_message_from_user_join(message):
    print('USER MESSAGE PIN ENTERED FROM JOIN: {}'.format(message))

    global pinname
    
    if message == pinname:
      emit('redirect from flask', {'url': url_for('nickname')})
    else:
      emit('redirect from flask', {'url': url_for('join',status='error')})



# Message from HTML/JS after entering NICKNAME in Nickname 
@socketio.on('nickname', namespace='/nickname')
def receive_message_from_user_join(message):
    print('USER MESSAGE PIN ENTERED FROM NICKNAME: {}'.format(message))

    global pinname
    global gamename
    global numplayers
    global players

    if message == '':
      # Error
      emit('redirect from flask', {'url': url_for('nickname',status='error')})
    else:     
    
      players[numplayers] = message     # Name of player
      numplayers += 1
      #emit('redirect from flask', {'url': url_for('active')})
      
      # Broadcast not needed in this implementation (will be required if multiple cuncurrent games are supported)
      emit('redirect from flask to start', {'url': url_for('start',game=gamename,players=numplayers,pin=pinname,player1=players[0],player2=players[1],player3=players[2],player4=players[3],player5=players[4])},broadcast=True,include_self=False,namespace='/start')

      emit('redirect from flask', {'url': url_for('wait',type='game',time='')})


'''
@socketio.on('message')
def receive_message(message):
    print('########: {}'.format(message))
    send('This is a message from Flask.')

@socketio.on('custom event')
def receive_custom_event(message):
    print('THE CUSTOM MESSAGE IS: {}'.format(message['name']))
    emit('from flask', {'extension' : 'Flask-SocketIO'}, json=True)

'''

if __name__ == '__main__':
    socketio.run(app)
