# Bingo number generator used to play the game

###############################################################################################
# IMPORTS
# Import built in GUI package for python, random to pick numbers, ImageTK and Image are imported to be able to handle images for the bingo patterns
import tkinter as tk, random, os
import PIL
from PIL import ImageTk, Image

# Different bingo patterns - full house, single line, train tracks, postage stamp
bingoPatterns = ['SingleLine', 'TrainTracks', 'FullHouse']

# Generate initial variables. List of bingo numbers
bingoNumbers = list(range(1, 76))
last5Numbers = []
totalNumbersCalled = 0
activePatternImages = []
activePatternBigImages = []
inactivePatternImages = []

bingoLettersToCheck = {'B':15, 'I':15, 'N':15, 'G':15, 'O':15}

# Stores the current game, can't play if not set
currentGame = ''

###############################################################################################
# GAME GUI

# Generates the GUI as it should be on start up. GUI elements are made to be global variables in order to allow manipulation of the GUI over the course of the game.
def generateInitialGUI():
    global root, bingoPatternLabels, currentNumberLabel, bingoLabels, bingoNumbers, last5Numbers, totalNumbersCalledLabel
    
    root = tk.Tk()
    root.title('Bingo')
    root.grid_columnconfigure(0, weight=1, minsize=500)

    topFrame = tk.Frame(root, width = 500, height = 100)
    topFrame.grid()
    mainGameFrame = tk.Frame(root)
    mainGameFrame.grid()
    bottomFrame = tk.Frame(root)
    bottomFrame.grid()

    mainGameFrame.bind('<Button-1>', generateNextNumber)

    # Add images for bingo patterns
    loadPatternImages()

    # Different labels with different images stored in a list
    createInitialBingoPatternLabels(topFrame)

    randomBingoGame = tk.Button(topFrame, text = 'Random Game', command = startRandomGame)
    randomBingoGame.grid(row = 0, column = len(bingoPatternLabels))

    currentNumberLabel = tk.Label(mainGameFrame,
        text = '0',
        width = 5)
    currentNumberLabel.grid(row = 0, column = 16, rowspan = 7)
    currentNumberLabel.bind('<Button-1>', generateNextNumber)

    # Stores previous bingo number labels
    createLast5NumberLabels(mainGameFrame)

    # Initializes each label with correct numbers (1, 2, ..., 74, 75), appends label to the list
    createInitialBingoNumberLabels(mainGameFrame)

    totalNumbersCalledLabel = tk.Label(bottomFrame, text = totalNumbersCalled)
    totalNumbersCalledLabel.grid()

    root.mainloop()

# Loads the different pattern images
def loadPatternImages():
    for i in range(0, len(bingoPatterns)):
        # Creates a iterable loop
        activeImageName = 'bingo' + str(bingoPatterns[i]) + 'Active.png'
        inactiveImageName = 'bingo' + str(bingoPatterns[i]) + 'Inactive.png'

        # Loads in a smaller and larger version of each image
        activeImgOpen = Image.open(activeImageName)
        activeImg = ImageTk.PhotoImage(activeImgOpen.resize((75, 75), Image.ANTIALIAS))
        activeBigImg = ImageTk.PhotoImage(activeImgOpen.resize((200,200), Image.ANTIALIAS))

        inactiveImgOpen = Image.open(inactiveImageName)
        inactiveImg = ImageTk.PhotoImage(inactiveImgOpen.resize((75, 75), Image.ANTIALIAS))

        # Appends each image to corresponding list
        activePatternImages.append(activeImg)
        activePatternBigImages.append(activeBigImg)
        inactivePatternImages.append(inactiveImg)

# Creates the pattern labels which house the pattern images
def createInitialBingoPatternLabels(master):
    global bingoPatternLabels
    
    bingoPatternLabels = []
    for i in range(0, len(bingoPatterns)):
        imageLabel = tk.Label(master)
        if i == 0:
            imageLabel.config(image = inactivePatternImages[0])
        elif i == 1:
            imageLabel.config(image = inactivePatternImages[1])
        elif i == 2:
            imageLabel.config(image = inactivePatternImages[2])

        imageLabel.grid(row = 0, column = i)
        bingoPatternLabels.append(imageLabel)

# Creates the labels which display the previous 5 numbers called
def createLast5NumberLabels(master):
    global last5NumberLabels
    
    last5NumberLabels = []

    for i in range(0, 5):
        newLabel = tk.Label(master, text = '#', bg = 'cyan', width = 2)
        newLabel.grid(row = 1, column = i)
        newLabel.bind('<Button-1>', generateNextNumber)
        last5NumberLabels.append(newLabel)

