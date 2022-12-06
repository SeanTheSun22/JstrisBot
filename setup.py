
import keyboard
import pyautogui
import json


def FindPos():
    print("Press Enter to set")
    keyboard.wait('enter')
    return pyautogui.position()

print("Place cursor over top left of game box")
P1 = FindPos()
print("Place cursor over bottom right of game box")
P2 = FindPos()

Positions = {
    "P1x":P1.x,




    "P1y":P1.y,
    "P2x":P2.x,
    "P2y":P2.y
}

with open("GamePos.json", "w") as file:
    json.dump(Positions, file)

