#######Created by Team 84 - - - Dots & Boxes - - - CPSC 231
#######This is the secondary file of the program which contains the functions
#######which operates the gameplay (player/computer moves, save/loading during
#######gameplay, etc.

#       |----         OVERVIEW OF FILE LAYOUT         ----|       

#                       IMPORTS           
#                       GLOBAL VARIABLES        
#                       SETUP      
#                       SAVING             
#                       LOADING                 
#                       COMPUTER MOVE GENERATION         
#                       PLAYER MOVE INPUT             
#                       MOVE CONVERSION
#                       CHECKING/SAVING GAME STATE                
#                       DRAWING MOVES         
#                       END OF GAME            
#                       MAIN FUNCTION

#       |----        START OF FILE     ----|         #

#       |----         IMPORTS         ----|       #

import turtle
import constants
import platform
import time
import sys
import random

#       |----         GLOBAL VARIABLES        ----|      #

playerName = ''
listofMoves = []
currentMove = []
gameState = []

trt = turtle.Turtle()
trt.hideturtle()
eventTurtle = turtle.Turtle()
eventTurtle.hideturtle()
screenClickTurtle = turtle.Turtle()
screenClickTurtle.ht()
wn = turtle.Screen()

#       |----        FUNCTIONS        ----|         #

#       |----        SETUP        ----|         #

##This function generates the initial gameState model (for a new game) with
##all positions set to "!", which indicates they have not yet been triggered
##in the game. The gameState model is a 3D list (and this is the returned
##value), with the outermost list representing the entire game grid, the
##middle list representing a row of squares (starting from the topmost row),
##and the innermost list representing each individual square in order from
##left to right. Within each innermost list there are 5 elements: from left
##to right they are: (1) the initial of the owner of the square (either
##player "P", computer "C", or unowned "!"), (2) the north horizontal line
##on a square, (3) the east vertical line on a square, (4) the south
##horizontal line on a square, and (5) the west vertical line on a square;
##for each line, if not triggered via gameplay will be represented by "!",
##and once triggered via gameplay will be represented by either a "C" for
##computer or "P" for the player.
def generateblankState():
    
    blankState = []
    
    #Creates the middle list, which represents an entire row of squares on
    #the game grid The innermost list is first created and appended to this
    #middle list, after which it is reset before each pass through
    for rows in range(constants.n_dots-1):
        tempList = []

        #Creates the innermost list representing the squares in that specific
        #row. The number of squares and thus number of innermost lists is
        #determined by the n_dots constants which represents the number of
        #dots and therefore number of squares on the game grid
        for columns in range(constants.n_dots-1):
            #This represents a single square on the game grid in a completely
            #blank or untriggered state
            tempList.append(["!","!","!","!","!"])
            
        #The 2D list of a row of squares is appended to the final output
        #list after each pass through
        blankState.append(tempList)   
        
     
    return blankState

##This function checks if all the moves in a square have been completed but
##the owner initial has yet to be saved to the gameState. This check is
##necessary to prevent the  possibility of a user saving the game in between
##the time a scoring move is made and the actual saving that a square was
##completed.
def checkSquareInitial():

    for row in gameState:
        
        for square in row:

            #Checks through each square and if there is only one "!" left
            #in that square, that means the square has all moves completed
            #but the owner has yet to be set. If this condition is true the
            #function will return False to saveGame and True otherwise
            if square.count("!") == 1:
                
                return False
            
    return True

##Creates a 2D list of all possible moves for the current game.
#Each sublist contains a list of 4 coordinates representing a move
##This is used for the computer's random choice of move if a "smart"
##move is not available
def possibleMoves():
    
    #Generates a list of all possible moves using the constants dist
    #(the distance between dots) and the number of dots on the grid (n_dots)
    possibleMoves = []
    #Initial x and y positions on the game grid (the coordinates of the
    #first dot)
    xPosition = -constants.dist
    yPosition = constants.dist

    #Loop creates a 2D list containing all possible moves for the chosen
    #number of dots (n_dots). The first for loop is for decreasing the y
    #coordinate to move through each possible y coordinate on the game grid
    #The first nested for loop is for increasing the x coordinate to move
    #through each possible x coordinate on the game grid, and add a
    #horizontal move to the list. The second nested for loop is for
    #increasing the x coordinate to move through each possible x coordinate
    #on the grid, and add a vertical move to the list
    for rows in range(constants.n_dots):
        for columns in range(constants.n_dots - 1):
            possibleMoves.append([xPosition, yPosition,
                                  xPosition+constants.dist, yPosition])
            xPosition = xPosition + constants.dist
            
        #X position reset to be back in the initial position (x coordinate
        #of the first dot)
        xPosition = -constants.dist
    
        if len(possibleMoves) < (
                          (((constants.n_dots * 2)-2) * constants.n_dots)-3):
            for columns in range(constants.n_dots):
                possibleMoves.append([xPosition, yPosition,
                                      xPosition, yPosition-(constants.dist)])
                xPosition = xPosition + constants.dist

        #Y position decreased to move down to the next row of dots
        yPosition = yPosition - constants.dist
        #X position reset to be back in the initial position (x coordinate
        #of the first dot)
        xPosition = -(constants.dist)

    return possibleMoves

