import pygame, sys
import socket
from pygame.locals import *
import pickle
import random
pygame.init()
fps = pygame.time.Clock()
scrn = pygame.display.set_mode((720, 360))
bg = pygame.image.load('bg.png')
server = "192.168.64.56"
port = 5555
font = pygame.font.Font('freesansbold.ttf', 32)
player1turn = font.render('your turn',True, 'black' )
player2turn = font.render('oppenant turn',True, 'black' )
youlost = font.render('YOU LOST', True, 'yellow')
youwon = font.render('YOU WON', True, 'yellow')
scorerect1 = (100,2,100,100)
scorerect2 = (550,2,100,100)
turnrect = (310,2,100,100)
resultbox = (310,130,100,100)
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((server, port))
game_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
run = True
boatx = []
boaty = []
while run:
    x = random.randint(1,10)
    y = random.randint(1,10)
    if x not in boatx and len(boatx) < 11:
        boatx.append(x)
    if y not in boaty and len(boaty) < 11:
        boaty.append(y)
    if len(boatx) == 10 and len(boaty) == 10:
        run = False
c.send(pickle.dumps((boatx, boaty)))
boatse = pickle.loads(c.recv(2048))
for t in range(10):
    x = boatse[0][t] + 12
    y = boatse[1][t]
    game_map[y][x] = 2
for t in range(10):
    x = boatx[t]
    y = boaty[t]
    game_map[y][x] = 1
rects = []
ourboat = []
y = 0
for raw in game_map:
    x = 0
    for tile in raw:
        if tile == 1:
            ourboat.append(pygame.Rect(x*30, y*30, 29, 29))
        rects.append(pygame.Rect(x*30, y*30, 29, 29))
        x += 1
    y += 1
dropedf = []
dropeds = []
tobesent = []
receved = []
def bomb_drop(loc,x,y):
    tobesent.append((x-13,y))
    y = loc // 24
    x = loc - ((y)*24)
    if game_map[y][x] == 2:
        dropeds.append(rects[loc])
    if game_map[y][x] == 0:
        dropedf.append(rects[loc])
s1 = 0
s2 = 0
turn = pickle.loads(c.recv(2048))
print(turn)
nothing = 0
c.sendall(pickle.dumps(nothing))
gameover = False
while True:
    scrn.blit(bg, (0,0))
    if s1 == 10:
        scrn.blit(youwon, resultbox)
        gameover = True
    if s2 == 10:
        scrn.blit(youlost, resultbox)
        gameover = True
    s1 = len(dropeds)
    s2 = 0
    for cords in receved:
        if game_map[cords[1]-1][cords[0]] == 1:
            s2 += 1
    score1 = font.render('score: ' + str(s1), True, 'black')
    score2 = font.render('score: ' + str(s2), True, 'black')
    if turn == 1:
        scrn.blit(player1turn,turnrect)
    else:
        scrn.blit(player2turn,turnrect)
    scrn.blit(score1,scorerect1)
    scrn.blit(score2,scorerect2)
    l = pickle.loads(c.recv(2048))
    if len(l) == 0 or l in receved:
        pass
    else:
        turn = 1 - turn
        receved.append(l)
    if len(tobesent) == 0:
        t = ()
        c.send(pickle.dumps(t))
    else:
        t = tobesent[-1]
        c.send(pickle.dumps(t))
    mx, my = pygame.mouse.get_pos()
    x = ((mx//10)//3)+1
    y = ((my//10)//3)+1
    rectno = ((y - 1)*24) + x
    pygame.draw.rect(scrn,'red',rects[rectno - 1])
    for rect in ourboat:
        pygame.draw.rect(scrn,'brown',rect)
    for rect in dropedf:
        pygame.draw.rect(scrn,'blue',rect)
    for rect in dropeds:
        pygame.draw.rect(scrn,'black',rect)
    for cords in receved:
        if game_map[cords[1]-1][cords[0]] == 0:
            pygame.draw.rect(scrn,'blue',rects[((cords[1] - 1)*24) + cords[0]])
        else:
            pygame.draw.rect(scrn,'black',rects[((cords[1] - 1)*24) + cords[0]])
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if gameover == False and x > 13 and x < 24 and y > 1 and y < 12 and turn == 1 and (x-13,y) not in tobesent:
                    turn = 1 - turn
                    bomb_drop(rectno - 1,x,y)

    pygame.display.update()
    fps.tick(60)
