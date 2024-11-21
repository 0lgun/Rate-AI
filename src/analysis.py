from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QDialog, QProgressBar

from src.app_module import get_features, icon_folder, customize_widget, cursor, conn, get_file_name


# gerekli modüller import ediliyor.

class Analysis(QDialog): # Yüzde olarak memnuniyet oranını gösteren sınıf

    def __init__(self,rating,path,is_exists): # rating ve dosya ismi parametre olarak alınıyor.
        super().__init__()
        self.save_score(path,rating,is_exists)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # soru işareti gizleniyor.

        self.file_name = get_file_name(path) # pencere ismi için dosya adı kullanılıyor.
        self.color = "transparent" # duygu durumuna göre değişken bar çubuğu rengi
        self.rating = int (rating * 100) # rating yüzde cinsinden ifade edilecek.

        self.init_ui()

    def save_score(self,path,rating,is_exists):
        if not is_exists:
            cursor.execute("INSERT INTO Analysis VALUES (?,?)",(path,rating))
            conn.commit()

    def get_emotion(self): # ratinge göre duygu durunu döndüren fonksiyon
        if self.rating >= 75:
            emotion =  "very_happy" # icon ismi
            self.color = "green" # duyguya göre özelleştirilmiş bar rengi

        elif self.rating > 60: # rating
            emotion = "happy"
            self.color = "blue"

        elif 0.25 < self.rating < 40:
            emotion = "sad"
            self.color = "orange"

        elif self.rating <= 25:
            emotion = "very_sad"
            self.color = "red"

        else:
            emotion = "confused"
            self.color = "yellow"

        return emotion # icon ismi döndürülüyor.

    def init_ui(self):
        right_side = QVBoxLayout() # ekranın sağı
        left_side = QVBoxLayout() # ekranın solu

        background = QLabel(self)
        background.setPixmap(QPixmap(icon_folder+"analysis_background.jpg")) # arka plan
        background.adjustSize()

        emotion = self.get_emotion() # duygu durumu tespiti - icon ismi

        progress_bar = QProgressBar(self) # Yüzdeyi gösterecek olan bar
        progress_bar.setValue(self.rating)
        progress_bar.setTextVisible(False)
        progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {self.color}; }}")

        recognition_item = QLabel(self) # büyüteç ve duygu iconu
        recognition_item.setPixmap(QPixmap(icon_folder+"emotion-recognition.png"))

        emotion_label = QLabel(self) # ilgili duyguyu gösteren icon
        emotion_label.setPixmap(QPixmap(icon_folder+emotion+".png"))

        progress_label = QLabel(self) # yüzdeyi sayı cinsinden ifade eden label
        customize_widget(widget = progress_label, text = f"%{self.rating}", text_size = 35, color = self.color)

        rate_layout = QHBoxLayout()  # widget yerleştirmek için yatay layout

        rate_layout.addWidget(recognition_item) # yerleştirme işlemleri
        rate_layout.addWidget(progress_label)
        rate_layout.addStretch()

        left_side.addWidget(progress_bar)
        left_side.addLayout(rate_layout)

        emotion_layout = QHBoxLayout()

        emotion_layout.addStretch()
        emotion_layout.addWidget(emotion_label)

        right_side.addLayout(emotion_layout)

        layout = QHBoxLayout()

        layout.addLayout(left_side)
        layout.addLayout(right_side)

        self.setLayout(layout)
        self.setWindowTitle("analiz <-> ".upper()+self.file_name.upper()) # pencere ismi
        self.setWindowIcon(QIcon(icon_folder + "analysis_icon.png")) # pencere ikonu
        self.setFixedSize(250,175) # sabit pencere boyutu