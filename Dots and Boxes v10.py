# ############################################# #
#												#
# 	Game		: Dots & Boxes					#
# 	Class		: CPSC 231 (Python)				#
# 	Created by	: Team 84						#
#												#
# ============================================= #
#												#
# 	Members:									#
# 	# Ahmet Numan Aral							#
# 	# Abhinav Dhungel 							#
# 	# Kaylee Stelter							#
# 	# Shivani Thakkar							#
# 	# Fungai Mawoyo								#
#												#
# ============================================= #
#												#
# 	This is the main file of the program		#
# 	-> initiates the game						#
#												#
# ############################################# #

#       |----         OVERVIEW OF FILE LAYOUT         ----|       

#                       IMPORTS           
#                       GLOBAL VARIABLES        
#                       SET-UP       
#                       TITLE SCREEN & INSTRUCTIONS             
#                       LOADING/STARTING NEW GAME                 
#                       DRAWING THE GAME BOARD & BUTTONS           
#                       MAIN FUNCTION AND END OF GAME              
#                       MAIN FUNCTION CALL    



#       |----        START OF FILE     ----|         #

#       |----         IMPORTS         ----|       #

import turtle
import constants 
import os 
import sys 
import time 
import random 
import platform 
import makeMove 

#       |----         GLOBAL VARIABLES        ----|      #

wn = turtle.Screen()
trt = turtle.Turtle()


#       |----        SET-UP        ----|         #

##Sets the sizes of the command window canvas window via reference of the
##constants file
def window():
    
    constants.cmd_win_size
    constants.canvas


##For improved aesthetics, checks to see what OS the user is running the
##program on and changes the font accordingly
def platform_font(text):
    """Checks operating system of end user and changes fonts as appropriate
       for ideal display purposes"""
    
    osPlatform = platform.system()
    
    if osPlatform == 'Windows':
        trt.write(text, font=("Bauhaus 93", 27, "bold"))
        
    else:
        trt.write(text, font=("Arial", 27, "bold"))



#       |----        TITLE SCREEN & INSTRUCTIONS      ----|         #

##Stamps a random-colored line with the shape provided as a parameter with
##a turtle
def drawborder(shape):
    """This function draws a random colored-border with a given shape"""
    
    trt.shape(shape)
    
    for i in range(0,11):
       trt.color(random.random(),random.random(), random.random())  
       trt.forward(25)
       trt.stamp()
       
##Draws the separating columns of ascii characters with a turtle for on-screen
##aesthetics on the title screen
def separator():
    
    for i in range(5):
        trt.write("║")
        trt.fd(13)

##Draws the square and circle border around the game title      
def drawLogoBorder():
    
    #A square and circular rainbow border is drawn around the text area with
    #the main turtle by calling the drawborder function
    for i in range(3):
        trt.goto(-152, 100)
        drawborder("circle")

        trt.goto(-152, -65)
        drawborder("square")

    
    trt.color("black")
    #Border is drawn around game title
    trt.goto(-152,54)
    trt.write('╔' + 11 * '═' + '╦' + 8 * '═' + '╦' + 15 * '═' + '╗')

    trt.goto(-152,-37)
    trt.write('╚' + 11 * '═' + '╩' + 8 * '═' + '╩' + 15 * '═' + '╝\n')

##Adds the title of the game to the title screen using the main turtle
def logoText():
    
    #Adds game title and parts of border - - Calls on the function
    #platform_font to alter fonts based on end user's operating system
    #Section for "Dots"
    platform_font('Dots')
    time.sleep(.7)
    trt.goto(16,41)
    separator()
    time.sleep(.1)               
    trt.goto(-50,0)
    
    #Section for "and"
    platform_font('and')
    time.sleep(.5)
    trt.goto(144,41)
    separator()
    time.sleep(.1)
    trt.goto(25,0)
    
    #Section for "Boxes"
    platform_font('Boxes')
    time.sleep(.5)
    trt.goto(78,-11)
    
    #Adds author credit to title screen
    trt.write("v.Team84", font=("AR DESTINE", 10, "normal"))
    time.sleep(3)

    

