import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QDialog, QProgressBar, QMessageBox, QPushButton, \
    QApplication

from src.app_module import get_features, icon_folder, customize_widget, cursor, conn, get_file_name


# gerekli modüller import ediliyor.

class Analysis(QDialog): # Yüzde olarak memnuniyet oranını gösteren sınıf

    def __init__(self,rating,path,is_exists): # rating ve dosya ismi parametre olarak alınıyor.
        super().__init__()
        self.save_score(path,rating,is_exists)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # soru işareti gizleniyor.

        print(rating,path,is_exists)

        self.path = path
        self.file_name = get_file_name(path) # pencere ismi için dosya adı kullanılıyor.
        self.color = "transparent" # duygu durumuna göre değişken bar çubuğu rengi
        self.rating = int (rating * 100) # rating yüzde cinsinden ifade edilecek.

        self.init_ui()

    def save_score(self,path,rating,is_exists):
        if not is_exists:
            cursor.execute("INSERT INTO Analysis VALUES (?,?)",(path,rating))
            conn.commit()

    def delete_record(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Onay Penceresi")
        seperator = "\n"+"*"*75+"\n"

        msgBox.setText(f"{self.file_name.upper()} ile ilgili tüm kayıtları silmek istediğinizden emin misiniz?"
                       f"{seperator}-Analiz ve puanlama işlemlerine ait tüm veriler silinecektir-{seperator}" )

        yes_button = msgBox.addButton('Evet', QMessageBox.YesRole)
        no_button = msgBox.addButton('Hayır', QMessageBox.NoRole)

        msgBox.setDefaultButton(no_button)

        msgBox.exec_()

        if msgBox.clickedButton() == yes_button:
            print(self.path)
            rated_path = self.path[ : -4] + "_rated.csv"
            print(rated_path)
            cursor.execute("DELETE FROM CurrentPages WHERE path=?", (rated_path,))
            conn.commit()

            cursor.execute("DELETE FROM Analysis WHERE path=?", (self.path,))
            conn.commit()

            if os.path.isfile(self.path):
                os.remove(rated_path)
            QMessageBox.information(self,"KAYIT SİLME",f"{self.file_name} ile ilgili tüm kayıtlar başarıyla silindi!")
            self.close()

    def create_delete_button(self):
        delete_button = QPushButton(self)
        delete_button.clicked.connect(self.delete_record)
        customize_widget(delete_button, text="KAYDI SİL", color="black", border_color="red",
                         border=2, background_color="red", text_size=20, font="Arial Black")

        delete_layout = QHBoxLayout()
        delete_layout.addWidget(delete_button, alignment=Qt.AlignCenter)

        return delete_layout

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
        x,y = 375,250
        right_side = QVBoxLayout() # ekranın sağı
        left_side = QVBoxLayout() # ekranın solu

        background = QLabel(self)
        background.setPixmap(QPixmap(icon_folder+"analysis_background.jpg")) # arka plan
        background.adjustSize()

        emotion = self.get_emotion() # duygu durumu tespiti - icon ismi

        progress_bar = QProgressBar(self) # Yüzdeyi gösterecek olan bar
        progress_bar.setValue(self.rating)
        progress_bar.setTextVisible(False)
        progress_bar.setFixedWidth(x//2)
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

        emotion_layout.addSpacing(x//1.6)
        emotion_layout.addWidget(emotion_label)

        right_side.addLayout(emotion_layout)
        right_side.addStretch()

        layout = QVBoxLayout()

        delete_layout = self.create_delete_button()

        layout.addLayout(left_side)
        layout.addLayout(right_side)
        layout.addLayout(delete_layout)

        self.setLayout(layout)
        self.setWindowTitle("analiz <-> ".upper()+self.file_name.upper()) # pencere ismi
        self.setWindowIcon(QIcon(icon_folder + "analysis_icon.png")) # pencere ikonu
        self.setFixedSize(x,y) # sabit pencere boyutu

app = QApplication(sys.argv)
an = Analysis(rating=0.42857142857142855,
              path="C:/Users/Olgun/Desktop/Rate AI/screenshots/ÖZELLİK GÖSTER/result.txt",
              is_exists=True)
an.exec_()
sys.exit(app.exec_())