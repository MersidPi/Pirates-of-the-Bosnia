from battleships.ili934xnew import ILI9341, color565
from battleships.display import display, refreshDisplay

def drawLineAlongY(positionX, startY, endY, col=color565(255, 255, 255)):
    if (endY < startY):
        pom = endY
        endY = startY
        startY = pom
    y = startY
    while y <= endY:
        display.pixel(positionX, y, col)
        y += 1
        
def drawLineAlongX(pozicija_y, x1, x2, col=color565(255, 255, 255)):
    if (x2 < x1):
        pom = x2
        x2 = x1
        x1 = pom
    i = x1
    while i <= x2:
        display.pixel(i, pozicija_y, col)
        i += 1

def drawGrid(startX, startY, cellSize, gridSize, color = color565(255, 255, 255)):
    x = startX
    for i in range(gridSize + 1):
        drawLineAlongY(x, startY, startY + cellSize * gridSize, color)
        x += cellSize
    y = startY
    for i in range(gridSize + 1):
        drawLineAlongX(y, startX, startX + cellSize * gridSize, color)
        y += cellSize
        