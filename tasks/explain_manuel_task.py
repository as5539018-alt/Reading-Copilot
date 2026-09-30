from PySide6.QtCore import QRunnable
from tasks.task_signal import TaskSignal
import traceback

class ExplainManuelTask(QRunnable):
    def __init__(self, controller, text):
        super().__init__()
        self.controller = controller
        self.signal=TaskSignal()
        self.text = text
    def run(self):
        try:
            response=self.controller.for_manuel_explain(self.text)
            self.signal.finished.emit(response)
        except Exception as e:
            self.signal.finished.emit("Le Service d'Explication est temporairement indisponible.")
            traceback.print_exc()