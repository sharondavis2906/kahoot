# Kahoot server

from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app)

pinname = '1234'
gamename = ''
numplayers = 0

question_num = 1
question_time = 30


lines = []

players = ['','','','','']
playersid = ['','','','','']
scores = [0,0,0,0,0]


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/player')
def player():
    return render_template('player.html')




@app.route('/question')
def question():
    return render_template('question.html')



@app.route('/answer')
def answer():
    return render_template('answer.html')


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

    for p in range (0,4):
      players[p]=''

      
    emit('redirect from flask to start', {'url': url_for('index')})



# Message from HTML/JS after pressing Game Start on Start page
@socketio.on('gamestart', namespace='/start')
def receive_message_from_user_start(message):
    print('USER MESSAGE START GAME FROM START: {}'.format(message))
     
    global gamename 
    global pinname
    global question_num
    global question_time
    
    question_time = 5
    
    # Display question on host screen
    emit('redirect from flask to question', {'url': url_for('question',game=gamename,pin=pinname,que_num=question_num, que_time=question_time)}, namespace='/question')

    # Answer screen on client screen
    #p=0
    #while p < numplayers:
      #emit('redirect from flask to question', {'url': url_for('answer',game=gamename,pin=pinname,que_num=question_num, que_time=question_time)}, namespace='/answer')


# send question time


# Question timeout
@socketio.on('question timeout', namespace='/question')
def receive_message_from_user(message):
    print('USER MESSAGE FROM QUESTION TIMEOUT: {}'.format(message))
 

    global gamename 
    global pinname
    global question_num
    global question_time

    # Redirect to results
     
       
# timeout before question is displayed      
@socketio.on('question timeoutp', namespace='/question')
def receive_message_from_user(message):
    print('USER MESSAGE FROM PRE-QUESTION TIMEOUT: {}'.format(message))
 

    global gamename 
    global pinname
    global question_num
    global question_time
    global lines

    linen = (question_num-1) * 5

    print('LINES: {}'.format(lines))

    # Display the question on Host
    emit('message from flask to question',{'question':lines[linen],'answer1':lines[linen+1],'answer2':lines[linen+2],'answer3':lines[linen+3],'answer4':lines[linen+4]},namespace='/question')    

    # Display the answer on Player
      

# Message from HTML/JS after selecting a game 
@socketio.on('game selected', namespace='/')
def receive_message_from_user(message):
    print('USER MESSAGE FROM INDEX: {}'.format(message))
    
    global gamename
    global lines
    gamename = message
    
    # Load file
    
    fname = gamename + ".txt"
    
    filep = open(fname, "r")
    lines = filep.readlines()
    filep.close()
    
    print('LINESXXX: {}'.format(lines))
    
    #emit('from flask', message.upper())
 
    #emit('from flask', message,broadcast=True,include_self=False,namespace='/start')   
    #emit('from flask', message,namespace='/start')
    
 
    
    #uu = "?game=" + message
       
    # Sends /start?game=message&players='0'&pin='1234' (no players when moving from index to start)  
    
    global pinname
    global numplayers
    
    numplayers = 0
    
    
    emit('redirect from flask to index', {'url': url_for('start',game=gamename,pin=pinname)})
    
   
   
   
   
# Message from HTML/JS after a player connects and enters the PIN
@socketio.on('gamepin', namespace='/player')
def receive_message_from_user_join(message):
    print('USER MESSAGE PIN ENTERED FROM PLAYER: {}'.format(message))

    global pinname
    
    if message == pinname:
      emit('message from flask to player', {'mode': 'pinok'})
    else:
      emit('message from flask to player', {'mode': 'badpin'})
   
   
   
   
   # Message from HTML/JS after entering the nickname 
@socketio.on('nickname', namespace='/player')
def receive_message_from_user_join(message):
    print('USER MESSAGE PIN ENTERED FROM NICKNAME: {}'.format(message))

    global pinname
    global gamename
    global numplayers
    global players

    if message == '':
      # Error
      emit('message from flask to player', {'mode': 'badname'})
    else:     
    
      players[numplayers] = message     # Name of player
      playersid[numplayers] = request.sid
      numplayers += 1
                 
      # Host
      emit('message from flask to start',{'numplayers':numplayers,'player1':players[0],'player2':players[1],'player3':players[2],'player4':players[3],'player5':players[4]},broadcast=True,include_self=False,namespace='/start')
      
      # Players
      emit('message from flask to player', {'mode': 'nameok'})

   
   
   
   
   
   
   
   
   
   


if __name__ == '__main__':
    socketio.run(app)