# Creates the labels for numbers 1, 2, ..., 74, 75
def createInitialBingoNumberLabels(master):
    global bingoLabels, bingoLetterLabels

    # Stores each bingo number label in a list
    bingoLabels = []
    bingoLetterLabels = []

    currentRow = 2
    for i in range(0, 75):
        newLabel = tk.Label(master, text = str(i+1), width = 2)

        # Arranges the labels in a 5x15 grid
        if (i+1) % 15 == 0:
            
            nextLetterLabel = tk.Label(master, text = 'Letter', width = 2, bg = 'black', fg = 'white')

            # Generates each letter before the row of numbers starts
            if currentRow == 2:
                nextLetterLabel.config(text = 'B')
                nextLetterLabel.grid(row = currentRow, column = 0, padx = (2, 2), pady = (5, 5))
            elif currentRow == 3:
                nextLetterLabel.config(text = 'I')
                nextLetterLabel.grid(row = currentRow, column = 0, padx = (2, 2), pady = (5, 5))
            elif currentRow == 4:
                nextLetterLabel.config(text = 'N')
                nextLetterLabel.grid(row = currentRow, column = 0, padx = (2, 2), pady = (5, 5))
            elif currentRow == 5:
                nextLetterLabel.config(text = 'G')
                nextLetterLabel.grid(row = currentRow, column = 0, padx = (2, 2), pady = (5, 5))
            elif currentRow == 6:
                nextLetterLabel.config(text = 'O')
                nextLetterLabel.grid(row = currentRow, column = 0, padx = (2, 2), pady = (5, 5))
            
            nextLetterLabel.bind('<Button-1>', generateNextNumber)
            bingoLetterLabels.append(nextLetterLabel)

            newLabel.grid(row = currentRow, column = ((i)%15) + 1, padx = (2, 2), pady = (5, 5))
            
            currentRow += 1
        else:
            newLabel.grid(row = currentRow, column = ((i)%15) + 1, padx = (2, 2), pady = (5, 5))
        
        newLabel.bind('<Button-1>', generateNextNumber)

        bingoLabels.append(newLabel)

# Resets all GUI elements back to their default states
def resetGUI():
    
    # Reset last 5 numbers
    for label in last5NumberLabels:
        label.config(text = '#', bg = 'cyan', width = 2)

    # Reset BINGO labels
    for label in bingoLetterLabels:
        label.config(width = 2, bg = 'black', fg = 'white')

    # Reset main number labels
    for label in bingoLabels:
        # Sets the background to match that of the root frame as it is impossible to make it transparent
        label['bg'] = root['bg']
        label.config(fg = 'black')

    # Reset the current number label back to 0
    currentNumberLabel.config(text = 0)

    # Reset the total numbers called back to 0
    totalNumbersCalledLabel.config(text = 0)

    bingoLettersToCheck['B'] = 15
    bingoLettersToCheck['I'] = 15
    bingoLettersToCheck['N'] = 15
    bingoLettersToCheck['G'] = 15
    bingoLettersToCheck['O'] = 15

###############################################################################################
# GAME FUNCTIONALITY

# Overlays a frame with a large image of the active pattern in play
def showBigPattern(patternToShow):
    global testLabel, imageFrame
    
    imageFrame = tk.Frame(root)
    imageFrame.grid(row = 0, column = 0, sticky = tk.N, rowspan = 3)

    # Ensures the user cannot click the frame below the popup
    imageFrame.grab_set()

    testLabel = tk.Label(imageFrame, width = root.winfo_width(), height = root.winfo_height())

    if currentGame == bingoPatterns[0]:
        testLabel.config(image = activePatternBigImages[0])
    elif currentGame == bingoPatterns[1]:
        testLabel.config(image = activePatternBigImages[1])
    elif currentGame == bingoPatterns[2]:
        testLabel.config(image = activePatternBigImages[2])

    testLabel.grid(row = 0, column = 0)
    testLabel.bind('<Button-1>', destroyBigPattern)


# Destroys the overlapping frame
def destroyBigPattern(Event):
    imageFrame.destroy()

