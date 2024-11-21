import pandas as pd

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QDialog, QApplication

from src.app_module import icon_folder, get_features, set_checkbox_icon, resources_folder, cursor, conn


# gerekli modüller import ediliyor.


class ShowRatings(QDialog): # ratinglerle birlikte gösteren pencere
    def __init__(self,rated_path,file_name="chat_comments_rated"):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.file_name = file_name

        self.path = rated_path
        self.page_path = resources_folder + "current_page"

        self.num_showing_comment = 9 # bir sayfada gösterilecek yorum sayısı

        self.font_size = 90 // self.num_showing_comment + 15

        self.current_window_index,self.num_comment = int(),int() # bulunulan sayfa ve toplam yorum sayısı

        self.v_box = QVBoxLayout()

        self.comment_list,self.rating_list = list(),list() # yorum-rating listeleri

        self.get_active_window_index() # son bakılan pencrenin indeksini getir.

        self.init_ui()


    def create_new_rate_box(self):
        check_box = QLabel(self)
        check_box.setStyleSheet(get_features(background_color="transparent"))
        return check_box

    def is_file_exists(self): # dosya ismi veritabanında kayıtlı mı?
        cursor.execute("SELECT * FROM CurrentPages WHERE path = ?", (self.path,))
        data = cursor.fetchone()
        if data is None:
            return False # değil
        return True # kayıtlı

    def find_the_last_page(self):
        if self.num_comment == 0: # hiç yorum yoksa
            return 1  # sadece birinci sayfa
        elif self.num_comment % self.num_showing_comment == 0: # tam bölünüyorsa
            return int(self.num_comment / self.num_showing_comment)
        else: # tam bölünmüyorsa
            return int(self.num_comment // self.num_showing_comment) + 1

    def get_active_window_index(self):
        try:
            cursor.execute("SELECT currentPage FROM CurrentPages WHERE path=?", (self.path,))

            self.current_window_index = cursor.fetchone()[0]
        except TypeError: # daha önce harhangi bir sayfa değiştirme işlemi yapılmadıysa
            self.current_window_index = 1

    def save_current_page(self):
        if self.is_file_exists(): # kayıt varsa güncelle
            cursor.execute("UPDATE currentPages set CurrentPage = ? WHERE path=?",
                                (self.current_window_index,self.path))

        else: # yoksa kayıt oluştur
            cursor.execute("INSERT INTO CurrentPages (path,currentPage) VALUES (?,?)",
                                    (self.path,self.current_window_index))
        conn.commit()

    def restart(self): # pencereyi yeniden başlat
        self.close()
        show_ratings = ShowRatings(self.path,self.file_name)
        show_ratings.exec_()

    def change_window(self): # sayfayı değiştir
        button = self.sender()
        is_changed = False
        if button.objectName() == "prev" and self.current_window_index > 1: # önceki sayfaya git
            self.current_window_index -= 1 
            is_changed = True
        elif button.objectName() == "next" and self.current_window_index < self.find_the_last_page():
            self.current_window_index += 1 # sonraki sayfaya git
            is_changed = True
        if is_changed: # ilk sayfada geri ve son sayfada ileriye basılma durumlarında yenileme yapma.
            self.save_current_page()
            self.restart()


    def get_range(self):
        df = pd.read_csv(self.path, encoding='utf-8-sig')
        comments , ratings = df["comment"] , df["rating"]

        self.num_comment = len(df) #toplam yorum sayısı

        start_index = (self.current_window_index - 1) * self.num_showing_comment
        # bir sayfadaki yorum sayısı * (pencere-1)
        end_index = start_index + self.num_showing_comment
        # başlangıç indeksi + bir sayfadaki yorum sayısı
        # örneğin sayfa 2 için --> başangıç = 1*12 = 12 ve bitiş = 12+12 = 24
        # yani ikinci sayfa 12-23 arası yorumları gösterecek.

        for i in range(self.num_comment):
            comment = comments[i]

            if  end_index > i >= start_index and not comment in self.comment_list: # tekrarlama durumu
                self.comment_list.append(comment)
                self.rating_list.append(ratings[i]) # sadece ratingi al.
        
        return (start_index,end_index)


    def show_the_comments(self):
        comment_counter,rate_counter = 0,0
        index_list = self.get_range()
        start_index, end_index = index_list[0], index_list[1] # başlangıç, bitiş indeksleri ör: 36,48

        while comment_counter < len(self.comment_list): # tüm listeyi tara.
            content_label = QLabel(self)
            self.customize_widget(widget=content_label,
                                  text=str(comment_counter + start_index +  1) + ". " + str(
                                      self.comment_list[comment_counter]), font_size = self.font_size)

            rate_layout = QHBoxLayout()
            rate_layout.addStretch()

            for box in range(5): # rating için yıldızlar yerleştiriliyor.
                rate_box = self.create_new_rate_box()
                is_rated = "unrated.png"

                if self.rating_list[comment_counter] > rate_counter:
                    is_rated = "rated.png"

                rate_box.setPixmap(QPixmap(icon_folder+is_rated))

                rate_layout.addWidget(rate_box)
                rate_counter += 1

            rate_counter = 0  # yeni liste için rate sayacı sıfırlanıyor.

            h_box = QHBoxLayout()
            h_box.addWidget(content_label)
            h_box.addStretch()

            h_box.addLayout(rate_layout)

            self.v_box.addLayout(h_box)
            comment_counter += 1
        self.v_box.addStretch()
        self.create_navigation_items()
    
    def create_navigation_items(self):
        next_button = QPushButton(self)
        next_button.setObjectName("next")
        prev_button = QPushButton(self)
        prev_button.setObjectName("prev")

        self.page_label = QLabel(self)
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setText(str(self.current_window_index) + "/" + str(self.find_the_last_page()))
        self.page_label.setStyleSheet(get_features(size=self.font_size, color="white",font="Comic sans MS"))

        navigation_widgets = [prev_button, self.page_label, next_button]
        navigation_layout = QHBoxLayout()
        navigation_layout.addStretch()
        for widget in navigation_widgets:
            if widget.objectName() == "prev" or widget.objectName() == "next":
                widget.setIcon(QIcon(icon_folder + widget.objectName() + ".png"))
                widget.setIconSize(QSize(50, 50))
                widget.clicked.connect(self.change_window)
            navigation_layout.addWidget(widget)
        navigation_layout.addStretch()
        self.v_box.addStretch()
        self.v_box.addLayout(navigation_layout)

    def customize_widget(self, widget, font_size = 25, background_color = "transparent",
                         color = "white", border_color = "white", border = 0, text=""):
        if not self.font_size is None:
            font_size = self.font_size

        widget.adjustSize()
        widget.setStyleSheet(
            get_features(size=font_size, background_color=background_color, color=color,
                         border=border, border_color=border_color))
        widget.setText(text)

    def init_ui(self):
        window_background = QLabel(self)
        window_background.setPixmap(QPixmap(icon_folder + "show_rating_background.jpg"))
        window_background.adjustSize()

        self.show_the_comments()

        self.setLayout(self.v_box)

        self.setWindowTitle("PUANLANAN YORUMLAR")
        self.setWindowIcon(QIcon(icon_folder + "comment_icon.png"))