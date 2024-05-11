import os
import keyboard
import time
import math
import random

def startgame():
    global leftpaddle
    global rightpaddle
    global ball
    global ballvelocity
    global gamerunning
    global gridsize
    global paddlesize
    global velocitymultiplier
    global botenabled
    global score

    botenabled = True

    gridsize = 32
    paddlesize = 9 #currently doesn't work for even numbers
    velocitymultiplier = 1
    score = 0

    leftpaddle = []
    rightpaddle = []

    for i in range(gridsize // 2 - paddlesize // 2, gridsize // 2 + paddlesize // 2 + 1):
        leftpaddle.append([i, 0])
        rightpaddle.append([i, gridsize-1])

    ball = [gridsize//2, gridsize//2] #ball starts in center

    ballvelocity = [random.uniform(-0.5, 0.5), 1]

    gamerunning = True

def updateball():
    global ball
    global ballvelocity
    global gamerunning
    global leftpaddle
    global rightpaddle
    global score

    ballrow = math.floor(ball[0])
    ballcol = math.floor(ball[1])

    if ballcol == gridsize-1 or ballcol == 0:
        gamerunning = False
        return
    if ballcol == gridsize-2:
        distance_from_center = ball[0] - rightpaddle[paddlesize // 2][0] 
        if abs(distance_from_center) <= paddlesize // 2:
            normalized_offset = distance_from_center / (paddlesize / 2)
            ballvelocity = [normalized_offset, -1]
            score += 1
    elif ballcol == 1:
        distance_from_center = ball[0] - leftpaddle[paddlesize // 2][0] 
        if abs(distance_from_center) <= paddlesize // 2:
            normalized_offset = distance_from_center / (paddlesize / 2)
            ballvelocity = [normalized_offset, 1]
            score += 1
    if ballrow == 0 or ballrow == gridsize-1:
        ballvelocity[0] *= -1

    ballrowvelocity, ballcolvelocity = ballvelocity
    ball[0] += ballrowvelocity * velocitymultiplier
    ball[1] += ballcolvelocity * velocitymultiplier


def drawmat():
    mat = [[" " for _ in range(gridsize)] for _ in range(gridsize)]
    for r, c in leftpaddle:
        mat[r][c] = "#"
    for r, c in rightpaddle:
        mat[r][c] = "#"
    
    r, c = ball
    mat[math.floor(r)][math.floor(c)] = "O"
    
    return mat


def updatescreen(mat):
    if not gamerunning:
        time.sleep(0.5)
    os.system('cls')
    if gamerunning:
        print("Terminal Pong")
        print("Press 'q' to quit | Press 'r' to restart")
        print(" " + " ".join("_" for _ in range(gridsize + 1)))
        print("\n".join("| " + " ".join(str(item) for item in row) + " |" for row in mat))
        print("|" + " ".join("_" for _ in range(gridsize + 1)) + "|")
        print("Score: ", score)
    else:
        print("YOU LOSE!")

startgame()

while True:
    time.sleep(0.025)
    if keyboard.is_pressed('s'):
        if leftpaddle[-1][0] < gridsize-1:
            for i in range(paddlesize):
                leftpaddle[i][0] += 1
    elif keyboard.is_pressed('w'):
        if leftpaddle[0][0] > 0:
            for i in range(paddlesize):
                leftpaddle[i][0] -= 1
    if not botenabled:
        if keyboard.is_pressed('k'):
            if rightpaddle[-1][0] < gridsize-1:
                for i in range(paddlesize):
                    rightpaddle[i][0] += 1
        elif keyboard.is_pressed('i'):
            if rightpaddle[0][0] > 0:
                for i in range(paddlesize):
                    rightpaddle[i][0] -= 1
    else:
        if ballvelocity[1] == 1:
            distance_to_edge = gridsize-1 - ball[1]
            predicted_row = ball[0] + math.floor(distance_to_edge * (ballvelocity[0] / ballvelocity[1]))

            if rightpaddle[len(rightpaddle) // 2][0] < predicted_row and rightpaddle[-1][0] < gridsize-1:
                for i in range(paddlesize):
                    rightpaddle[i][0] += 1
            elif rightpaddle[len(rightpaddle) // 2][0] > predicted_row and rightpaddle[0][0] > 0:
                for i in range(paddlesize):
                    rightpaddle[i][0] -= 1

    if gamerunning:
        updateball()
        updatescreen(drawmat())
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('r'):
        startgame()


