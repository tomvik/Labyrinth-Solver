import Common
from BrowserWrapper import OpenBrowserAndStoreCustomLabyrinth

def PlayGame():
    OpenBrowserAndStoreCustomLabyrinth(Common.NUM_ROWS, Common.NUM_COLUMNS, Common.LABYRINTH_PATH)

    

if __name__ == "__main__":
    Common.initialize_keyboard_listener()
    PlayGame()