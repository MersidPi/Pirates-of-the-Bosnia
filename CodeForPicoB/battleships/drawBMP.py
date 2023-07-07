from battleships.ili934xnew import ILI9341, color565
from battleships.display import display, refreshDisplay

# Učitavanje slika iz BMP fajla
empty = open('battleships/bitmaps/empty.bmp', 'rb')
ship = open('battleships/bitmaps/ship.bmp', 'rb')
shipHit = open('battleships/bitmaps/skull.bmp', 'rb')
miss = open('battleships/bitmaps/testMiss.bmp', 'rb') #test miss
aim = open('battleships/bitmaps/aim.bmp', 'rb')
heart = open('battleships/bitmaps/heart2.bmp', 'rb')
heartDelete = open('battleships/bitmaps/heartDelete.bmp', 'rb')
heartMy = open('battleships/bitmaps/heartMy2.bmp', 'rb')
aimShip = open('battleships/bitmaps/aimShip.bmp', 'rb')
aimSkull = open('battleships/bitmaps/aimSkull.bmp', 'rb')
aimTestMiss = open('battleships/bitmaps/aimTestMiss.bmp', 'rb')
etf = open('battleships/bitmaps/etf.bmp', 'rb')
copyright = open('battleships/bitmaps/copyright.bmp', 'rb')
logo = open('battleships/bitmaps/piratesLogo_120x87.bmp', 'rb')


def drawBMP(offset_y, offset_x, value):
    f = empty
    if value == 1:
        f = ship
    elif value == 2:
        f = shipHit
    elif value == 3:
        f = miss
    elif value == "aim":
        f = aim
    elif value == "heart":
        f = heart
    elif value == "heartDelete":
        f = heartDelete
    elif value == "heartMy":
        f = heartMy
    elif value == "aimShip":
        f = aimShip
    elif value == "aimSkull":
        f = aimSkull
    elif value == "aimTestMiss":
        f = aimTestMiss
    elif value == "etf":
        f = etf
    elif value == "copyright":
        f = copyright
    elif value == "logo":
        f = logo
        
    # drawing picture on display
    if f.read(2) == b'BM':  #header
        dummy = f.read(8) #file size(4), creator bytes(4)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
            depth = int.from_bytes(f.read(2), 'little')
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                w, h = width, height
                for row in range(h):
                    if flip:
                        pos = offset + (height - 1 - row) * rowsize
                    else:
                        pos = offset + row * rowsize
                    if f.tell() != pos:
                        dummy = f.seek(pos)
                    for col in range(w):
                        bgr = f.read(3)
                        display.pixel(offset_y+col,offset_x+row,color565(bgr[2],bgr[1],bgr[0]))
                f.seek(0,0)