# Starts a bingo game
def startRandomGame():
    global currentGame, bingoPatterns

    # Either start a new game or restart the game
    if currentGame == '':
        currentGame = bingoPatterns[random.randint(0, len(bingoPatterns) - 1)]

        showBigPattern(bingoPatterns.index(currentGame))

        # Show grayed out images for bingo patterns not used
        for i in range(0, len(bingoPatternLabels)):
            if i != bingoPatterns.index(currentGame):

                if i == 0:
                    bingoPatternLabels[i].config(image = inactivePatternImages[i])
                elif i == 1:
                    bingoPatternLabels[i].config(image = inactivePatternImages[i])
                elif i == 2:
                    bingoPatternLabels[i].config(image = inactivePatternImages[i])
            
            else:
                if i == 0:
                    bingoPatternLabels[i].config(image = activePatternImages[i])
                elif i == 1:
                    bingoPatternLabels[i].config(image = activePatternImages[i])
                elif i == 2:
                    bingoPatternLabels[i].config(image = activePatternImages[i])

    else:
        currentGame = bingoPatterns[random.randint(0, len(bingoPatterns) - 1)]
        
        showBigPattern(bingoPatterns.index(currentGame))

        restartGame()

        # Show grayed out images for bingo patterns not used
        for i in range(0, len(bingoPatternLabels)):
            if i != bingoPatterns.index(currentGame):

                if i == 0:
                    bingoPatternLabels[i].config(image = inactivePatternImages[i])
                elif i == 1:
                    bingoPatternLabels[i].config(image = inactivePatternImages[i])
                elif i == 2:
                    bingoPatternLabels[i].config(image = inactivePatternImages[i])
            
            else:
                if i == 0:
                    bingoPatternLabels[i].config(image = activePatternImages[i])
                elif i == 1:
                    bingoPatternLabels[i].config(image = activePatternImages[i])
                elif i == 2:
                    bingoPatternLabels[i].config(image = activePatternImages[i])

# Restarts the game by resetting all relevant variables and labels back to their default states
def restartGame():
    global bingoNumbers, last5Numbers, totalNumbersCalled

    bingoNumbers = list(range(1, 76))
    last5Numbers = []
    totalNumbersCalled = 0

    resetGUI()

# Function to generate a random number
def generateNextNumber(event):
    global totalNumbersCalled

    if currentGame != '':
        if len(bingoNumbers) > 0:
            # Generates a random index between 1 and the length of the remaining bingo numbers
            nextNumber = bingoNumbers[random.randint(0, len(bingoNumbers) - 1)]
            bingoLabels[nextNumber-1].config(bg = 'green', fg = 'white')
            currentNumberLabel.config(text = nextNumber)
            bingoNumbers.remove(nextNumber)

            # Increment the total number of numbers called by 1 and update the corresponding label
            totalNumbersCalled += 1
            totalNumbersCalledLabel.config(text = totalNumbersCalled)

            updateLastNumberCalled(nextNumber)
            checkNumbersInRow(nextNumber)

# Update the last 5 numbers stored and update the corresponding labels
def updateLastNumberCalled(numberCalled):
    # If there have been 5 or more numbers called remove the oldest and then append the newest number
    if len(last5Numbers) >= 5:
        del last5Numbers[0]
        last5Numbers.append(numberCalled)
        for i in range(0, len(last5Numbers)):
            last5NumberLabels[i].config(text = last5Numbers[i])
    # If 5 numbers have not yet been called add the number to the list without deleting
    else:
        last5Numbers.append(numberCalled)
        numberRemaining = 5 - len(last5Numbers)
        for i in range(0, len(last5Numbers)):
            last5NumberLabels[i + numberRemaining].config(text = last5Numbers[i])

# Checks whether a row of numbers has been fully called, if it has then the corresponding letter background changes
def checkNumbersInRow(numberCalled):
    global bingoLettersToCheck

    if numberCalled > 0 and numberCalled <= 15:
        # Check B
        bingoLettersToCheck['B'] -= 1
    elif numberCalled > 15 and numberCalled <= 30:
        # Check I
        bingoLettersToCheck['I'] -= 1
    elif numberCalled > 30 and numberCalled <= 45:
        # Check G
        bingoLettersToCheck['N'] -= 1
    elif numberCalled > 45 and numberCalled <= 60:
        # Check I
        bingoLettersToCheck['G'] -= 1
    elif numberCalled > 60 and numberCalled <= 75:
        # Check O
        bingoLettersToCheck['O'] -= 1
    
    # Check if each row has numbers, if not numbers set the background color to magenta
    if bingoLettersToCheck['B'] == 0:
        bingoLetterLabels[0].config(bg = 'magenta')
    
    if bingoLettersToCheck['I'] == 0:
        bingoLetterLabels[1].config(bg = 'magenta')
    
    if bingoLettersToCheck['N'] == 0:
        bingoLetterLabels[2].config(bg = 'magenta')

    if bingoLettersToCheck['G'] == 0:
        bingoLetterLabels[3].config(bg = 'magenta')

    if bingoLettersToCheck['O'] == 0:
        bingoLetterLabels[4].config(bg = 'magenta')

###############################################################################################
# STARTS THE PROGRAM

def main():
    generateInitialGUI()

if __name__ == '__main__':
    main()
