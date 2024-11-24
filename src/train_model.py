import os.path

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from src.model_module import CustomCuDNNGRU, numwords,data_test_pad,target_test, max_tokens, data_train_pad, target_train, model_path
from tensorflow.keras.optimizers import Adam
from keras.saving.save import save_model

if os.path.isfile(model_path):
    os.remove(model_path)

model = Sequential() # katmanların sırayla eklendiği model.
embedding_size = 60 # her kelimenin vektör temsili için kullanılacak boyut
# input dim : kelime haznesi, output_dim : vektör uzunluğu, input_length = pad edilmiş dizi uzunluğu
model.add(Embedding(input_dim=numwords, output_dim=embedding_size,
                    input_length=max_tokens,name="embedding-layer"))

# CuDNNGRU;  GRU'ya göre 10 kat daha hızlı.
model.add(CustomCuDNNGRU(units = 16,return_sequences=True)) # 16 nöron, tüm output'lar dönsün.
model.add(CustomCuDNNGRU(units=8, return_sequences=True)) # 8 nöron
model.add(CustomCuDNNGRU(units=4)) # 4 nöron ve son olduğu için False dönüyor
# model.add(CuDNNGRU(units=4)) #aynı şey. default = False
model.add(Dense(1,activation="sigmoid")) # 1e yakınsa olumlu, 0'a yakınsa olumsuz.

optimizer = Adam(learning_rate=1e-3) # 1e-3 = 10 üzeri -3 --> 0.001

model.compile(loss="binary_crossentropy",optimizer=optimizer,metrics=["accuracy"]) # 0-1 olduğu için binary

model.fit(x=data_train_pad,y=target_train,epochs = 4, batch_size = 128)
# data : veriler, target : 0-1 etiketler, epochs -> kaç defa eğitilsin, batch -> paket boyutu

save_model(model,model_path)

result = model.evaluate(data_test_pad, target_test) # 95.07
