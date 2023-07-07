from battleships.intro import showIntro
showIntro()
from battleships.controls import selectControls
from battleships.arrange import arrangeShips
from battleships.battle import battle
from battleships.end import endScreen
from time import sleep

playAgain = True
while playAgain == True:
    
    # player B
    
    # getting input mode, choose with pico buttons
    inputMode = selectControls()
    
    # arrange ships into matrix
    matrix = arrangeShips(inputMode)
    
    # now battle starts
    battle(matrix, inputMode)
    
    # prompt for playing again
    playAgain = endScreen(inputMode)
