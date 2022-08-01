import pyautogui
from pynput import keyboard

key_option: str = ""

def on_press(key):
    global key_option
    if key == keyboard.Key.esc:
        print('Esc')
        key_option = 'q'
    else:
        try:
            key_option = key.char
            if key.char == 'q':
                print('q')
        except:
            key_option = ''
            pass

def initialize_keyboard_listener():
    keyboardListener = keyboard.Listener(on_press=on_press)
    keyboardListener.start()

WINDOW_COORDINATES_TXT = "data/gameWindow.txt"
PAGE_URL = "https://www.rechner.club/raetsel/labyrinth-generieren"

pyautogui.PAUSE = 0.01

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
BINARY_WHITE = 255
BINARY_BLACK = 0
