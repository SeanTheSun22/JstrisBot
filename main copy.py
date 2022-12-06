import json
import keyboard
import math
from PIL import ImageGrab
import time
import pyautogui
import numpy as np
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def CreateBoard(Positions, BoxSize, PieceColors):

    Screen = ImageGrab.grab((Positions["P1x"], Positions["P1y"], Positions["P2x"], Positions["P2y"]))

    Board = [[0 for x in range(10)] for y in range(20)] 
    for i in range(1, 20):
        for j in range(10):
            PixColor = Screen.getpixel((math.floor(j * BoxSize.x + BoxSize.x / 2), math.floor(i * BoxSize.y + BoxSize.y / 2)))
            if PixColor in PieceColors.keys():
                Board[i][j] = 1

    PixColor = Screen.getpixel((math.floor(4 * BoxSize.x + BoxSize.x / 2), math.floor(0 * BoxSize.y + BoxSize.y / 2)))
    if PixColor in PieceColors.keys():
        Piece = PieceColors[PixColor]
    else:
        Piece = None
    
    return Board, Piece

def ScoreBoard(NewBoard):

    HoleScore = 0
    Height = 0
    for j in range(10):
        i = 0
        while i != 20 and NewBoard[i][j] != 1:
            
            i += 1
        
        if 19 - i > Height:
            Height = 19 - i
        while i != 20:
            if NewBoard[i][j] == 0:
                HoleScore += 1
            i += 1

    RoughScore = 0
    i1 = 0
    while i1 != 20 and NewBoard[i1][0] != 1:
        i1 += 1
    for j in range(9):
        i2 = i1
        i1 = 0
        while i1 != 20 and NewBoard[i1][j + 1] != 1:
            i1 += 1
        RoughScore += abs(i2-i1)

    Score = 10 * HoleScore + 2 * RoughScore + 2 * Height
    print(HoleScore, RoughScore, Height)
    return Score

def PlacedBoard(Board, Piece, Pos, Rotation):
    i = 0
    if Piece == "Bar":
        if Rotation == 0 or Rotation == 2:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0 and Board[i + 1][Pos + 2] == 0 and Board[i + 1][Pos + 3] == 0:
                i += 1
            for j in range(4):
                Board[i][Pos + j] = 1
            return Board
        if Rotation == 1 or Rotation == 3:
            while i != 19 and Board[i + 1][Pos] == 0:
                i += 1
            for j in range(4):
                Board[i - j][Pos] = 1
            return Board
            
    if Piece == "T":
        if Rotation == 0:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0 and Board[i + 1][Pos + 2] == 0:
                i += 1
            for j in range(3):
                Board[i][Pos + j] = 1
            Board[i - 1][Pos + 1] = 1
            return Board
        if Rotation == 1:
            while i != 19 and Board[i][Pos + 1] == 0 and Board[i + 1][Pos] == 0:
                i += 1
            for j in range(3):
                Board[i - j][Pos] = 1
            Board[i - 1][Pos + 1] = 1
            return Board
        if Rotation == 2:
            while i != 19 and Board[i][Pos] == 0 and Board[i + 1][Pos + 1] == 0 and Board[i][Pos + 2] == 0:
                i += 1
            for j in range(3):
                Board[i - 1][Pos + j] = 1
            Board[i][Pos + 1] = 1
            return Board
        if Rotation == 3:
            while i != 19 and Board[i][Pos] == 0 and Board[i + 1][Pos + 1] == 0:
                i += 1
            for j in range(3):
                Board[i - j][Pos + 1] = 1
            Board[i - 1][Pos] = 1
            return Board

    if Piece == "Box":
        while i != 19 and Board[i + 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0:
            i += 1
        for j in range(2):
            Board[i][Pos + j] = 1
            Board[i - 1][Pos + j] = 1
        return Board
    if Piece == "S":
        if Rotation == 0 or Rotation == 2:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0 and Board[i][Pos + 2] == 0:
                i += 1
            for j in range(2):
                Board[i][Pos + j] = 1
                Board[i - 1][Pos + j + 1] = 1
            return Board
        if Rotation == 1 or Rotation == 3:
            while i != 19 and Board[i][Pos] == 0 and Board[i + 1][Pos + 1] == 0:
                i += 1
            for j in range(2):
                Board[i - j - 1][Pos] = 1
                Board[i - j][Pos + 1] = 1
            return Board
    if Piece == "Z":
        if Rotation == 0 or Rotation == 2:
            while i != 19 and Board[i][Pos] == 0 and Board[i + 1][Pos + 1] == 0 and Board[i + 1][Pos + 2] == 0:
                i += 1
            for j in range(2):
                Board[i][Pos + j + 1] = 1
                Board[i - 1][Pos + j] = 1
            return Board
        if Rotation == 1 or Rotation == 3:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i][Pos + 1] == 0:
                i += 1
            for j in range(2):
                Board[i - j][Pos] = 1
                Board[i - j - 1][Pos + 1] = 1
            return Board
    if Piece == "L":
        if Rotation == 0:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0 and Board[i + 1][Pos + 2] == 0:
                i += 1
            for j in range(3):
                Board[i][Pos + j] = 1
            Board[i - 1][Pos + 2] = 1
            return Board
        if Rotation == 1:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0:
                i += 1
            for j in range(3):
                Board[i - j][Pos] = 1
            Board[i][Pos + 1] = 1
            return Board
        if Rotation == 2:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i][Pos + 1] == 0 and Board[i][Pos + 2] == 0:
                i += 1
            for j in range(3):
                Board[i - 1][Pos + j] = 1
            Board[i][Pos] = 1
            return Board
        if Rotation == 3:
            i += 1
            while i != 19 and Board[i - 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0:
                i += 1
            for j in range(3):
                Board[i - j][Pos + 1] = 1
            Board[i - 2][Pos] = 1
            return Board

    if Piece == "J":
        if Rotation == 0:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0 and Board[i + 1][Pos + 2] == 0:
                i += 1
            for j in range(3):
                Board[i][Pos + j] = 1
            Board[i - 1][Pos] = 1
            return Board
        if Rotation == 1:
            i += 1
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i - 1][Pos + 1] == 0:
                i += 1
            for j in range(3):
                Board[i - j][Pos] = 1
            Board[i - 2][Pos + 1] = 1
            return Board
        if Rotation == 2:
            while i != 19 and Board[i][Pos] == 0 and Board[i][Pos + 1] == 0 and Board[i + 1][Pos + 2] == 0:
                i += 1
            for j in range(3):
                Board[i - 1][Pos + j] = 1
            Board[i][Pos + 2] = 1
            return Board
        if Rotation == 3:
            while i != 19 and Board[i + 1][Pos] == 0 and Board[i + 1][Pos + 1] == 0:
                i += 1
            for j in range(3):
                Board[i - j][Pos + 1] = 1
            Board[i][Pos] = 1
            return Board

