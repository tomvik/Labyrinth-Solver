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

def Print(function_name: str, message: str):
    print('[{}]: {}'.format(function_name, message))

WINDOW_COORDINATES_TXT = "data/gameWindow.txt"
HEADLESS = True
PAGE_URL = "https://www.rechner.club/raetsel/labyrinth-generieren"
ROWS_ELEMENT_QUERY = '[name="zeilenstr"]'
COLUMNS_ELEMENT_QUERY = '[name="spaltenstr"]'
SUBMIT_ELEMENT_QUERY = '[name="berechnen"]'
IMAGE_BLOCK_ELEMENT_QUERY = '[id="ergebnisblock"]'
NUM_ROWS = 10
NUM_COLUMNS = 5
LABYRINTH_PATH = 'data/labyrinth.png'

pyautogui.PAUSE = 0.01

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
BINARY_WHITE = 255
BINARY_BLACK = 0
