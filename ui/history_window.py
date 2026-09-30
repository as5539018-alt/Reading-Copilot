from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QTextEdit, QMessageBox
from PySide6.QtCore import Qt


class HistoryWindow(QWidget):
    def __init__(self, history_service):
        super().__init__()
        self.history_service = history_service
        self.setWindowTitle("Historique")
        layout = QVBoxLayout()
        self.setLayout(layout)
        H_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher dans l'historique...")
        layout.addWidget(self.search_input)
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        self.load_history()
        self.details = QTextEdit()
        self.details.setReadOnly(True)
        layout.addWidget(self.details)
        self.search_input.textChanged.connect(self.search_history)
        self.history_list.currentItemChanged.connect(self.show_entry)
        self.delete_button = QPushButton("🗑️ Supprimer")
        self.clear_button = QPushButton("🧹 Vider")
        layout.addWidget(self.delete_button)
        layout.addWidget(self.clear_button)
        self.delete_button.clicked.connect(self.delete_entry)
        self.clear_button.clicked.connect(self.clear_history)

    def load_history(self):
        entries = self.history_service.get_all()
        self.history_list.clear()
        for entry in entries:
            item = QListWidgetItem(f"{entry['word']} - {entry['date']}")      
            item.setData(Qt.UserRole, entry["id"])
            self.history_list.addItem(item)




    def search_history(self, query):
        entries = self.history_service.search(query)
        self.history_list.clear()
        for entry in entries:
            item = QListWidgetItem(f"{entry['word']} - {entry['date']}")
            item.setData(Qt.UserRole, entry["id"])
            self.history_list.addItem(item)



    def show_entry(self, current, previous):
        if current is None:
            return
        history_id = current.data(Qt.UserRole)
        entry = self.history_service.get_by_id(history_id)
        if entry is None:
            return
        word = entry["word"]
        explanation = entry["explanation"]
        date = entry["date"]
        text=(
            f" {date}\n\n"
            f"mot : {word}\n\n"
            f"Explication : \n {explanation}"
        )
        self.details.setPlainText(text)
    def delete_entry(self):
        current = self.history_list.currentItem()
        if current is None:
            return
        history_id = current.data(Qt.UserRole)
        answer = QMessageBox.question(self, "Confirmation", "Voulez-vous supprimer ce mot ? ")
        if answer != QMessageBox.Yes:
            return
        self.history_service.delete(history_id)
        self.load_history()
        self.details.clear()
    
    def clear_history(self):
        answer = QMessageBox.question(self, "Confirmation", "Voulez-vous tout supprimer ? ")
        if answer != QMessageBox.Yes:
            return
        self.history_service.clear_all()
        self.load_history()
        self.details.clear()