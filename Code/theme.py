def selectTheme():
    # here goes code with photoresistor to recommend theme, and then user chooses
    print("1 - dark")
    print("2 - light")
    x = input()
    if x == "1":
        print("selected dark")
    elif x == "2":    
        print("selected light")
    else:
        print("invalid input")
    print("\n")
