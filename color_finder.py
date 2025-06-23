import pyautogui
import time

print("🖱 Hover over the top song result when it finishes loading. Ctrl+C to exit.")
while True:
    x, y = pyautogui.position()
    color = pyautogui.pixel(x, y)
    print(f"At ({x}, {y}) = {color}", end='\r')
    time.sleep(0.5)
