import sys
import os
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QApplication, QFrame, QStackedWidget, QPlainTextEdit, QSizePolicy, QLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer, QPoint, Qt

class PopupService(QWidget):
    def __init__(self, settings, history_window):
        super().__init__()
        self.setWindowTitle("""📖 Reading Copilot""")
        self.resize(400, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        Global_Layout = QVBoxLayout()
        close_button = QPushButton("✕")
        close_button.setObjectName("close_button")
        close_button.setFixedSize(40, 40)
        close_button.setStyleSheet("QPushButton:hover{background-color: #e74c3c;}")
        close_button.clicked.connect(self.close)
        minimize_button = QPushButton("—")
        minimize_button.setObjectName("minimize_button")
        minimize_button.setFixedSize(40, 40)
        minimize_button.setStyleSheet("QPushButton#minimize_button:hover{background-color: grey;}")
        minimize_button.clicked.connect(self.showMinimized)
        self.home = QPushButton("Accueil")
        self.home.setObjectName("home")
        self.home.setStyleSheet("QPushButton:hover{ background-color: grey;}")
        self.home.clicked.connect(self.show_home)
        self.historic_button = QPushButton("⟲ Historique")
        self.historic_button.setObjectName("historic_button")
        self.historic_button.setStyleSheet("QPushButton:hover{ background-color: grey;}")
        self.historic_button.clicked.connect(self.show_historic)
        self.barre = QWidget()
        self.barre.setStyleSheet("background-color: #2c3e50; min-height: 40px; max-height: 40px;")
        layout_barre = QHBoxLayout(self.barre)
        layout_barre.setContentsMargins(0, 0, 0, 0)
        layout_barre.addStretch()     
        layout_barre.addWidget(self.home)
        layout_barre.addWidget(self.historic_button)
        layout_barre.addWidget(minimize_button)
        layout_barre.addWidget(close_button)
        self.dragging = False
        self.drag_position = None
        self.mainpage = QWidget()
        mainpage_layout = QVBoxLayout(self.mainpage)



        self.label = QLabel("✨ Sélectionnez un texte puis faites «crtrl + shift + e».\n\n✨ Ou Ecrivez sur le champ ensuite cliquez sur « la flèche bleu ».\n\n La réponse apparaîtra ici.")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.button = QPushButton("↑")
        self.button.setObjectName("button")
        self.input_text = QPlainTextEdit()
        self.input_text.setPlaceholderText("Écris un mot, une phrase ou un paragraphe...")
        self.input_text.setFixedHeight(40)
        self.input_text.textChanged.connect(self.adjust_input_height)
        self.input_text.setFrameShape(QFrame.NoFrame)
        #self.input_text.setStyleSheet("border: none;")
        self.input_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.copy_button = QPushButton("📋")
        self.settings=settings
        self.settings_button=QPushButton("⚙️")
        p=self.settings.pos()
        self.settings.move(p.x(), p.y())
        self.history_window = history_window
        layout=QVBoxLayout()
        button_frame=QFrame()
        small_layout=QHBoxLayout()
        H_layout=QHBoxLayout()
        layout.addWidget(self.barre)
        #layout.addWidget(self.label)
        mainpage_layout.addWidget(self.label)

        small_layout.addWidget(self.button)
        small_layout.addWidget(self.copy_button)
        small_layout.addWidget(self.settings_button)
        small_layout.setContentsMargins(0,0,0,0)
        button_frame.setLayout(small_layout)
        H_layout.addWidget(self.input_text,1)
        H_layout.addWidget(button_frame, 0, Qt.AlignmentFlag.AlignBottom)
        H_layout.addStretch()
        H_layout.setContentsMargins(20, 10, 20, 10)
        my_frame=QFrame()
        my_frame.setObjectName("my_frame")
        my_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        my_frame.setStyleSheet("""
        #my_frame{
            border: 2px solid transparent;
            border-radius: 10px;
            background-color: white;
        }""")
        my_frame.setLayout(H_layout)
        
        #layout.addLayout(H_layout)
        mainpage_layout.addWidget(my_frame)
        self.setLayout(layout)
        self.my_stack = QStackedWidget()
        self.my_stack.addWidget(self.mainpage)
        self.my_stack.addWidget(self.history_window)
        layout.addWidget(self.my_stack)

        
        self.copy_button.setFixedWidth(42)
        self.settings_button.setFixedWidth(42)
        self.copy_button.setFixedHeight(40)
        self.settings_button.setFixedHeight(40)
        small_layout.setContentsMargins(0,0,0,0)
        small_layout.setSpacing(4)



        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)        



        self.setFixedSize(500, 420)
        font=QFont("Segoe UI", 11)
        self.setFont(font)
        self.input_text.setFont(font)

        
        dossier_actuel = os.path.dirname(os.path.abspath(__file__))
        chemin_css = os.path.join(dossier_actuel, "popup_style.css")
        with open(chemin_css, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def set_controller(self, controller):
        self.controller = controller
        self.button.clicked.connect(self.send_text)
        self.copy_button.clicked.connect(self.copy_response)
        self.copy_button.setEnabled(False)
        self.settings_button.clicked.connect(self.show_settings) 
        self.show()
    def show_text(self, text):
        self.label.setText(text)

    def show_loading(self):
        self.button.setEnabled(False)
        self.button.setText("⏳")
        self.label.setText("Analyse du texte en cour...")

    def hide_loading(self):
        self.button.setEnabled(True)
        self.button.setText("↑")
    
    def display_respsonse(self, text):
        self.show_text(text)
        self.hide_loading()
        self.copy_button.setEnabled(True)
   
    def copy_response(self):
        clipboard=QApplication.clipboard()
        clipboard.setText(self.label.text())
        self.copy_button.setText("✅")
        QTimer.singleShot(2000, lambda: self.copy_button.setText("📋"))
    def show_settings(self):
        position=self.settings_button.mapToGlobal( QPoint(0, self.settings_button.height()))
        self.settings.move(position)
        self.settings.show()

    def show_historic(self):
        self.history_window.load_history()
        self.my_stack.setCurrentWidget(self.history_window)
        """self.history_window.show()
        self.history_window.raise_()
        self.history_window.activateWindow()"""
    def show_home(self):
        self.my_stack.setCurrentWidget(self.mainpage)
    
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            if self.barre.geometry().contains(
                event.position().toPoint()):
                self.dragging = True
                self.drag_position =(
                    event.globalPosition().toPoint()
                    -self.frameGeometry().topLeft()
                )
        super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if self.dragging:
            new_position = (
                event.globalPosition().toPoint()
                -self.drag_position
            )
            self.move(new_position)
        super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.dragging = False
            self.drag_position = None
        super().mouseReleaseEvent(event)
    def adjust_input_height(self):
        line_count = 0
        block = self.input_text.document().begin()
        while block.isValid():
            line_count += block.layout().lineCount()
            block = block.next()
        line_height = self.input_text.fontMetrics().lineSpacing()
        total_height = (line_count * line_height) + 15
        total_height = max(40, min(total_height, 200)) 
        self.input_text.setFixedHeight(total_height)
    def send_text(self):
        text=self.input_text.toPlainText().strip()
        if not text:
            return
        self.controller.explain_manuel(text)
