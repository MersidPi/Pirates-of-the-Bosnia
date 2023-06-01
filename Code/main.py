# idemo lagano oficijelni start - 21:15 1.6.2023.

''' this is just a frame, these functions will need lots of parameters
    and certainly better names than these xD
    execution flow of the game:
    intro, select controls, optional dark/light theme, arrange ships, battle, end screen, play again
'''

from intro import intro
from connection import connect
from controls import selectControls
from theme import selectTheme
from arrange import arrangeShips
from battle import battle
from endScreen import endScreen

#while playAgain == True:
intro()
connect()
selectControls()
selectTheme()
arrangeShips()
battle()
endScreen()