##Main function for the creation of opening game title screen and aesthetics
##Calls on the above functions which are responsible for displaying the opening
##title screen & instructions to the user
def welcome():

    #Sets up the turtle and command window sizes
    window()    
    
    trt.speed(0)
    trt.up()
    trt.hideturtle()   

    #Draws the border around the game title
    drawLogoBorder()
    
    time.sleep(.5)
    trt.goto(-152,41)
    trt.right(90)

    #Separator is called to draw the columns of ascii characters for aesthetics
    #on the title screen
    separator()
    time.sleep(.7)
    trt.goto(-56,41)
    separator()
    time.sleep(.1)
    trt.goto(-138,0)

    #Writes the game title to the title screen
    logoText()

##Displays the instructions for the game on the game screen to the user
def instrText():

    trt.write(
        "       " + "╔" + ' ' + 14 * '═ ' + '╗' + '\n'
        "       " + "         The rules of the game       \n"
        "       " + "╚" + ' ' + 14 * '═ ' + '╝\n', align="center",
        font=("Arial", 14, "normal"))


    trt.color("black")
    trt.goto(15,-250)
    trt.write(    
    "=> The player which gets to make a play first will be\n"
    "chosen randomly.\n\n"

    "=> An empty grid of dots will be also be randomly generated.\n\n"

    "=> The player and computer will take turns by drawing\n"
    "a horizontal or vertical line between two adjacent dots on the\n"
    "grid.\n\n"

    "=> A move is executed by clicking on the dots which would connect\n"
    "to form the desired line. If clicks are made while a message is\n"
    "displayed on-screen, they may not be registered. Please try your\n"
    "move again if this occurs.\n\n"

    "=> A player who completes the fourth side of a 1x1\n"
    "square will have claimed that square, earn one point,\n"
    "and take another turn.\n\n"

    "=> The player can save game by clicking on the\n"
    "save button on the game window.\n\n"

    "=> The game ends when neither player can add a line\n"
    "to the grid.\n\n"

    "=> When the game has ended, the player with the most\n"
    "completed squares is declared the winner.\n", align="center",
    font=("Arial", 12, "normal"))

##Is called via a click on the load button (turtle) and executes the
##function which loads a new game
def load(x,y):
    turtle.clearscreen()
    #Creates new clickable buttons for the user upon clearing the screen
    createBtns()[1].ht()
    return loadGame()

##Is called via a click on the new button (turtle) and executes the function
##which begins a new game
def new1(x,y):
    turtle.clearscreen()
    #Creates new clickable buttons for the user upon clearing the screen
    createBtns()[0].ht()
    return newGame()

##Is called via a click on the exit button (turtle) and executes an exit from
##the program/terminal
def exitG(x,y):
    os._exit(0)
    
    
##Function for Game Instructions, Strategies, Any other Pre-game information
##to be displayed to the user, etc.
def instructions():

    #Hides the turtle animations until they are complete, so that the user will
    #not see the intermediate animations. See turtle.update() and
    #turtle.tracer(True) below, which updates the turtle screen with all
    ##completed animations and allows animations to be visible again.
    turtle.tracer(False)
    
    trt.up()
    trt.ht()
    
    #Clears the screen and displays the instructions to the game screen
    trt.color("cyan")
    trt.clear()
    trt.goto(-5,260)
    instrText()

    #Creates clickable buttons for the user for various options (new, load, exit)
    btnsSetup()

    
    turtle.update()
    turtle.tracer(True)

    turtle.done()  

##Creates the clickable buttons (turtles) for the user (new, load, exit)
##Returns a list of turtle names and sets their speed and other settings
def createBtns():
    
    trtn = turtle.Turtle()
    trtl = turtle.Turtle()
    trtx = turtle.Turtle()

    trtList = [trtn, trtl, trtx]
    
    for obj in trtList:
        obj.speed(0)
        obj.up()
        obj.ht()

    return trtList

##Creates the clickable buttons for the user (new, load, exit)
##Utilizes the createBtns function to create three turtles, which are aligned
##appropriately on the screen and associated with their appropriate function
##call
def btnsSetup():
    trtn = createBtns()[0]
    trtl = createBtns()[1]
    trtx = createBtns()[2]

    #Sets the corresponding text above the button and turtle shape, size, and
    #colour appropriately
    buttonsTextSettings(trtn, -120, 0)
    buttonsTextSettings(trtl, 0, 1)
    buttonsTextSettings(trtx, 120, 2)

    trtl.onclick(load)
    trtn.onclick(new1)
    trtx.onclick(exitG)

    

