def selectControls():
    '''
    displaying options for controls, after clicking button
    the option is highlighted and another click will select it
    
    then declaration of controls and updating parameter
    to know which control is chosen, it will be needed
    '''
    print("click the corresponding button to select controls")
    print("1 - matrix keyboard")
    print("2 - joystick")
    print("3 - mobile phone")
    x = input()
    if x == "1":
        print("selected keyboard")
    elif x == "2":    
        print("selected joystick")
    elif x == "3":    
        print("selected phone")
    else:
        print("invalid input")
    print("\n")