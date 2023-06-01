from time import sleep

def battle():
    '''
    function that will be run while players are attacking each other
    player that goes first can be randomly determined, for example
    picos send random number on topic and whose is bigger, goes first
    attack will have time limit, which will be shown on 8 LEDs
    while opponent is attacking LEDs will "run" back and forth
    aim function is needed here, like in arrangeShips
    matrix will change values
    all of this will be sent on topic so that both players can see
    whats going on (not being able to see opponents ships ofc xD)
    when all ships of one player are
    destroyed, game will end, loop and this function will end
    
    '''
    print("player 1 attacks")
    sleep(1)
    print("miss")
    print("player 2 attacks")
    sleep(1)
    print("miss")
    print("player 2 attacks")
    sleep(1)
    print("hit!\ngame over\n")
    