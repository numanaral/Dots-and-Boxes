#######Created by Team 84 - - - Dots & Boxes - - - CPSC 231
#######This is file which contains all of the constants used in the program

#       |----        START OF FILE     ----|         #

#       |----         IMPORTS         ----|       #

import turtle
import os
import platform
import ctypes


#       |----         GLOBAL VARIABLES        ----|      #

wn = turtle.Screen()
osPlatform = platform.system()
n_dots = 4
dist = 50
ang = 90

#Sets the window size differently depending on which OS the user is running
#the program on, this is to improve aesthetics for the user
if osPlatform == 'Windows':
   cmd_win_size = os.system("mode con cols=50 lines=28")
   user32 = ctypes.windll.user32
   screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
   w = (int(screensize[0]))
   h = (int(screensize[1]))
   canvas = wn.setup(w, h, 0, 0)
   
else:
   cmd_win_size = None
   canvas = wn.setup(800, 800)

#       |----        END OF FILE      ----|         #



