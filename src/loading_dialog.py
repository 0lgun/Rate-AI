from functools import partial

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog, QHBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer

from src.app_module import icon_folder, customize_widget

# gerekli modüller import ediliyor.

class LoadModelThread(QThread):
    def __init__(self,path):
        super().__init__()
        self.path = path
    model = pyqtSignal(object) # modeli al

    def run(self):
        from src.load_model import LoadModel
        model = LoadModel(comments_path=self.path) # modeli yükle
        self.model.emit(model)

class LoadingDialog(QDialog): # yükleniyor penceresi
    def __init__(self,path=""):
        super().__init__()
        self.success = False # yükleme tamamlandı mı?
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.num_dark = 1

        self.color = "#2F2F2F" # koyu gri

        self.estimatedCompletionTime = 14000 # yaklaşık tamamlanma süresi

        self.value = 0

        self.path = path

        self.model = None

        self.initUI()

    def initUI(self):
        x,y = 500,375
        self.setWindowTitle('Model Yükleme')
        
        self.label = QLabel("Yükleniyor {}".format(self.num_dark*"."), self)
        customize_widget(widget=self.label,color="white")

        self.progress_label = QLabel(self)
        customize_widget(widget=self.progress_label,color="white",text=f"%0")

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress_label,alignment=Qt.AlignRight)
        progress_layout.addSpacing(x//5)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedSize(x//1.5,y//25)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(self.estimatedCompletionTime)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {self.color};
                border: 2px solid {self.color};
            }}
            QProgressBar::chunk {{
                background-color: white;
            }}
        """)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label,alignment=Qt.AlignCenter)
        layout.addWidget(self.progress_bar,alignment=Qt.AlignCenter)
        layout.addLayout(progress_layout)
        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(partial(self.update_progress_bar, self.success))
        self.timer.start(500)  # 1000 ms = 1 saniye

        self.start_loading(self.path)

        self.setLayout(layout)
        self.setFixedSize(x,y)

        self.setStyleSheet("background-color: black;")
        self.setWindowIcon(QIcon(icon_folder+"loading_icon.png"))
        self.setWindowTitle("Model Yükleniyor...")

    def start_loading(self,path):
        self.label.setText('Yükleniyor .')
        self.thread = LoadModelThread(path=self.path)
        self.thread.model.connect(self.get_model)
        self.thread.start()

    def get_model(self, model):
        self.model = model
        self.label.setText("Yükleme \nbaşarıyla\ntamamlandı.")
        self.timer.stop()
        self.progress_label.setText("%100")
        self.progress_bar.setValue(self.estimatedCompletionTime)
        QTimer.singleShot(1000,self.close)
        self.success = True

    def update_progress_bar(self,success):
        try:
            if not success:
                self.label.setText("Yükleniyor {}".format(self.num_dark * "."))

                self.num_dark += 1

                if self.value == self.estimatedCompletionTime:
                    self.value = int(self.estimatedCompletionTime * .99)

                self.progress_bar.setValue(self.value)

                rate = (self.value/self.estimatedCompletionTime)*100
                rate = round(rate)

                if rate == int(rate):
                    rate = int(rate)

                if rate >= 99:
                    rate = 99

                self.progress_label.setText(f"%{rate}")

                if self.num_dark == 4:
                    self.num_dark = 1

                self.value += 500

        except AttributeError:
            pass