def FindSpot(Board, Piece, Hold, PieceGeometry):
    k = 0
    for j in range(1,10):
        i = 0
        while i != 19 and Board[i][j] == 0:
            i += 1
        k += i
    i = 0
    while i != 19 and Board[i][0] == 0:
        i += 1
    if k / 9 <= i - 4:
        if Piece == "Bar":
            return 0, 1, 0        
        if Hold == "Bar":
            return 0, 1, 1
    
    x = random.randint(0,1)

    Scores = [[32767 for x in range(10)] for y in range(8)]
    Board = np.array(Board)

    for i in range(x, 11 - PieceGeometry[Piece][0]):
        NewBoard = Board.copy()
        NewBoard = PlacedBoard(NewBoard, Piece, i, 0)
        Scores[0][i] = ScoreBoard(NewBoard)

    for i in range(x, 11 - PieceGeometry[Piece][0]):
        NewBoard = Board.copy()
        NewBoard = PlacedBoard(NewBoard, Piece, i, 2)
        Scores[2][i] = ScoreBoard(NewBoard)
    
    for i in range(x, 11 - PieceGeometry[Piece][1]):
        NewBoard = Board.copy()
        NewBoard = PlacedBoard(NewBoard, Piece, i, 1)
        Scores[1][i] = ScoreBoard(NewBoard)
    
    for i in range(x, 11 - PieceGeometry[Piece][1]):
        NewBoard = Board.copy()
        NewBoard = PlacedBoard(NewBoard, Piece, i, 3)
        Scores[3][i] = ScoreBoard(NewBoard)

    for i in range(x, 11 - PieceGeometry[Hold][0]):
        NewBoard = Board.copy()
        NewBoard = PlacedBoard(NewBoard, Hold, i, 0)
        Scores[4][i] = ScoreBoard(NewBoard)

    for i in range(x, 11 - PieceGeometry[Hold][0]):
        NewBoard = Board.copy()
        NewBoard = PlacedBoard(NewBoard, Hold, i, 2)
        Scores[6][i] = ScoreBoard(NewBoard)
    
    for i in range(x, 11 - PieceGeometry[Hold][1]):
        NewBoard = Board.copy()
        NewBoard = PlacedBoard(NewBoard, Hold, i, 1)
        Scores[5][i] = ScoreBoard(NewBoard)

    for i in range(x, 11 - PieceGeometry[Hold][1]):
        NewBoard = Board.copy()
        NewBoard = PlacedBoard(NewBoard, Hold, i, 3)
        Scores[7][i] = ScoreBoard(NewBoard)

    index = [0, 0]
    for i in range(8):
        for j in range(10):
            if Scores[i][j] < Scores[index[0]][index[1]]:
                index = [i, j]
    print(index)
    if index[0] <= 3:
        return index[1], index[0], 0
    else:
        return index[1], index[0] - 4, 1

