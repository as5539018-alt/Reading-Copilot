from PySide6.QtCore import QObject, Signal
class TaskSignal(QObject):
    finished=Signal(str)