##Determines who will take the first turn in the game
##Will be randomly generated if it's a new game and the player if it's a
##loaded game. The returned string is the name of the player who will take
##the first turn
def whoIsFirst():
    
    #Creates a list of possible choices for the first player random choice
    playerChoices = [playerName, "*Computer"]

    #If the game is a loaded game, the player is set to the first player          
    if isLoadedGame() == True:
        eventTurtle.up()
        eventTurtle.goto(-(2*constants.dist),(2*constants.dist))
        eventTurtle.write("Continuing from a saved game. " + playerName
                          + " will take this turn", align="left",
                          font=("Arial", 10, "bold"))
        time.sleep(1)
        eventTurtle.clear()
        
        return playerName

    #If the game is not a loaded game, the player is chosen randomly from
    #the playerChoices list
    elif isLoadedGame() == False:
        eventTurtle.up()
        eventTurtle.goto(-(2*constants.dist),(2*constants.dist))
        eventTurtle.write("Randomly selecting the player who will take"
                          " the first move...", align="left",
                          font=("Arial", 10, "bold"))
        time.sleep(1)
        eventTurtle.clear()
        # Chooses a random player to start the game, assigned to a variable
        #so that it can be passed on later to another function
        firstPlayer = random.choice(playerChoices)
        # Displays to the user if either they or the computer will make the
        #first move
        eventTurtle.write(firstPlayer + " will go first", align="left",
                          font=("Arial", 10, "bold"))
        time.sleep(1)
        eventTurtle.clear()

        return firstPlayer

#       |----        SAVING       ----|         #

##If the user clicks on the save button (turtle) during gameplay this
#function will write the current gameState to a txt file. The file contains
#the grid size on the first line, the player's name on the second line,
#and each row of the gameState on separate lines following those two items.
#Each square is separated by whitespace.
def saveGame():

    global gameState

    #Check to prohibit the user from saving if the game is over
    if checkEndGame() == True:
        eventTurtle.up()
        eventTurtle.goto(-(2*constants.dist),(2*constants.dist))
        eventTurtle.write("The game is over, you can't save the game!",
                          align="center", font=("Arial", 10, "bold"))
        time.sleep(2)
        eventTurtle.clear()

    #Check to prohibit the user from saving if a square has been completed,
    #but the initial has yet to be drawn. This would occur when the user
    #attempts to save just after a scoring move has been played, but the
    #game has yet to set the owner of the square or draw the initial,
    #and would cause the save file to be written erroneously 
    elif checkSquareInitial() == False:
        
        eventTurtle.up()
        eventTurtle.goto(-(constants.dist),(2*constants.dist))
        eventTurtle.write("You can't save the game right now!"
                          " Please try again in few moments.",
                          align="center", font=("Arial", 10, "bold"))
        time.sleep(2)
        eventTurtle.clear()

    #The constants.n_dots constant is written to the first line of the save
    #file, which represents the size of the grid. The playerName variable
    #is written to the second line of the save file, so that the user would
    #not have to re-enter their name upon loading a game. For each innermost
    #element of the gameState 3D list, each character is written to the file
    #and represents an individual square on the gameboard. A space is then
    #added to differentiate squares in the save file. Once an entire row of
    #squares is written to the file, a line break is used to differentiate
    #between each row.
    else:    
        saveFile = open("save.txt", "w")
        saveFile.write(str(constants.n_dots)+"\n")
        saveFile.write(playerName+"\n")
        squareList = []
        rowList = []
        
        for row in gameState:
            for square in row:
                for element in square:
                    saveFile.write(element)
                saveFile.write(" ")
            saveFile.write("\n")
        eventTurtle.up()
        eventTurtle.goto(-(2*constants.dist),(2*constants.dist))
        eventTurtle.write("The game has been saved!", align="center",
                          font=("Arial", 10, "bold"))
        time.sleep(1.3)
        eventTurtle.clear()

        saveFile.close()

#       |----        LOADING        ----|         #

##This function determines if the game is a loaded game, and if so,
##returns True
def isLoadedGame():

    #If any positions in the gameState are triggered, that means
    #that the game is not a blank state and therefore is a loaded game
    for row in gameState:
        for square in row:
            for element in square:
                if element != "!":
                    return True


    return False