def PlacePiece(Piece, Hold, Spot, Rotation, Chosen, Time):
    if Chosen == 1:
        pyautogui.press('c')
        Temp = Hold
        Hold = Piece
        Piece = Temp

    if Piece == "Bar":
        if Rotation == 0:
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 1:
            pyautogui.press('up')
            if Spot <= 4:
                pyautogui.press('left', presses = 5 - Spot)    
            else:
                pyautogui.press("right", presses = Spot - 5)  
            pyautogui.press('space')
            return Hold
        if Rotation == 2:
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 3:
            pyautogui.press('up')
            if Spot <= 3:
                pyautogui.press('left', presses = 4 - Spot)    
            else:
                pyautogui.press("right", presses = Spot - 4)  
            pyautogui.press('space')
            return Hold
    if Piece == "T":
        if Rotation == 0:
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot) 
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 1:
            pyautogui.press('up')
            if Spot <= 3:
                pyautogui.press('left', presses = 4 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 4)
            pyautogui.press('space')
            return Hold
        if Rotation == 2:
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 3:
            pyautogui.press('up')
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
    if Piece == "Box":
        if Spot <= 3:
            pyautogui.press('left', presses = 4 - Spot)
        else:
            pyautogui.press("right", presses = Spot - 4)
        pyautogui.press('space')
        return Hold
    if Piece == "S":
        if Rotation == 0:
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 1:
            pyautogui.press('up')
            if Spot <= 3:
                pyautogui.press('left', presses = 4 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 4)
            pyautogui.press('space')
            return Hold
        if Rotation == 2:
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 3:
            pyautogui.press('up')
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
    if Piece == "Z":
        if Rotation == 0:
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 1:
            pyautogui.press('up')
            if Spot <= 3:
                pyautogui.press('left', presses = 4 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 4)
            pyautogui.press('space')
            return Hold
        if Rotation == 2:
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 3:
            pyautogui.press('up')
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
    if Piece == "L":
        if Rotation == 0:
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 1:
            pyautogui.press('up')
            if Spot <= 3:
                pyautogui.press('left', presses = 4 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 4)
            pyautogui.press('space')
            return Hold
        if Rotation == 2:
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 3:
            pyautogui.press('up')
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
    if Piece == "J":
        if Rotation == 0:
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 1:
            pyautogui.press('up')
            if Spot <= 3:
                pyautogui.press('left', presses = 4 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 4)
            pyautogui.press('space')
            return Hold
        if Rotation == 2:
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
        if Rotation == 3:
            pyautogui.press('up')
            pyautogui.press('up')
            pyautogui.press('up')
            if Spot <= 2:
                pyautogui.press('left', presses = 3 - Spot)
            else:
                pyautogui.press("right", presses = Spot - 3)
            pyautogui.press('space')
            return Hold
    return Hold

def main():
    with open('GamePos.json', 'r') as file:
        Positions = json.load(file)

    GameSize = Point(Positions["P2x"] - Positions["P1x"], Positions["P2y"] - Positions["P1y"])

    BoxSize = Point(math.floor(GameSize.x / 10), math.floor(GameSize.y / 20))

    PieceColors = {(15, 155, 215): "Bar",
                   (175, 41, 138): "T",
                   (227, 159, 2): "Box",
                   (89, 177, 1): "S",
                   (215, 15, 55): "Z",
                   (227, 91, 2): "L",
                   (33, 65, 198): "J",}

    PieceGeometry = {"Bar": [4, 1],
                     "T": [3, 2],
                     "Box": [2, 2],
                     "S": [3, 2],
                     "Z": [3, 2],
                     "L": [3, 2],
                     "J": [3, 2]}

    Time = 0
    
    time.sleep(2)
    Board, Piece = CreateBoard(Positions, BoxSize, PieceColors)
    Hold = "Bar"
    pyautogui.press('c')

    while not keyboard.is_pressed('Esc'):
        Board, Piece = CreateBoard(Positions, BoxSize, PieceColors)
        if Piece != None:
            Spot, Rotation, Chosen = FindSpot(Board, Piece, Hold, PieceGeometry)
            print(Spot, Rotation, Chosen)
            Hold = PlacePiece(Piece, Hold, Spot, Rotation, Chosen, Time)
    return

main()