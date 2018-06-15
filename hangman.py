import sys
import re
import random

livesRemaining = 0
usedLetters = []
currentState = ""

def validateInput(userInput):
	try:
			userInput = int(userInput)
			if (2 < userInput < 11):
				return True
			else:
				return False
	except ValueError:
			return False

def getWord(wordLength):
	wordListFiltered = []
	
	keyword = re.compile(r'\b\w{'+ re.escape(wordLength) + r'}\b')

	with open("wordList.txt","r") as wordList:    
		for line in wordList:
			for result in keyword.findall(line):
				wordListFiltered.append(result)
				
	wordList.close()
	if len(wordListFiltered) == 0:
		sys.exit("No words found in dictionary for length")
	selectedWord = wordListFiltered[random.randint(0,len(wordListFiltered)-1)]
	
	del wordListFiltered
	
	global currentState
	for letter in selectedWord:
		currentState = currentState + "_"
	#currentState = currentState.strip()
	currentState = list(currentState)
	return selectedWord.upper()

def validateGuess(inputLetter):
	if not inputLetter.isalpha() or not len(inputLetter)==1:
		print "Invalid Input"
		return False
	elif inputLetter in usedLetters:
		print "Letter already used"
		return False
	else:
		usedLetters.append(inputLetter)
		return True
	

#def lives():

def getGuess(selectedWord):
	inputLetter = str(raw_input("\n\nEnter Letter: ")).upper()
	if validateGuess(inputLetter):
		processGuess(inputLetter, selectedWord)
	else:
		getGuess(selectedWord)
		
		
def processGuess(inputLetter, selectedWord):
	
	if livesRemaining>=0:
		matchIndex = [match.start() for match in re.finditer(inputLetter, selectedWord)]
		if len(matchIndex) == 0:
			wrongGuess(inputLetter, selectedWord)
		
		for index in matchIndex:
			currentState[index]=inputLetter
		
		if ''.join(currentState)==selectedWord:
			print ' '.join(currentState)
			sys.exit("You Win!")
		else:
			print ' '.join(currentState)
			getGuess(selectedWord)
			
	

def wrongGuess(inputLetter, selectedWord):
	global livesRemaining
	
	print (inputLetter + " is wrong.")
	
	livesRemaining -=1
	
	if livesRemaining == 0:
		printHangman(livesRemaining)
		sys.exit("You Lose. Answer: " + selectedWord)
	else:
		printHangman(livesRemaining)
		print ' '.join(currentState)
		getGuess(selectedWord)
	
def printHangman(livesRemaining):
	
	switcher = {
        0: " _________     \n|         |    \n|         0    \n|        /|\   \n|        / \   \n|              \n|\n|__________    \n",
        1: " _________     \n|         |    \n|         0    \n|        /|    \n|        / \   \n|              \n|\n|__________    \n",
        2: " _________     \n|         |    \n|         0    \n|         |    \n|        / \   \n|              \n|\n|__________    \n",
        3: " _________     \n|         |    \n|         0    \n|         |    \n|        /     \n|\n|\n|__________    \n",
        4: " _________     \n|         |    \n|         0    \n|         |    \n|\n|\n|\n|__________    \n",
        5: " _________     \n|         |    \n|         0    \n|\n|\n|\n|\n|__________    \n",
        6: " _________     \n|         |    \n|\n|\n|\n|\n|\n|__________    \n",
        7: " _________     \n|\n|\n|\n|\n|\n|\n|__________    \n",
        8: " _________     \n|\n|\n|\n|\n|\n|\n|\n",
        9: " _________     \n\n\n\n\n\n\n\n",

    }
	
	print switcher.get(livesRemaining, "Invalid Lives")
	print "\n\n"
	
def main():
	args = sys.argv[1:]
	
	if not args:
		print 'usage: [--wordLength <wordLength>]'
		sys.exit(1)
	
	wordLength = ''
	
	if args[0] != '--wordLength':
		print 'usage: [--wordLength <wordLength>]'
	else:
		wordLength = args[1]
		if validateInput(wordLength) is False:
			sys.exit('Word length must be an Integer between 3 and 10')

	del args[0:]
	
	selectedWord = getWord(wordLength)	
	#print selectedWord
	#print currentState
	print ' '.join(currentState)
	
	global livesRemaining
	livesRemaining = 10
	#while livesRemaining > 0:
	getGuess(selectedWord)
	#processGuess(inputLetter, selectedWord)
	
	
		
	

if __name__ == '__main__':
  main()