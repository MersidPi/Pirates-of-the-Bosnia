# idemo lagano oficijelni start - 21:15 1.6.2023.

''' this is just a frame, these functions will need lots of parameters
    and certainly better names than these xD
    execution flow of the game:
    intro, select controls, optional dark/light theme, arrange ships, battle, end screen, play again
'''

from sapica.intro import showIntro
from sapica.connection import connect
from sapica.controls import selectControls
#from theme import selectTheme
from sapica.arrange import arrangeShips
from sapica.battle import battle
from sapica.endScreen import endScreen
from time import sleep


playAgain = True
while playAgain == True:
    showIntro()
    connect()
    selectedControl = selectControls()
    print("Selected control: ", str(selectedControl))
    #selectTheme() # myb implement it the same way as selCtrl
    arrangeShips()
    thisPlayerVictory = battle()
    playAgain = endScreen(thisPlayerVictory) 
    print("playAgain is: " + str(playAgain))
print("ENDOFGAME")

