from functools import partial

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import  QVBoxLayout, QLabel, QDialog, QHBoxLayout
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

        self.level_counter = 2
        self.num_dark = 1

        self.path = path

        self.model = None

        self.initUI()

    def initUI(self):
        x,y = 512,512
        self.setWindowTitle('Model Yükleme')
        self.setGeometry(300,100, x,y)

        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(icon_folder+f"level{self.level_counter}_loading.png"))
        self.background.setFixedSize(x,y)

        self.timer = QTimer(self)
        self.timer.timeout.connect(partial(self.update_background,self.success))
        self.timer.start(1000)  # 1000 ms = 1 saniye

        v_box = QVBoxLayout()
        
        label_layout = QHBoxLayout()
        
        self.label = QLabel("Yükleniyor {}".format(self.num_dark*"."), self)
        customize_widget(widget=self.label)
        
        label_layout.addStretch()
        label_layout.addWidget(self.label)
        label_layout.addStretch()

        v_box.addLayout(label_layout)

        self.start_loading(self.path)

        self.setLayout(v_box)
        self.setFixedSize(x,y)

        self.setWindowIcon(QIcon(icon_folder+"loading_icon.png"))
        self.setWindowTitle("Model Yükleniyor...")

    def start_loading(self,path):
        self.label.setText('Yükleniyor .')
        self.thread = LoadModelThread(path=self.path)
        self.thread.model.connect(self.get_model)
        self.thread.start()

    def get_model(self, model):
        self.model = model
        self.background.setPixmap(QPixmap(icon_folder+f"level{self.level_counter}_loading.png"))
        self.label.setText("Yükleme \nbaşarıyla\ntamamlandı.")
        QTimer.singleShot(1000,self.close)
        self.success = True

    def update_background(self,success):
        try:
            if not success:
                self.level_counter += 1
                path = icon_folder+f"level{self.level_counter}_loading.png"
                self.label.setText("Yükleniyor {}".format(self.num_dark * "."))
                self.background.setPixmap(QPixmap(path))

                self.num_dark += 1
                if self.num_dark == 4:
                    self.num_dark = 1

                if self.level_counter == 12:
                    self.level_counter = 1

        except AttributeError:
            pass