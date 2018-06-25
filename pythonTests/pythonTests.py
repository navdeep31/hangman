class Game:
    wordLength = None
    livesRemaining = None
    usedLetters = ['a']
    currentState = None

    def __init__(self):
        pass



def main():
    game = Game()
    inputLetter = 'b'
    if inputLetter in game.usedLetters:
        print "true"
    else:
        return "false"


if __name__ == "__main__":
    main()