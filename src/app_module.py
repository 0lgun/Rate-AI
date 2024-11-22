import sqlite3

from PyQt5.QtWidgets import QPushButton

# gerekli modüller import ediliyor.

icon_folder = "app_icons/" # iconların bulunduğu klasör

resources_folder = "src/resources/" # kaynak dosyalarının bulunduğu klasör

conn = sqlite3.connect(resources_folder+"database.db") # bağlantı kur.
cursor = conn.cursor()

# style sheet fonksiyonu
get_features = lambda font="Segoe Print", size=17, color="black",background_color="transparent",\
                      border=0,border_color="black":("font-family: {}; font-size: {}px; color: {};background-color: {};border: {}px solid {};"
     .format(font, size, color, background_color,border,border_color))

def set_checkbox_icon(checkbox,path,x=100,y=100): # check_box icon için fonksiyon
    checkbox.setStyleSheet(f'''
        QCheckBox::indicator {{
            width: {x}px;
            height: {y}px;
            border-image: url({path});
        }}
    ''')

class RoundButton(QPushButton): # özelleştirilmiş buton
    def __init__(self,x=100,y=60,text="Go"):
        super().__init__()
        self.setFixedSize(x,y)
        self.setText(text)
        self.setStyleSheet(f"""
    QPushButton {{
        border-radius: {y//2}px;
        background-color: grey;
        color: white;
    }}
    QPushButton:hover {{
        background-color: #45a049;
    }}
""")


# widget özelleştirme
def customize_widget(widget, text_size = 40, background_color = "transparent",
                     color = "black",border_color = "black", border = 0, text="", font = "Segoe Print"):
    widget.adjustSize()
    widget.setStyleSheet(
            get_features(size=text_size, background_color=background_color, color=color,
                         border=border, border_color=border_color,font=font))
    widget.setText(text)

# pencerelerde göstermek için dosya ismini sadeleştiriyor.
def get_file_name(path):
    last_index = path.rfind("/") # son '/' karakteri
    filename = path[last_index+1:-4] # dosya uzantısı çıkarılıyor.
    return filename
    # örneğin : C:Users/Desktop/....resources/comments.txt --> ismi : comments olarak döndürür.