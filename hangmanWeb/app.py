from flask import Flask, flash, redirect, render_template, request, session, abort
from flask.ext.session import Session
import random
import re
import sys

app = Flask(__name__)
Session(app)

game = None


class Game:
    wordLength = None
    selectedWord = None
    currentState = None
    usedLetters = ['a']
    livesRemaining = None

    def __init__(self):
        pass

    def __init__(self, wordLength = 0, selectedWord= '', currentState= [], usedLetters= [], livesRemaining= 10):
        self.wordLength = wordLength
        self.selectedWord = selectedWord
        self.currentState = currentState
        self.usedLetters = usedLetters
        self.livesRemaining = livesRemaining

def getWord(wordLength):

    wordListFiltered = []
    selectedWord = ''

    keyword = re.compile(r'\b\w{' + re.escape(wordLength) + r'}\b')

    with open("wordList.txt", "r") as wordList:
        for line in wordList:
            for result in keyword.findall(line):
                wordListFiltered.append(result)

    wordList.close()
    if len(wordListFiltered) == 0:
        sys.exit("No words found in dictionary for length")
    selectedWord = wordListFiltered[random.randint(0, len(wordListFiltered) - 1)]

    del wordListFiltered
    return selectedWord.upper()


def initaliseCurrentState(selectedWord):
    currentState = ''
    for letter in selectedWord:
        currentState = currentState + "_"
    currentState = list(currentState)
    return currentState


@app.route("/")
def index():
    return "Hangman"


#@app.route("/hangman/newgame/<int:wordLength>", methods=['POST'])
@app.route("/hangman/newgame/<int:wordLength>")
def newGame(wordLength):
    game = Game()
    game.wordLength = str(wordLength)
    game.selectedWord = getWord(game.wordLength)
    game.currentState = initaliseCurrentState(game.selectedWord)
    game.livesRemaining = 10

    session['game'] = Game(game.wordLength, game.selectedWord, game.currentState, game.usedLetters, game.livesRemaining)

    return render_template(
        'layout.html', game=game, wordLength=game.wordLength, selectedWord=game.selectedWord, currentState=' '.join(game.currentState),
            usedLetters=' '.join(game.usedLetters))


#@app.route("/hangman/guess/<string:inputLetter>", methods = ['POST'])
@app.route("/hangman/guess/<string:inputLetter>")
def test(inputLetter):
    global game
    print game
    game.currentState = inputLetter
    '''return render_template(
        'layout.html', game=game, wordLength=game.wordLength, selectedWord=game.selectedWord,
        currentState=' '.join(game.currentState),
        usedLetters=' '.join(game.usedLetters))'''
    return render_template(
        'layout.html', game=(str(game)+"Game Object Test"), currentState=game.currentState)

def getGuess(inputLetter):
    inputLetter = inputLetter.upper()
    if validateGuess(inputLetter):
        processGuess(inputLetter)
    else:
        getGuess(game.selectedWord)


def validateGuess(inputLetter):
    global game
    if not inputLetter.isalpha() or not len(inputLetter) == 1:
        print "Invalid Input"
        return False
    elif inputLetter in game.usedLetters:
        print "Letter already used"
        return False
    else:
        game.usedLetters.append(inputLetter)
        return True

def processGuess(inputLetter):
    if game.livesRemaining >= 0:
        matchIndex = [match.start() for match in re.finditer(inputLetter, game.selectedWord)]
        if len(matchIndex) == 0:
            wrongGuess(inputLetter)

        for index in matchIndex:
            game.currentState[index] = inputLetter

        if ''.join(game.currentState) == game.selectedWord:
            print ' '.join(game.currentState)
            sys.exit("You Win!")
        else:
            print "\n" + ' '.join(game.currentState)
            return render_template(
                'layout.html', wordLength=game.wordLength, selectedWord=game.selectedWord,
                currentState=' '.join(game.currentState),
                usedLetters=' '.join(game.usedLetters))
            #getGuess(game.selectedWord)


def wrongGuess(inputLetter):
    global game

    print (inputLetter + " is wrong.")

    game.livesRemaining -= 1

    if game.livesRemaining == 0:
        printHangman()
        sys.exit("You Lose. Answer: " + game.selectedWord)
    else:
        printHangman()
        print ' '.join(game.currentState)
        getGuess()

def printHangman():
    print ''


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port=80)