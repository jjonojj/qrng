import random
import pygame
import ctypes
import math as m

"""
qr-code generator 
jonas piechl

wikipedia:
Wegen der vielseitigen Anwendungsmöglichkeiten und der geringen Größe von QR-Codes wurde Wert darauf gelegt, dass der codierte Text nur wenig Platz benötigt. Abhängig davon, welche Zeichen im Text vorkommen, kann man den Text mit unterschiedlichen Zeichensätzen codieren:

Wenn der Text nur aus Ziffern (0–9) besteht, verbraucht er am wenigsten Platz. In diesem Fall werden jeweils drei Ziffern zusammengefasst und als 10-Bit-Einheit gespeichert.
Wenn der Text nur aus Ziffern (0–9), Großbuchstaben (A–Z) und neun weiteren Sonderzeichen (Leerzeichen, $, %, *, +, −, /, ., :) besteht, werden jeweils zwei Zeichen zusammengefasst und als 11-Bit-Einheit gespeichert.
Wenn der Text nur aus Zeichen besteht, die in ISO-8859-1 vorkommen (das sind unter anderem Groß- und Kleinbuchstaben, Ziffern, viele Satzzeichen und kombinierte Buchstaben für den westeuropäischen Sprachraum), wird jedes Zeichen als 8-Bit-Einheit gespeichert.
Wenn der Text nur aus Kanji besteht, wird jedes Zeichen als 13-Bit-Einheit gespeichert.
In den restlichen Fällen wird es komplizierter; dann wird die ECI-Zeichencodierung verwendet.

wir nutzen iso-8859-1

Nachdem der passende Zeichensatz bestimmt ist, werden die folgenden Informationen in die Bitfolge geschrieben:

die Kennnummer des Zeichensatzes ### ( 0100 für iso-8859-1 )
die Anzahl der Zeichen, die der Text hat ### ( bin(len(wort)) )
der Text selbst ### (  for loop and ord ig? )
die Ende-Kennung; sie ist immer 0000
die resultierende Bitfolge in 8-Bit-Einheiten zerlegen; am Ende ggfs. mit Null-Bits auffüllen
Auffüllen bis zur Datenkapazität der QR-Code-Version mit den Codewörtern 11101100 und 00010001 abwechselnd

"""

pygame.init()

size = 33

curqr = ""

ws = size * 10 + 40
w, h = ws, ws
qrcol = (0, 0, 0)
backg = (220, 220, 255)
checker = (255, 255, 255)
checker2 = (200, 200, 200)

test = (100, 100, 100)


def gen(word):
    enstr = ""  #binary string
    enstr += "0100"  #iso-8859-1
    enstr += bin(len(word))[2:]  #length of word
    for i in word:
        enstr += bin(ord(i))[2:]  #ascii value of char
    enstr += "0000"  #end
    while len(enstr)%8 != 0:
        enstr += "0"
    return enstr

window = pygame.display.set_mode((w, h), pygame.RESIZABLE)
pygame.display.set_caption("random qr codes")

ctypes.windll.dwmapi.DwmSetWindowAttribute(pygame.display.get_wm_info()['window'], 20, ctypes.byref(ctypes.c_int(1)), 4)

print(len(gen("Mächenbuch")))

def rngen():
    ret = ""
    for y in range(size):
        for x in range(size):
            ret += str(random.randint(0, 1))
    return ret

def bg():
    for y in range(size * 2):
        for x in range(size * 2):
            if (x % 2 == 0 and y % 2 == 0 or x % 2 != 0 and y % 2 != 0):
                pygame.draw.rect(window, checker, (x*10, y*10, 10, 10))

def render(btstr):
    for y in range(size):
        for x in range(size):
            """
            these are the whole template draw patterns for a v4 qr code. i sat 4 hours on this and it was pure pain.
            wikipedia link for nerds:
            https://de.wikipedia.org/wiki/Datei:QR_Code_V4_structure_example.svg
            
            """
            # strange cubes
            if ((x < 7 and y < 7) and not ((x == 1 or x == 5) and not (y == 0 or y == 6)) and not ((y == 1 or y == 5) and not (x == 0 or x == 6))   or   (x > size - 8 and y < 7)  and not ((x == size - 2 or x == size - 6) and not (y == 0 or y == 6)) and not ((y == 1 or y == 5) and not (x == size - 1 or x == size - 7))   or   (x < 7 and y > size - 8) and not ((x == 1 or x == 5) and not (y == size - 1 or y == size - 7)) and not ((y == size - 2 or y == size - 6) and not (x == 0 or x == 6))):
                pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if ((y == size - 1 or y == size - 3 or y == size - 4 or y == size - 5 or y == size - 6 or y == size - 8) and x == 8):
                pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if ((x < size - 4 and x > size - 10) and (y < size - 4 and y > size - 10) and ((x != size - 6 and x != size - 8) or (y != size - 6 and y != size - 8)) and not (x == size - 8 and y == size - 7) and not (x == size - 7 and y == size - 8) and not (x == size - 6 and y == size - 7) and not (x == size - 7 and y == size - 6)):
                pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))

            # sync lines
            if (x == 6 and y % 2 == 0 and y > 9 and y < size - 8):
                pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if (y == 6 and x % 2 == 0 and x > 9 and x < size - 8):
                pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            
            # format pixels
            if (x == 8 and (y >1 and y < 8)):
                pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if (y == 8 and (x >=0 and x < 8) and not (x == 1 or x == 7)):
                pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if (y == 8 and (x <= size - 3 and x >= size - 7)):
                pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            
            #version pixels
            if (x == size - 11):
                if (y == 1):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
                if (y == 4):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if (x == size - 10):
                if (y == 1):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if (x == size - 9):
                if (y == 3):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
                if (y == 4):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            
            if (y == size - 11):
                if (x == 0):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
                if (x == 2):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
                if (x == 3):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if (y == size - 10):
                if (x == 0):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
                if (x == 3):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            if (y == size - 9):
                if (x == 0):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
                if (x == 2):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
                if (x == 5):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            
            # real data, if statement needed for not overwriting the template
            if ((x >= 9 and x <= 21 and y != 6)   or   (y >= 9 and y <= 21 and x != 6)   or   (x >= 7 and x <= 8 and y >= 21 and y <= 24)   or   (y >= size - 4 and x >= size - 15)   or   (y >= size - 15 and x >= size - 4)   or   ((x == size - 10 or x == size - 11) and y >= size - 15)   or   (x >= size - 15 and (y == size - 10 or y == size - 11)) ):
                #pygame.draw.rect(window, test, (x*10 + 20, y*10 + 20, 10, 10))
                if (btstr[y*size + x] == "1"):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            """
            try:
                if (string[y*size + x] == "1"):
                    pygame.draw.rect(window, qrcol, (x*10 + 20, y*10 + 20, 10, 10))
            except IndexError:
                pass
            """

curqr = rngen()
running = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            curqr = rngen()

    window.fill(backg)
    render(curqr)

    pygame.display.flip()

pygame.quit()