##Re-draws the moves to the turtle screen upon the user choosing to
##load a previously saved game
def redrawMoves():
    
    global gameState
    global playerName
    
    turtle.tracer(False)
    
    trtredraw = turtle.Turtle()
    trtredraw.up()
    trtredraw.hideturtle()
    trtredraw.pensize(5)
    trtredraw.speed(0)

    #Calls for the initials to be re-drawn to the game screen      
    redrawInitials(trtredraw)

    #Utilizes a similar structure to the moveone function which draws
    #the moves during gameplay
    for row in range(constants.n_dots-1):
        
        for square in range(constants.n_dots-1):
            
            for element in range(1,5):
            
                if gameState[row][square][element] != "!":
                    
                    #Converts the move to turtle screen coordinates for
                    #use in positioning the turtle
                    move = convertToCoordinates([row, square, element])
                    
                    trtredraw.color("blue")
                    
                    if gameState[row][square][element] == "C":
                        trtredraw.color("red")

                    if move[1] == move[3]:
                        trtredraw.goto(move[0]+7,move[1])
                        trtredraw.down()
                        trtredraw.goto(move[2]-7,move[3])
                        trtredraw.up()

                    elif move[0] == move[2]:
                        trtredraw.goto(move[0],move[1]-7)
                        trtredraw.down()
                        trtredraw.goto(move[2],move[3]+7)
                        trtredraw.up()


    turtle.update()
    turtle.tracer(True)

##Re-draws the appropriate initials to the game screen upon the user
##choosing to load a previously saved game
def redrawInitials(trtredraw):
    
    global gameState

    #Checks through the gameState for any squares which have the owner
    #position triggered and draws the appropriate player's initial to
    #a position calculated using the position of that square in the
    #gameState 3D list
    for row in range(constants.n_dots-1):
        
        for square in range(constants.n_dots-1):
            
            if gameState[row][square][0] != "!":

                #Sets the position of the turtle to draw the player
                #initial in the correct location on the game screen
                yCoord = 5 - (constants.dist * row)
                xCoord = -35 + (constants.dist * square)
                trtredraw.goto(xCoord, yCoord)

                
                if gameState[row][square][0] == "C":
                    trtredraw.color("red")
                    trtredraw.write("*", font=("Arial", 27, "bold"))

                elif gameState[row][square][0] != "C":
                    trtredraw.color("blue")
                    trtredraw.write(playerName[0], font=("Arial", 27, "bold"))
                    

#       |----        COMPUTER MOVE GENERATION        ----|         #

##Initiates the generation of the computer's move and executes the functions
##neccesary to save the move and have it drawn onto the turtle screen.
#The final value returned to makeMove is a boolean value representing
##if the computer's move was a scoring move or not.
def computerMove():
    
    global gameState
    
    comp_name = "*Computer"
    trt.hideturtle()
    trt.up()
    trt.speed(1)

    #Set pen coloyr and size to red (the computer's colour)
    trt.color('red')
    trt.pensize(5)
    
    #The easyAI function is called to determine if there is a square
    #with only one move remaining, if not, False is returned and the
    #computer's move will be randomly generated
    if easyAI() ==  False:
        
        comp_move = computerMoveGenerator()

        #Converts the move to a format usable by setgameState
        convertedcomp_move = convertMove(comp_move)
        
        #Saves the computer's current move to the gameState
        setgameState(convertedcomp_move, comp_name)

        return moveone(comp_name, comp_move)

    #The easyAI function is called to determine if there is a square
    #with only one move remaining and if so, sets that move to be assigned
    #to the computer's move
    else:
        
        comp_move = easyAI()
        
        #Converts the move to a format usable by setgameState
        convertedcomp_move = convertMove(comp_move)

        #Saves the computer's current move to the gameState
        setgameState(convertedcomp_move, comp_name)

        return moveone(comp_name, comp_move)   

##This function checks to see if there are any squares with only one move
##left, and if so, returns that as the computer's move after converting
##it to coordinates on the game screen. If there is not such a move,
##the function returns False to the computerMove function
def easyAI():

    global gameState

    #Checks each square if it contains 2 "!", which indicates that there
    #is only one move left to complete that square. If there is only one
    #move left, the function determines the location of that move
    #and returns it to computerMove for use in the game
    for row in gameState:
        
        for square in row:
            
            if square.count("!") == 2:
                
                squareMoves = square[1:]
                return convertToCoordinates([gameState.index(row),
                                             row.index(square),
                                             (squareMoves.index("!")+1)])
            
    return False