##Adds the text above the clickable buttons for the user (new, load, exit)
##as well as sets the shape, color, and size of the buttons
def buttonsTextSettings(trt, x, counter):
    
    trt.color('black')
    trt.goto(x, -320)

    #The parameter counter is used to determine which button is being called
    #and to use that counter to set the text above the button appropriately
    if counter == 0:
        trt.write("  new  \n", align="center", font=("courier", 14, "normal"))
    elif counter == 1:
        trt.write("  load  \n", align="center", font=("courier", 14, "normal"))
    else:
        trt.write("  exit  \n", align="center", font=("courier", 14, "normal"))
    
    
    trt.color('black', 'cyan')
    trt.shape('square')
    trt.shapesize(2.2,3.9)
    trt.st()
        


#       |----        LOADING/STARTING NEW GAME       ----|         #        

##Function which is called when the user clicks on the "load game" button which
##is displayed on the game screen
def loadGame():

    #If a proper save file exists, the first line of the file is set to the grid
    #size (constants.n_dots) which is used to draw the grid and various other
    #checks in the main program file and the makeMove file. The second line of
    #the file is assigned to the player's name global variable in the makeMove
    #file
    try:
        saveFile = open("save.txt", "r")

        #Sets constants.n_dots to the value in the first line of the saveFile
        #and then skips to the next line
        constants.n_dots = int(saveFile.readline())
        #Sets the global variable playerName in the makeMove file to the second
        #line of the save file
        makeMove.playerName = saveFile.readline()
        #The player's name is spliced to remove the line break "\n" that occurs
        #at the end of the string due the file format of the save file
        makeMove.playerName = makeMove.playerName[0:-1]
        
        saveFile.close()
        
    #If there is no save file found, an error message is displayed on the turtle
    #screen and the instructions page is reprompted and the user may choose a
    #different option (new or exit)
    except:
        makeMove.eventTurtle.up()
        makeMove.eventTurtle.goto(-(2*constants.dist),(2*constants.dist)-15)
        makeMove.eventTurtle.write("There is no saved game to load",
                                   align="center", font=("Arial", 20, "bold"))
        time.sleep(1)
        makeMove.eventTurtle.clear()
        instructions()

    #The game grid is drawn onto the game screen utilizing the save file's
    #designated grid size
    gridDraw()

    #Finishes the loading of the save file including re-establishing the existing
    #game state and re-drawing all completed moves to the turtle/game screen
    fullyLoad()
        
    #Calls for the game to begin via the makeMove file 
    makeMove.makeMove()

    #Clears the screen after the game is complete
    wn.clear()

    #Executes the end of game message (whether the player/computer won and the
    #score of each player)
    makeMove.endOfGame(makeMove.playerName)
    time.sleep(2)

    #Creates and displays clickable buttons so that the user may start a new
    #game, load an existing game, or exit the game upon finishing a game
    endOptions()

##Completes the loading of the save file including re-estabilishing the existing
##game state and re-drawing all completed moves to the turtle/game screen
def fullyLoad():
    
    
    afile = open("save.txt", "r")
    #Skips the lines of the file which correspond to the grid size and player
    #name
    afile.readline()
    afile.readline()
    
    gameList = []
    rowList = []
    squareList = []

    #The game state is re-established by reading each line of the file,
    #splitting each line (each square is delimited by whitespace), and then
    #adding each character of a square to a sublist. That sublist is then
    #appended to another list which represents an entire row of squares.
    #Then the list containing an entire row of squares is appended to the
    #main list which becomes the game state. This is repeated as necessary
    #depending on the size of the file.
    for aline in afile:            
        row = aline.split()            
        for square in row:                
            for element in square:                    
                squareList.append(element)                    
            rowList.append(squareList)
            squareList = []                
        gameList.append(rowList)
        rowList = []
        
    makeMove.gameState = gameList
    
    #The moves now present in the gameState global variable are redrawn to
    #the turtle/game screen
    makeMove.redrawMoves()          
    afile.close()

