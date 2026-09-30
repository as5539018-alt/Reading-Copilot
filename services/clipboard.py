import pyperclip
from pynput import keyboard
import time

class ClipboardServices:
    def __init__(self):
        self.controller = keyboard.Controller()
    def copy_selection(self):
        self.controller.release(keyboard.Key.shift)
        self.controller.release(keyboard.Key.shift_r)
        self.controller.press(keyboard.Key.ctrl)
        self.controller.press("c")
        self.controller.release("c")
        self.controller.release(keyboard.Key.ctrl)
        time.sleep(0.1)
    def get_text(self):
        return pyperclip.paste()    
        