## The function computerMoveGenerator randomly selects a move from a list
##of all possible move choices, checks to see if that chosen move has
##already been executed in the current game, and if not, returns that
#move as a string. 
def computerMoveGenerator():
            
    global listofMoves
        

    #Chooses a random selection from the list of possible moves in the
    #2D list listofMoves        
    comp_randmove = random.choice(listofMoves)  
    comp_randmove = comp_randmove[:4]       

    #Sends the randomly chosen move to index positions in the 3D gameState
    #list  
    convertedMove = convertMove(comp_randmove)

    #Loop which continues unless the chosen random move has not yet been
    #taken     
    while getgameState(convertedMove) == True:           
        comp_randmove = random.choice(listofMoves)
        comp_randmove = comp_randmove[:4]
        convertedMove = convertMove(comp_randmove)
             
    return comp_randmove            

#       |----        PLAYER MOVE INPUT        ----|         #

##Takes the clicks of the player on the game board for the player's move
##The coordinates clicked on the game screen are appended to the currentMove
##and then checked for validity before being returned as a list of four
##coordinates to makeMove
def turtlePlayerInput():

    global currentMove
    
    wn.onscreenclick(Click)
    
    #If currentMove is an empty list, that means no point on the screen
    #has been clicked yet, so until a first point is clicked and saved,
    #the program will continue to wait for input from the user.
    if currentMove != []:
        #Once currentMove contains 4 elements, that means the user has
        #clicked two points on the game grid, and the coordinates are
        #first validated before being returned to the makeMove function
        if len(currentMove) == 4:
            
            #Once two clicked points' coordinates have been saved, the
            #coordinates are checked for validity via the
            #validClickedCoordinates function, which will return True
            #if the points are in valid locations (i.e. on a dot on the
            #game grid).            
            if validClickedCoordinates() == True:
                screenClickTurtle.clear()
                return currentMove

            #If the user's choice of coordinates is invalid, the currentMove
            #will be cleared, an error message will be displayed on the
            #turtle screen, and the program will continue to wait for the
            #user to choose another two points on the game screen
            else:
                screenClickTurtle.clear()
                currentMove = []
                eventTurtle.goto((constants.dist),(2*constants.dist))
                eventTurtle.write("Error: Please choose valid coordinates"
                                  " or wait until it is your turn.",
                                  align="center", font=("Arial", 10, "bold"))
                time.sleep(1.5)
                eventTurtle.clear()
                turtlePlayerInput()

    return currentMove

##Sends the cursor turtle to the clicked point and then saves the
##coordinates of that clicked point to the global variable currentMove
##of list type
def Click(x,y):
    
   global currentMove

   #Displays an orange dot where the user has clicked as a means of
   #displaying to the user that their clicks are being registered and
   #providing visual feedback
   screenClickTurtle.goto(x, y)
   screenClickTurtle.down()
   screenClickTurtle.dot(10, "orange")   
   screenClickTurtle.up()
   
   
   currentMove.append(x)
   currentMove.append(y)

   #The coordinates of the clicked points are checked to see if they match
   #with the location of the save button on the screen and if so, clears
   #the currentMove so that no error message is displayed on the screen
   #indicating the player had chosen invalid coordinates after saving the
   #game.  
   x1 = int(currentMove[0])
   y1 = int(currentMove[1])

   if len(currentMove) == 4:
       x2 = int(currentMove[2])
       y2 = int(currentMove[3])

       if -160 <= x2 <= -82 and 287 <= y2 <= 332:
           screenClickTurtle.clear()
           screenClickTurtle.up()
           currentMove = []
           turtlePlayerInput()
   

   if -160 <= x1 <= -82 and 287 <= y1 <= 332:       
       screenClickTurtle.clear()
       screenClickTurtle.up()
       currentMove = []
       turtlePlayerInput() 
         
