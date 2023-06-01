def arrangeShips():
    '''
    this function displays grid and available ships, player then selects a ship
    chooses its rotation - or | and then puts it on the grid, it needs a matrix
    and some logic implemented to disable overlap, impossible rotations (if its
    not possible to rotate a ship because theres no space) etc.
    it also needs function for key press (or joystick move, or key press on phone) reading
    and moving ship on screen according to that
    '''
    print("arranging ships...\npress any key to continue\n")
    x = input()