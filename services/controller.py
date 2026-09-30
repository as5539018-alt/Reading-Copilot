from tasks.explain_task import ExplainTask
from tasks.explain_manuel_task import ExplainManuelTask

class Controller:
    def __init__(self, popup, clipboard, aiservice, thread_pool, context_service, history_service):
        self.popup = popup
        self.clipboard=clipboard
        self.aiservice=aiservice
        self.thread_pool = thread_pool
        self.context_service = context_service
        self.history_service = history_service
    def explain(self):
        self.clipboard.copy_selection()
        selected_text=self.clipboard.get_text()
        selected_text=selected_text.strip()
        context = self.context_service.get_context()
        if not selected_text:
            return "il n'y a pas de texte selectionné ou service indisponible"
        result=self.aiservice.explain(selected_text, context)
        self.history_service.save(
                selected_text,
                context,
                result
        )
        return result
    def for_manuel_explain(self, text):
        result=self.aiservice.explain(text, None)
        self.history_service.save(
                text,
                None,
                result
        )
        return result
    def start_explanation(self):
        self.popup.show()
        self.popup.show_loading()
        task = ExplainTask(self)
        task.signal.finished.connect(self.popup.display_respsonse)
        self.thread_pool.start(task)
    def explain_manuel(self, text):
        self.popup.show_loading()
        task = ExplainManuelTask(self, text)
        task.signal.finished.connect(self.popup.display_respsonse)
        self.thread_pool.start(task)
    def raiser(self):
        self.popup.raise_()
        self.popup.activateWindow()