##Checks if the two clicked points (2 sets of coordinates) are within an
##acceptable range of a dot and returns True (if they are valid) and
##False (if they are not valid) 
def validClickedCoordinates():    

    global currentMove
    global listofMoves

    #Calls on the functions xList and yList which each generate a list
    #of valid x and y coordinates and their ranges appropriately
    validXList = xList()
    validYList = yList()
    
    validMove = []
    xcoordinate1Valid = False
    xcoordinate2Valid = False
    ycoordinate1Valid = False
    ycoordinate2Valid = False

    try:
        #Loop checks through each element in the generated list of valid
        #x coordinate ranges to see if the clicked point is within one of
        #the acceptable ranges. If it is, the coordinate is deemed valid
        #and the reference point (center of the dot) of the associated
        #clicked point is added to a temporary variable. If all coordinates
        #of the two clicked points are deemed valid this temporary variable
        #becomes the move which is sent to the rest of the program.
        for i in validXList:
            if currentMove[0] in i[1]:
                xcoordinate1Valid = True
                validMove.append(i[0])
                
                
            if currentMove[2] in i[1]:
                xcoordinate2Valid = True
                validMove.append(i[0])
                
        #See description of above loop      
        for i in validYList:
            if currentMove[1] in i[1]: 
                ycoordinate1Valid = True
                validMove.insert(1, i[0])
                
            if currentMove[3] in i[1]:
                ycoordinate2Valid = True
                validMove.append(i[0])
                
        #If all provided coordinates are valid, the temporary variable
        #validMove replaces the contents of currentMove.        
        if (xcoordinate1Valid == True and ycoordinate1Valid == True
            and xcoordinate2Valid == True and ycoordinate2Valid == True):

            
            #Two below if statements are used to re-order the coordinates
            #so that the topmost or leftmost dot is listed before the other
            #chosen coordinate. This is done to simplify and reduce coding
            #later in the program
            if ((validMove[:2] > validMove[2:]) and
               (validMove[1] == validMove[3])):
                validMove = validMove[2:] + validMove[:2]
                
            if ((validMove[:2] < validMove[2:]) and
               (validMove[0] == validMove[2])):
                validMove = validMove[2:] + validMove[:2]
                

            #If the move has valid coordinates and the move in the list
            #of all possible valid moves, the function returns true for
            #a valid move and sets the global variable currentMove to be
            #assigned to the value of the newly created local variable
            #validMove
            if validMove in listofMoves:
                currentMove = validMove
                return True
        else:
            
            return False

    except:
        return False

##Function creates and returns a list of all acceptable values for an
##x-coordinate calculated utilizing the constants dist and n_dots
def xList():
    
   xCorList = []
   xCor = -(constants.dist*2)
   
   for i in range(constants.n_dots):
      xCor = xCor + constants.dist
      #The -15 and +16 represent the acceptable range for a click to be
      #in (provides a "buffer" region around the dots)
      xRan = range(xCor - 15, xCor + 16)
      xCorList.append([xCor, xRan])
      
   return xCorList

##Function creates and returns a list of all acceptable values for a
##y-coordinate
def yList():
    
   yCorList = []
   yCor = (constants.dist*2)
   
   for i in range(constants.n_dots):
      yCor = yCor - constants.dist
      #The -15 and +16 represent the acceptable range for a click to be
      #in (provides a "buffer" region around the dots)
      yRan = range(yCor - 15, yCor + 16)
      yCorList.append([yCor, yRan])
      
   return yCorList

#       |----        MOVE CONVERSION        ----|         #

##This function works together with setgameState and getgameState to save
##or check a valid move to the gameState accordingly. It takes the submitted
##move as a parameter of list type with 4 elements: the x and y coordinates
##of the initial dot and the x and y coordinates of the second dot chosen.
##Depending on the location of the move on the game grid, a 2D list is
##returned, each element of the 2D list contains a list of the following
##items: (1) the index of the middle list in gameState which represents
##which row on the game grid the square which contains the move is located
##(2) the index of the innermost list in gameState which represents the
##position of the specific square in that row and (3) the index which
##represents the position of the move within the square. If the move would
##complete a line in more than one square, then a second set of 3 indices
##is appended to the 2D list.   
def convertMove(move):

    moveIndices = []

    #Initial x coordinate on the game grid
    xInitial = -(constants.dist)
    #Initial y coordinate on the game grid
    yInitial = constants.dist
      
    
    for squareRow in range(constants.n_dots-1):
        
        for squareColumn in range(constants.n_dots-1):
        
            #If the move is equivalent to any of the following moves
            #(representative of the current row and column on the game grid),
            #then a list of indices representing that move in terms of it's
            #position in the 3D list gameState is returned to setgameState
            if move == [xInitial, yInitial, (xInitial + constants.dist),
                        yInitial]:
                moveIndices.append([squareRow, squareColumn, 1])
            elif move == [xInitial + constants.dist, yInitial,
                          (xInitial + constants.dist),
                          (yInitial - constants.dist)]:
                moveIndices.append([squareRow, squareColumn, 2])
            elif move == [xInitial, (yInitial - constants.dist),
                          (xInitial + constants.dist),
                          (yInitial - constants.dist)]:
                moveIndices.append([squareRow, squareColumn, 3])
            elif move == [xInitial, yInitial, xInitial,
                          (yInitial - constants.dist)]:
                moveIndices.append([squareRow, squareColumn, 4])
       
    
            xInitial = xInitial + constants.dist
                    
        xInitial = -(constants.dist)
        yInitial = yInitial - constants.dist
            
    
    return moveIndices
        
