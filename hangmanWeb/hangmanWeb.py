from flask import Flask, flash, redirect, render_template, request, session, abort
#from flask.ext.session import Session
import random
import re
import sys

app = Flask(__name__)

app.secret_key = '12345'

#session(game)


@app.route("/hangman/newgame/<int:word_length>")
def newGame(word_length):
    session['word_length'] = str(word_length)
    session['selected_word'] = get_word(session['word_length'])
    session['current_state'] = initialise_current_state(session['selected_word'])
    session['lives_remaining'] = 10
    session['used_letters'] = []

    return render_template(
        'layout.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
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


@app.route("/hangman/guess/<string:input_letter>")
def get_guess(input_letter):
    input_letter = input_letter.upper()
    if validate_guess(input_letter):
        process_guess(input_letter)
    '''else:
        get_guess(session['selected_word'])'''
    print session['used_letters']
    return render_template(
        'layout.html', session=session, wordLength=session['word_length'], selectedWord=session['selected_word'],
        currentState=' '.join(session['current_state']), usedLetters=(session['used_letters']),
        inputLetter="received")


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
        match_index = [match.start() for match in re.finditer(input_letter, session['selected_word'])]
        if len(match_index) == 0:
            wrong_guess(input_letter)

        for index in match_index:
            session['current_state'] = input_letter

        if ''.join(session['current_state']) == session['selected_word']:
            print ' '.join(session['current_state'])
            sys.exit("You Win!")
        else:
            print "\n" + ' '.join(session['current_state'])
            return render_template(
                'layout.html')
            '''return render_template(
                'layout.html', session=session, wordLength=session['word_length'],
                selectedWord=session['selected_word'], currentState=' '.join(session['current_state']),
                usedLetters=(session['used_letters']))'''
            #getGuess(game.selectedWord)


def wrong_guess(input_letter):
    print (input_letter + " is wrong.")

    session['lives_remaining'] -= 1

    if session['lives_remaining'] == 0:
        print_hangman()
        sys.exit("You Lose. Answer: " + session['selected_word'])
    else:
        print_hangman()
        print ' '.join(session['current_state'])
        #get_guess()


def print_hangman():
    print ''


@app.route("/")
def index():
    return "Hangman"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)