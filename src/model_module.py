import numpy as np

from  tensorflow.python.keras.layers import CuDNNGRU
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Layer

from src.app_module import resources_folder

# gerekli modüller import ediliyor.

class CustomCuDNNGRU(Layer): # modelin .h5 olarak kaydedilmesi için özelleştirilmiş CuDNNGRU
    def __init__(self, units, return_sequences=False, **kwargs):
        super(CustomCuDNNGRU, self).__init__(**kwargs)
        self.units = units
        self.return_sequences = return_sequences
        self.gru = CuDNNGRU(units, return_sequences=return_sequences)

    def call(self, inputs):
        return self.gru(inputs)

    def get_config(self):
        config = super(CustomCuDNNGRU, self).get_config()
        config.update({
            "units": self.units,
            "return_sequences": self.return_sequences,
        })
        return config


path = resources_folder + "merge.txt"

model_path = resources_folder+"model.h5"

data = list()
target = list()

with open(path, "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip("\n")

    target.append(int(line[0])) # ratingler
    data.append(line[2:]) # yorumlar

cutoff = int(len(data) * 0.15) # verilerin %80i eğitim, %20si test için kullanılacak.

data_train = data[cutoff:] # yorum eğitim
target_train = target[cutoff:] # rating eğitim
target_train = np.array(target_train)

data_test = data[:cutoff] # yorumların % 20si
target_test = target[:cutoff] # ratinglerin % 20si
target_test = np.array(target_test)

numwords = 10000 # kelime haznesi - en çok kullanılan 10k kelimeyi al.
tokenizer = Tokenizer(num_words=numwords) # 10bin kelimelik tokenizer oluştur.

tokenizer.fit_on_texts(data) # en sık geçen kelimelere sayılar atanır. çok : 1, bilgisayar : 7000 gibi.

data_train_tokens = tokenizer.texts_to_sequences(data_train) # data-train tokenizasyonu (tüm dataya göre)
data_test_tokens = tokenizer.texts_to_sequences(data_test) # data-test tokenizasyonu (tüm dataya göre)

# tüm yorumların uzunluğunu tutan dizi
num_tokens = [len(tokens) for tokens in (data_test_tokens+data_train_tokens)]
num_tokens = np.array(num_tokens) # daha kolay işlem yapabilmek için numpy array'e dönüştürüyoruz.

max_data_size = np.max(num_tokens) # en uzun yorum

max_tokens = max_data_size # daha yüksek doğruluk için en uzun yoruma göre alıyoruz.
max_tokens = int(max_tokens) # token sayısı tam sayı olmalı.
# 0'lar eklenerek boyut max_tokens'a sabitleniyor.

data_train_pad = pad_sequences(data_train_tokens, maxlen=max_tokens)
data_test_pad = pad_sequences(data_test_tokens, maxlen=max_tokens)

idx = tokenizer.word_index  # her kelime ve her kelimenin sayısal değeri
inverse_map = dict(zip(idx.values(), idx.keys()))  # sayısal değer çağrıldığında kelimeyi bulsun

# inverse_map.get(7) # --> 7. en çok kullanılan kelime

def tokens_to_string(tokens):
    # token 0 değilse token'ı listeye ekle.
    words = [inverse_map.get(token) for token in tokens if token != 0]

    text = " ".join(words)
    return text