##This function operates in the opposing direction to the function
##convertMove, and takes in 2D list of sets of indices which each represent
##a specific location in the gameState 3D list and converts them into
##turtle screen coordinates. This is utilized for loading the game and
##computer's AI function.
def convertToCoordinates(moveIndices):
    

    #Initial x coordinate on the game grid
    xInitial = -(constants.dist)
    #Initial y coordinate on the game grid
    yInitial = constants.dist

    index1 = 0
    index2 = 0

    #Utilitizing a nested loop, if a set of moveIndices matches
    #the indicated list of indices, then it corresponds to the
    #screen coordinates returned by the function
    for squareRows in range(constants.n_dots-1):

        for squareColumns in range(constants.n_dots-1):

            if moveIndices == [index1, index2, 1]:
                return [xInitial, yInitial, (xInitial + constants.dist),
                        yInitial]
            elif moveIndices == [index1, index2, 2]:
                return [xInitial + constants.dist, yInitial,
                        (xInitial + constants.dist),
                        (yInitial - constants.dist)]
            elif moveIndices == [index1, index2, 3]:
                return [xInitial, (yInitial - constants.dist),
                        (xInitial + constants.dist),
                        (yInitial - constants.dist)]
            elif moveIndices == [index1, index2, 4]:
                return [xInitial, yInitial, xInitial,
                        (yInitial - constants.dist)]

            index2 = index2 + 1
            xInitial = xInitial + constants.dist
        index2 = 0
        index1 = index1 + 1
        xInitial = -(constants.dist)
        yInitial = yInitial - constants.dist

#       |----        CHECKING/SAVING GAME STATE       ----|         #

##This function allows for the modification of the gameState through player
##or computer moves, or through the loading of an existing saved game.
##The function will take the player's (or computer's) current validated move
##as a list and the current player's identity as a string containing their
##name as parameters and save it to the gameState via manipulation of the
##3D list model.
def setgameState(location, name):
    
    global gameState
    
    
    #For every set of indices provided by the parameter location, that
    #position is used to alter the gameState appropriately.
    for setofIndices in location:
        
        #If it is the computers turn, the indices in moveIndices are used
        #to change the value of the specified position in gameState,
        #if it is not the computer's turn, and thus the player's turn,
        #then the same procedure is followed however depending on whose
        #turn it is alters the value that position is set to, i.e. "C" for
        #computer or "P" for player.
        if name == "*Computer":
            
            gameState[setofIndices[0]][setofIndices[1]][setofIndices[2]] = "C"
            
        else:
            
            gameState[setofIndices[0]][setofIndices[1]][setofIndices[2]] = "P"
            
##This function takes the submitted move as a parameter of list type with
##4 elements: the x and y coordinates of the initial dot and the x and y
##coordinates of the second dot chosen. Utilizing the determinePosition
##function, which returns a 2D list containing the positions that move
##would complete in the gameState 3D list, the function checks to see
##if that position in gameState has already been triggered, and if so
##returns True. If the move has not already been triggered
##False is returned.
def getgameState(move):
    
    global gameState
    
    moveFound = False
    
    #For every set of indices provided by determinePosition (i.e.
    #the number of positions triggered by the move in the gameState),
    #that position is used to check the gameState appropriately.
    for setofIndices in move:
               
        if (gameState[setofIndices[0]][setofIndices[1]][setofIndices[2]]) != "!":
            moveFound = True
        
    return moveFound  
    
##This function checks if the game has been completed by checking if
#all squares in the game have been completed and returns True if that
#is the case, and False if the game is not yet over.
def checkEndGame():

    global gameState

    #If a square in gameState is found to be untriggered (and thus,
    #not completed), the game will return False for the game being over,
    #as all squares will be completed prior to the end of the game.
    for index1 in range(constants.n_dots-1):
        for index2 in range(constants.n_dots-1):
            if (gameState[index1][index2][0] == "!"):
                return False

    return True

##This function determines if the current move has completed a square.
##It takes in two parameters, the move (as a list type) which will be
##converted with the convertMove function, and the current player's name.
##Using the position of the most recently completed move, the function checks
##that location to see if all moves in that square have been completed,
##and if so, requests setgameState to trigger the owner of the square to
##the current player, and then calls the function drawSquareInitial to draw
##the initial on the game screen.
def square(move, name):
    
    move = convertMove(move)
    
    global gameState
    squareCompleted = True
    playerScored = False

    
    for element in move:
                
        #Checks the square the current move is in, and looks through each
        #possible move for that square to see if they have all been completed.
        #If so, the owner of the square is triggered in gameState depending
        #on whose move it is and the initial is drawn on the game screen
        #within the appropriate square.
        for index in range(1, 5):
            
            if gameState[element[0]][element[1]][index] == "!":
                squareCompleted = False
                
        
        if squareCompleted == True:
            playerScored = True
            
            if name == "*Computer":
                
                setgameState([[element[0],element[1],0]], name)
                drawSquareInitial(element, name)
            else:
                
                setgameState([[element[0],element[1],0]], name)
                drawSquareInitial(element, name)
                
        squareCompleted = True

    #True or False is returned so that the main loop of this file will know
    #that the most recent move has scored a point and an additional move
    #for that player is warranted.
    return playerScored