##Function which is called when the user clicks on the "new game" button
##which is displayed on the game screen
def newGame():
    
    trt.clear()
    makeMove.gameState = []

    #Prompts for the user to enter their name and checks it for validity
    #before continuing
    while True:
        player_name = constants.wn.textinput("Name","Please enter your name")

        if player_name == None:
            continue
        if not player_name.isalpha():
            continue
        
        else:
            break

    makeMove.playerName = player_name
    
    #Continues the calls to create a new game
    newGame2()

##Sets the random grid size for the game screen, draws the board, and starts
##the game
def newGame2():
    
    constants.n_dots = random.randrange(3,11)      
      
    gridDraw()
 
    makeMove.makeMove()
          
    wn.clear()
    trt.down()
    makeMove.endOfGame(makeMove.playerName)
    time.sleep(1)
    endOptions()



#       |----        DRAWING THE GAME BOARD & BUTTONS       ----|

##Draws the dashed lines between the dots on the game board 
def gridDrawLines(x,y):
    
    trt.goto(x,y)

    
    for i in range(constants.n_dots):
        for i in range(constants.n_dots-1):
            for i in range(constants.n_dots):
                trt.down()
                trt.fd(constants.dist/((2*constants.n_dots)+1))
                trt.up()
                trt.fd(constants.dist/((2*constants.n_dots)+1))
            trt.fd(constants.dist/((2*constants.n_dots)+1))
        trt.backward((constants.n_dots-1) * constants.dist)      
        trt.right(constants.ang)                    
        trt.forward(constants.dist)                
        trt.left(constants.ang)
        
##Labels the game board with letters and numbers to aid the user in selecting
#moves
def labelGrid():
    
    #Letters for the game board        
    trt.goto(-52,75)
    trt.left(90)

    #Writes the letters for the game board, starting with A and continuing
    #based on the number of dots on the grid
    for letter in map(chr, range(65,(65+constants.n_dots))): 
        trt.write(letter)
        trt.fd(constants.dist)

    
    trt.goto(-80,43)
    trt.right(90)
    
    #Write the numbers for the game board, starting with 1 and continuing
    #based on the number of dots on the grid
    for i in range(1,(constants.n_dots+1)):
        trt.write(i)
        trt.fd(constants.dist)

##Creates the dots on the game board on the turtle screen, utilizing the
##constants n_dots for the number of dots (and therefore grid size) and dist,
##which represents the distance between dots on the game screen
def gridStamp():
    
    #Returns turtle back to original position and then places it so the game
    #board is drawn in the center. The home code is necessary to revert all
    #the angle movement codes
    trt.home()
    trt.goto(-50,50)
    trt.shape('circle')
    trt.shapesize(0.5)
    
    #Create two "for in" loops: "j" for the horizontal movement and "i" for
    #the vertical movement, each loop places dots in a horizontal line and
    #gets the turtle to second line facing east
    for i in range(constants.n_dots):
        for j in range(constants.n_dots):
            trt.stamp()                                      
            trt.forward(constants.dist)                      
        trt.backward(constants.n_dots * constants.dist)      
        trt.right(constants.ang)                    
        trt.forward(constants.dist)                          
        trt.left(constants.ang)

##Main calls to draw the game board, including the numbers and letters around
##the game board, the dots, and the dashed lines between the dots
def gridDraw():   


    turtle.clearscreen()
    
    #Displays game title on the game board
    wn.title("Dots and Boxes")
    trt.goto(-120, 240)
    trt.write("Dots and Boxes", font=("Bauhaus 93", 27, "bold"))

    #Adds letters and numbers to the game board to aid the user in selecting
    #moves on the game board
    labelGrid()
    
    #Hides the turtle animations until all animations have been completed,
    #updated and made visible via the turtle.update() and turtle.tracer(True)
    #calls below. This is an aesthetic addition so that the user doesn't see
    #the intermediate animations
    turtle.tracer(False)

    #Adds the dots to the game board
    gridStamp()

    #Draws the dashed lines between the dots on the game board
    gridDrawLines(-50,50)
    trt.right(constants.ang)
    gridDrawLines(-50+(constants.n_dots-1)*constants.dist,50)
    trt.home()

    turtle.update()
    turtle.tracer(True)

    
    inGameBtns()

