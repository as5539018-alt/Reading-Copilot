from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QSpinBox

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setFixedSize(250, 180)
        layout = QVBoxLayout()
        H_layout=QHBoxLayout()
        self.auto_copy = QCheckBox("Copier automatiquement la réponse")
        layout.addWidget(self.auto_copy)
        words_label = QLabel("Nombre maximum de mots")
        H_layout.addWidget(words_label)
        self.max_words= QSpinBox()
        self.max_words.setMinimum(20)
        self.max_words.setMaximum(300)
        self.max_words.setValue(80)
        H_layout.addWidget(self.max_words)
        layout.addLayout(H_layout)
        #layout.setSpacing(0)
        layout.setContentsMargins(10, 10, 10, 10)


        self.setLayout(layout)
        
        #self.setStyleSheet("""
        #QWidget{
        #    background: white;
        #   border:1px solid #D1D5DB;
        #    border-radius: 12px;
        #}
        #""")
