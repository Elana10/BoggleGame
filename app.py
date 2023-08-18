from boggle import Boggle
from flask import Flask, session, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "somebodyoncetoldme"
debug = DebugToolbarExtension(app) 

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TESTING'] = True

boggle_game = Boggle() 

@app.route('/')
def boggle_home():
    """shows the base.html home page with boutique landing page board """
    board = [['B','O','G','G','L', 'E'],['B','O','G','G','L', 'E'],['B','O','G','G','L', 'E'],['B','O','G','G','L', 'E'],['B','O','G','G','L', 'E']]

    return render_template('base.html', board = board)

@app.route('/guess', methods = ['POST'])
def handle_guess_input():
    """
    This will take the javascript axios request with the 
    
    """
    # Retrieve JSON data from the axios request.
    data = request.json 
    #Retrieve the guess information from the data object. 
    guess = data.get('guess')
   
    
    # Use the Boggle Class method to check the guess. 
    board = session['board']
    
    response = boggle_game.check_valid_word(board, guess.upper())   

    #Ensure that the guess hasn't been guessed before and updates the response, if necessary (or returns the same response back)
    response = review_word_to_guess_list(guess, response)

    # Send the checked response to axios request in js file (using json code).
    return jsonify({'results': response, 'current_score' : session.get('current_score',0), 'high_score' : session.get('high_score',0)})

def update_guess_list(guess):
    # add the guess word to the list in sessions
    guess_list = session.get('guess_list', [])
    guess = guess.upper()
    guess_list.append(guess)
    session['guess_list'] = guess_list

def review_word_to_guess_list(guess, response):
    # true/false the word has already been guessed. 
    guess_list = session.get('guess_list', [])
    guess = guess.upper()
    word_guessed_already = guess in guess_list

    #update session['guess_list'] or change response to already guessed. 
    if word_guessed_already:
        response = 'already-guessed'
        return response
    elif response == 'not-word' or response == 'not-on-board':
        return response
    else:
        update_score(guess)
        update_guess_list(guess)
        return response

def update_score(guess):
    score = session.get('current_score', 0)
    word_len = len(guess)

    if word_len < 5:
        score = score + 1
    elif word_len < 6:
        score = score + 2
    elif word_len < 7:
        score = score + 3
    elif word_len < 8:
        score = score + 5
    else: 
        score = score + 11

    session['current_score'] = score
    update_high_score(session['current_score'])

def update_high_score(score):
    high_score = session.get('high_score', 0)
    if score > high_score:
        session['high_score'] = score

@app.route('/game')
def boggle_game_start():

    board = boggle_game.make_board()
    session['board'] = board

    session['current_score'] = 0
    high_score = session.get('high_score', 0)
    session['guess_list'] = []

    count = session.get('attempt_num', 0) + 1
    session['attempt_num'] = count
    
    return jsonify({'board' : board, 'count' : count, 'current_score' : 0, 'high_score' : high_score, 'guess_list' : session['guess_list']})