##Creates the clickable buttons (turtles) for the user (save, exit, menu) that
##are displayed during gameplay
def inGameBtns():              

    trts = turtle.Turtle()
    trtx = turtle.Turtle()
    trtm = turtle.Turtle()

    trtList = [trts, trtx, trtm]

    for obj in trtList:
        obj.speed(0)
        obj.up()
        obj.ht()

    #Sets the corresponding text above the button and turtle shape, size,
    #and colour appropriately
    inGameButtonsTextSettings(trts, -120, 0)
    inGameButtonsTextSettings(trtx, 120, 1)
    inGameButtonsTextSettings(trtm, 0, 2)

    trts.onclick(saveG)
    trtx.onclick(exitG)
    trtm.onclick(menu)

##Writes the text and sets the shape, color, and size for the clickable
##buttons that are displayed during gameplay to the user
def inGameButtonsTextSettings(trt, x, counter):
    
    trt.color('black')
    trt.goto(x, 320)

    #The parameter counter is used to determine which button is being called
    #and to use that counter to set the text above the button appropriately
    if counter == 0:
        trt.write("  save  \n", align="center", font=("courier", 14, "normal"))
    elif counter == 1:
        trt.write("  exit  \n", align="center", font=("courier", 14, "normal"))
    else:
        trt.write("  menu  \n", align="center", font=("courier", 14, "normal"))
    
    
    trt.color('black', 'cyan')
    trt.goto(x-1, 310)
    trt.shape('square')
    trt.shapesize(2.2,3.9)
    trt.st()
        
##Called when the user clicks the "save" button
##Function calls the saveGame function within the makeMove file
def saveG(x,y):
    
    return makeMove.saveGame()

##Called when the user clicks the "menu" button
##Function clears the screen and returns to the instruction screen where the
##user can choose a different option for the game
def menu(x,y):
    
    turtle.clearscreen()
    trt.right(90)
    instructions()
        

    



#       |----        MAIN FUNCTION AND END OF GAME      ----|         #



##Sets the settings for the clickable buttons after the game is over
#(shape, color, size, text above)
def endBtnsAlign(trt, x, counter):
    
    trt.color('black')
    trt.goto(x, -320)

    #The parameter counter is used to determine which button is being called
    #and to use that counter to set the text above the button appropriately
    if counter == 0:
        trt.write("  new  \n", align="center", font=("courier", 14, "normal"))
    elif counter == 1:
        trt.write("  menu  \n", align="center", font=("courier", 14, "normal"))
    else:
        trt.write("  exit  \n", align="center", font=("courier", 14, "normal"))
    
    trt.color("black", "cyan")
    trt.goto(x-1,-326)
    trt.shape('square')
    trt.shapesize(2.2,3.9)
    trt.st()

##Creates the clickable buttons (turtles) for the user (new, load, exit)
##Returns a list of turtle names and sets their speed and other settings 
def endBtns():
    
    trtn = turtle.Turtle()
    trtm = turtle.Turtle()
    trtx = turtle.Turtle()

    trtList = [trtn, trtm, trtx]

    for obj in trtList:
        obj.speed(0)
        obj.up()
        obj.ht()

    return trtList
    

##Creates the clickable buttons for the user (new, load, exit)
##Utilizes the endBtns function to create three turtles, which are aligned
##appropriately on the screen and associated with their appropriate function
##call
def endOptions():
    
    trtn = endBtns()[0]
    trtm = endBtns()[1]
    trtx = endBtns()[2]

    endBtnsAlign(trtn, -120, 0)
    endBtnsAlign(trtm, 0, 1)
    endBtnsAlign(trtx, 120, 2)

    trtn.onclick(new2)
    trtm.onclick(menu)
    trtx.onclick(exitG)
    turtle.done()   
    
##Function which is called when the user clicks on the "new game" button which
##is displayed on the game screen. This new game is called only when the user
##has already completed a game, whereas the newGame function is called when the
##user has started a fresh game or returned to the menu    
def new2(x,y):
    
    turtle.clearscreen()
    #Hides the turtle representing the "new" button
    endBtns()[0].ht()
    trt.right(90)
    trt.clear()
    makeMove.gameState = []
    return newGame2()



##Main function for this file
##Calls upon the welcome and instructions functions which initiate and run the
##entire game
def playGame():
    welcome()
    instructions()


#       |----        MAIN FUNCTION CALL    ----|         #

##Call to main function
playGame()

#       |----        END OF FILE      ----|         #
