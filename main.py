import sys
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout
from PySide6.QtCore import QThreadPool
from ui.popup import PopupService
from ui.settings_window import SettingsWindow
from services.clipboard import ClipboardServices
from services.controller import Controller
from services.ai_service import AIService
from tasks.explain_task import ExplainTask
from services.add_hotkey import HotkeyServices
from services.context_service import ContextService
from services.history_service import HistoryService
from ui.history_window import HistoryWindow

app = QApplication(sys.argv)
clipboard=ClipboardServices()
settings=SettingsWindow()
ai = AIService()
thread_pool=QThreadPool()
context_service=ContextService()
history_service=HistoryService()
history_window = HistoryWindow(history_service)
popup = PopupService(settings, history_window)
controller = Controller(popup, clipboard, ai, thread_pool, context_service, history_service)
popup.set_controller(controller)
hotkey=HotkeyServices(controller)
hotkey.start()
app.exec()
