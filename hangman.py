import sys
import re
import random

livesRemaining = 0
usedLetters = ["A"]
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
		currentState = currentState + " _"
	currentState.strip()
	return selectedWord

def validateGuess(inputLetter):
	if inputLetter.isalpha() and inputLetter not in usedLetters and len(a):
		usedLetters.append(inputLetter)
		return True
	else:
		print "Invalid Character or letter already used"
		return False
	

#def lives():

def getGuess():
	inputLetter = str(raw_input("Entered Letter: ")).upper()
	if validateGuess(inputLetter):
		sys.exit("Letter is: " + inputLetter)
	else:
		getGuess()
	
	
	
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
	print selectedWord

	
	global livesRemaining
	livesRemaining = 8
	#while livesRemaining > 0:
	getGuess()
	
	
		
	

if __name__ == '__main__':
  main()