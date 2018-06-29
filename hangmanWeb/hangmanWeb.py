from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import json
import random
import re
import sys

app = Flask(__name__)

app.secret_key = '12345'


@app.route("/hangman")
def render_homepage():
    return render_template(
        'index.html')


@app.route("/hangman/newgame",  methods=['POST'])
def new_game():
    word_length = request.form['word_length'];
    session['word_length'] = str(word_length)
    session['selected_word'] = get_word(session['word_length'])
    session['current_state'] = initialise_current_state(session['selected_word'])
    session['lives_remaining'] = 10
    session['used_letters'] = []
    return render_template(
        'gamebody.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
        currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']))


def get_word(word_length):

    word_list_filtered = []
    selected_word = ''

    keyword = re.compile(r'\b\w{' + re.escape(word_length) + r'}\b')

    with open("wordList.txt", "r") as word_list:
        for line in word_list:
            for result in keyword.findall(line):
                word_list_filtered.append(result)

        word_list.close()
    if len(word_list_filtered) == 0:
        sys.exit("No words found in dictionary for length")
    selected_word = word_list_filtered[random.randint(0, len(word_list_filtered) - 1)]

    del word_list_filtered
    return selected_word.upper()


def initialise_current_state(selected_word):
    current_state = ''
    for letter in selected_word:
        #current_state.append('_')
        current_state = current_state + '_'
    current_state = list(current_state)
    return current_state

@app.route("/hangman/guess", methods=['GET'])
def get_guess1():
    return "GET request not post"


@app.route("/hangman/guess", methods=['POST'])
def get_guess():
    input_letter = request.form['input_letter'];
    input_letter = input_letter.upper()
    result = 0
    if validate_guess(input_letter):
        process_guess(input_letter)
    '''else:
        get_guess(session['selected_word'])'''
    print session['used_letters']
    print ('current state = ' + str(session['current_state']))

    return render_template(
        'gamebody.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
        currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']),
        inputLetter=input_letter, livesRemaining=session['lives_remaining'])

    '''if result ==0:
        return render_template(
            'gamebody.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
            currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']),
            inputLetter=input_letter, livesRemaining=session['lives_remaining'])
    elif result==1:
        return render_template(
            'lose.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
            currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']),
            inputLetter=input_letter, livesRemaining=session['lives_remaining'])
    elif result==2:
        return render_template(
            'win.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
            currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']),
            inputLetter=input_letter, livesRemaining=session['lives_remaining'])
    '''

    #return result

    '''render_template(
        'gamebody.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
        currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']),
        inputLetter=input_letter, livesRemaining=session['lives_remaining'])'''


def validate_guess(input_letter):
    if not input_letter.isalpha() or not len(input_letter) == 1:
        print "Invalid Input"
        return False
    elif input_letter in session['used_letters']:
        print "Letter already used"
        return False
    else:
        used_letters = session['used_letters']
        used_letters.append(input_letter)
        session['used_letters'] = used_letters
        print session['used_letters']
        return True


def process_guess(input_letter):
    if session['lives_remaining'] >= 0:
        current_state = session['current_state']
        match_index = [match.start() for match in re.finditer(input_letter, session['selected_word'])]
        if len(match_index) == 0:
            wrong_guess(input_letter)

        for index in match_index:
            current_state[index] = input_letter

        session['current_state'] = current_state

        if ''.join(session['current_state']) == session['selected_word']:
            print ' '.join(session['current_state'])
            return 2
            render_template(
                'win.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
                currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']),
            inputLetter=input_letter, livesRemaining=session['lives_remaining'])
            sys.exit("You Win!")
        else:
            print "\n" + ' '.join(session['current_state'])
            return


def wrong_guess(input_letter):
    print (input_letter + " is wrong.")

    session['lives_remaining'] -= 1

    if session['lives_remaining'] == 0:
        return render_template(
            'lose.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
            currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']),
            inputLetter=input_letter, livesRemaining=session['lives_remaining'])
        sys.exit("You Lose. Answer: " + session['selected_word'])
    else:
        return render_template(
            'gamebody.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
            currentState=' '.join(session['current_state']), usedLetters=' '.join(session['used_letters']),
            inputLetter=input_letter, livesRemaining=session['lives_remaining'])



def print_hangman():
    print ''


@app.route("/")
def index():
    return "Hangman"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)