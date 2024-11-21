import sys
from functools import partial

from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QApplication, QMessageBox, QPushButton, QHBoxLayout

from src.app_module import get_features, icon_folder, RoundButton, customize_widget


class TestWindow(QWidget):

    def __init__(self,load_model):
        super().__init__()
        self.timer = QTimer()
        self.load_model = load_model
        self.default_text = "YORUM YAP..."
        self.init_ui()

    def update_label(self,result_label,text):
        result_label.setText(text)

    def send(self,result_label,text_area):
        user_comment = text_area.toPlainText()

        if user_comment == str() or user_comment ==  self.default_text:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir yargı belirtiniz.')
        else:
            from src.load_model import LoadModel
            load_model = LoadModel()
            interpret = load_model.interpret_comment(user_comment)
            result_label.setText("SONUÇ : ")

            self.timer.timeout.connect(partial(self.update_label, result_label,text="SONUÇ : " + interpret))
            self.timer.start(250) # 1/4 sn bekle. böylece kullanıcı yorumladığını anlayabilsin

    def init_ui(self):
        background = QLabel(self)
        background.setPixmap(QPixmap(icon_folder+"model_test_background.jpg"))
        background.adjustSize()

        text_area = QTextEdit(self)
        customize_widget(widget=text_area,text=self.default_text,color="white")
        text_area.moveCursor(QTextCursor.End)

        area_layout = QHBoxLayout()
        area_layout.addWidget(text_area, alignment=Qt.AlignCenter)

        result_label = QLabel(self)
        customize_widget(widget=result_label, text="SONUÇ : ", color="white")

        result_layout = QHBoxLayout()
        result_layout.addWidget(result_label, alignment=Qt.AlignCenter)

        send_button = QPushButton(self)
        customize_widget(widget=send_button, color="white")
        send_button.setIcon(QIcon(icon_folder+"random_icon.png"))
        #send_button.setIconSize(QSize(adjustSize()))
        send_button.clicked.connect(partial(self.send,result_label,text_area))

        button_layout = QHBoxLayout()
        button_layout.addWidget(send_button,)

        v_box = QVBoxLayout()

        v_box.addLayout(area_layout)
        v_box.addStretch()
        v_box.addLayout(button_layout)
        v_box.addLayout(result_layout)

        self.setLayout(v_box)
        self.setWindowTitle("MODEL TEST")
        self.setWindowIcon(QIcon(icon_folder + "model_test_icon.png"))
        self.show()