##Utilized if a player clicks on the save button between the time a scoring
##move has been drawn and before the owner initial has been set and drawn onto
##the game screen. Erroneous coordinates are appended to the player's move,
##and thus, these coordinates are removed and then the gameState is checked
##to see if any squares have all moves completed but the owner initial has
##not been set. If that is the case, then the setting of the owner square
##and drawing of the initial is re-initiated.
def playerSquareCheck(player_move):

    ##Splices the players move if necessary due to the user clicking the
    ##save button in between a move being drawn
    ##The coordinate of the save button would be appended to the current
    ##move and cause errors later in the program, so if the player's move
    #contains more than 4 elements, the "extra" coordinates are cut off
    if len(player_move) > 4:
        player_move = player_move[:4]
                
    if checkSquareInitial() == False:
        playerScored = square(player_move, playerName)

#       |----        DRAWING MOVES        ----|         #

##This function draws the player/computer initial to the game screen when
##a square has been completed and displays an event message indicating
##a point has been scored. It takes in two parameters, the move
##(as a list type) which has already been converted with the convertMove
##function, and the current player's name. Using the position of the current
##move, the turtle which writes the initial is relocated to the appropriate
##square on the game screen.
def drawSquareInitial(move, name):

    pointTurtle = turtle.Turtle()
    
    #Sets the position of the turtle to draw the player initial in the
    #correct location on the game screen
    yCoord = 5 - (constants.dist * move[0])
    xCoord = -35 + (constants.dist * move[1])
    trt.goto(xCoord, yCoord)

    trt.color("blue")
    pointTurtle.color("blue")

    #Sets the colour of the turtles depending on whose initial is being drawn
    if name[0] == "*":
        trt.color("red")
        pointTurtle.color("red")


    trt.write(name[0], font=("Arial", 27, "bold"))

    #Sets up the turtle which displays a temporary on screen message to
    #indicate to the player if a point was scored
    
    pointTurtle.hideturtle()
    pointTurtle.up()
    pointTurtle.goto(-(2*constants.dist),(2*constants.dist))
        
    pointTurtle.write('+1 point!', align="center", font=("Arial", 10, "bold"))
    time.sleep(0.5)
    pointTurtle.clear()

##Utilizes the name and move parameters to the draw the provided move onto
##the game screen in the colour determined by the current player's name.
##The value returned is a boolean value indicating if the current move
##had scored a point or not (True if a point was scored and False if not).
def moveone(name, move):
    
    trt = turtle.Turtle()
    trt.color("blue")
    
    if name == "*Computer":
        trt.color("red")
        
    trt.pensize(5)
    trt.hideturtle()
    trt.up()
    trt.speed(1)

    #Utilizes the list of coordinates provided in the move parameter
    #to position the turtle and draw the appropriate line
    if move[1] == move[3]:
        trt.goto(move[0]+7,move[1])
        trt.down()
        trt.goto(move[2]-7,move[3])
        trt.up()

    elif move[0] == move[2]:
        trt.goto(move[0],move[1]-7)
        trt.down()
        trt.goto(move[2],move[3]+7)
        trt.up()
    
    
    #Displays an event message to the screen indicating which player
    #just made a move
    eventTurtle.up()
    eventTurtle.goto(-(2*constants.dist),(2*constants.dist))
    eventTurtle.write(name, align="center", font=("Arial", 10, "bold"))
    eventTurtle.goto(-(2*constants.dist),(2*constants.dist)-15)
    eventTurtle.write("has made a move!", align="center",
                      font=("Arial", 10, "bold"))
    time.sleep(1.2)
    eventTurtle.clear()

    return square(move, name)  
    
#       |----        END OF GAME        ----|         #

##This function displays messages to the user once the game has been
##completed including if the game was a tie, who won, and the number
##of points the player/computer had.
def endOfGame(playerName):
    
    time.sleep(1.5)
    trt.goto(-(2*constants.dist), 0) 

    #Calls the function which determines the score of the player/computer
    #and returns it as a list, with the player score in the first position
    #and the computer score in the second position
    scoreList = determineScore()
    
    comp_name = "*Computer"
    
    
    trt.write(('Game Over!\n\n'), font=("Bauhaus 93", 25, "bold"))
    trt.goto(-(3*constants.dist), -(0.5*constants.dist))

    #Depend on the values of the computer and player's points,
    #the game message is displayed on the game screen appropriately
    if scoreList[0] > scoreList[1]:
        trt.write(playerName + " has won the game with " +
                  scoreList[0] + " points!\n",
                  font=("Bauhaus 93", 15, "bold"))
        trt.write(comp_name + " had " + scoreList[1] +
                  " point(s)!", font=("Bauhaus 93", 15, "bold"))   
        time.sleep(0.3)
        
    elif scoreList[0] == scoreList[1]:
        trt.write('The game was a tie with ' + scoreList[0] +
                  " points!", font=("Bauhaus 93", 15, "bold"))
        time.sleep(0.3)
        
    else:
        trt.write(comp_name + " has won the game with " +
                  scoreList[1] + " points!\n",
                  font=("Bauhaus 93", 15, "bold"))
        trt.write(playerName + " had " + scoreList[0] +
                  " point(s)!", font=("Bauhaus 93", 15, "bold"))     
        time.sleep(0.3)

