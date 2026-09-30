from pynput import keyboard

class HotkeyServices:
    def __init__(self, controller):
        self.controller=controller
        self.listener=keyboard.GlobalHotKeys(
            {"<ctrl>+<shift>+e": self.controller.start_explanation})
    def start(self):
        self.listener.start()