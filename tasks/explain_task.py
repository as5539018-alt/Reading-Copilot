from PySide6.QtCore import QRunnable
from tasks.task_signal import TaskSignal
import traceback

class ExplainTask(QRunnable):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.signal=TaskSignal()
    def run(self):
        try:
            response=self.controller.explain()
            self.signal.finished.emit(response)
        except Exception as e:
            self.signal.finished.emit("Le Service d'Explication est temporairement indisponible.")
            traceback.print_exc()