##This function looks through the gameState and counts the numbers
##of occurrences of the player or computer's initial in the owner location
##of each square and adds those values to respective variables.
##Those two variables are then added a list which is returned to
##endOfGame to display the end of game message
##including the winner and number of points of the winner.
def determineScore():
    
    global gameState
    player_points = 0
    comp_points = 0
    
    #Depending on the owner of a square in gameState points are added to
    #the appropriate player/computer variable
    for index1 in range(constants.n_dots-1):
        for index2 in range(constants.n_dots-1):
            if (gameState[index1][index2][0] == "C"):
                comp_points = comp_points + 1
            elif (gameState[index1][index2][0] == "P"):
                player_points = player_points + 1
                
    scoreList = [str(player_points), str(comp_points)]
    
    return scoreList

#       |----        MAIN FUNCTION       ----|         #

##The main function for this file which is called in the main program
##file to begin gameplay. Responsible for all the function calls which
##operate gameplay (choosing a move, computer move generation, etc.)
def makeMove():
           
    global gameState
    global playerName
    global listofMoves
    global currentMove

    eventTurtle.hideturtle()
    eventTurtle.up()
            
    #Sets the global variable gameState to the blank/fresh gameState
    #generated by the indicated function if gameState is an empty list.
    #If gameState is not an empty list that means a previously loaded
    #save file was loaded
    if gameState == []:                
        gameState = generateblankState()

    
    #List of all possible moves on the game grid (as calculated using
    #the constants dist and n_dots) for use in various functions
    listofMoves = possibleMoves()

    #Determines which player will take the first move
    firstPlayer = whoIsFirst()
     
    #If the computer was chosen to make the first move, this if statement
    #executes a call to the computerMove function
    if firstPlayer == "*Computer":
       
       computerMove()
       #Sets turtle colour back to blue for the player's first move
       trt.color('blue')

    #Main loop in which most of the game's moves are completed in
    #This loop continues until the end of the game is reached
    while checkEndGame() == False:
                      
        while True:
        
            #Allows for player input on the game screen
            player_move = turtlePlayerInput()
            #Converts the chosen player move to a set of indices representing
            #a position in the gameState 3D list for use in setgameState and
            #getgameState
            convertedplayer_move = convertMove(player_move)
            eventTurtle.clear()
        
            #If the move is not in the list of possible valid moves, the
            #loop continues from the beginning until the user chooses a
            #valid move
            if not player_move[:4] in listofMoves:
                               
                continue
                            
            else:

                #If the move chosen by the user has not already been
                #executed in the current/loaded game, the move is saved
                #to the gameState
                if getgameState(convertedplayer_move) == False:
                    setgameState(convertedplayer_move, playerName)
                    
                    break

                #If the move has already been executed in the current/loaded
                #game, an error message is displayed and the user is
                #re-prompted for input
                else:
                    currentMove = []
                    eventTurtle.goto(-(3*constants.dist),(2*constants.dist)-5)
                    eventTurtle.write("That move has already been taken."
                                      " Please choose another move.",
                                      align="left", font=("Arial", 10, "bold"))
                    time.sleep(1.5)
                    eventTurtle.clear()
                    continue

        #Executes the drawing of the move and the check to see if a square
        #has been completed. The value returned to playerScored is a boolean
        #value representing if the player's current move has scored a point
        #or not and is used to determine if the player should be allowed to
        #take an additional turn
        playerScored = moveone(playerName, player_move)

        playerSquareCheck(player_move)
        
        currentMove = []
        
        #If the end of the game has not been reached after the player takes
        #a turn and the player did NOT score a point, the computer will then
        #take it's turn
        if checkEndGame() == False and playerScored == False:
            playerScored = computerMove()
            currentMove = []
            #If the computer's last move scored a point, this loop will
            #keep repeating the computer's move until they no longer score
            #a point on that turn, after which it will continue to the
            #players turn
            while playerScored == True and checkEndGame() == False:
                playerScored = computerMove()

    time.sleep(0.1)
    
#       |----        END OF FILE      ----|         #

