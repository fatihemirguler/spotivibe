import numpy as np
import pandas as pd
from PySide6.QtCore import Qt
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import euclidean_distances
import sys

from sklearn.preprocessing import MinMaxScaler
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QSlider, QComboBox

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

data_2_df=pd.read_csv("data_2.csv")
df=data_2_df.copy()

data_with_titles=df.drop(columns=["index","duration_ms","target"])
df = data_with_titles.drop(columns=["song_title", "artist",])

categorical_cols = ["key", "mode", "time_signature"]

df = pd.get_dummies(df, columns=categorical_cols)
numerical_cols = df.columns.difference(categorical_cols)

scaler = MinMaxScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# def normalize_input_feature(feature,min,max):
#     return (feature-min)/(max-min)

# print(df.describe())
sample_user_input = {
    "acousticness": 0.3,
    "danceability": 0.7,
    "energy":0.3,
    "instrumentalness": 0.4,
    'key_0':0,
    'key_1':0, 'key_2':0, 'key_3':0, 'key_4':0, 'key_5':0, 'key_6':0, 'key_7':0, 'key_8':1,
    'key_9':0, 'key_10':0, 'key_11':0,
    "liveness": 0.164,
    "loudness": 0.8,
    'mode_0': 0, 'mode_1':1, 'time_signature_1.0':0,
    'time_signature_3.0':0, 'time_signature_4.0':1, 'time_signature_5.0':0,
    "speechiness": 0.7,
    "tempo": 0.8,
    "valence": 0.1
}
user_input_array = np.array(list(sample_user_input.values()))

#print(user_input_array)
#key,mode,time_signature cat(one-hot)

# user_input_vector = [user_input[feature] for feature in df.columns if
#                      feature != "song_title" and feature != "artist"] #it basically means user_input as array

def show_song_with_spesific_key(key_index, data_frame, num_songs=5):
    songs_with_key = data_frame[data_frame[f'key_{key_index}'] == 1]

    if songs_with_key.empty:
        print("Bu anahtar notaya sahip şarkı bulunamadı.")
        return
    num_selected_songs = min(num_songs, len(songs_with_key))
    random_songs = songs_with_key.sample(num_selected_songs)
    selected_songs_with_titles = data_with_titles.loc[random_songs.index, ["song_title", "artist"]]
    # print(type(random_songs))
    print(selected_songs_with_titles)

# key_index = 11
# show_song_with_spesific_key(key_index, df)
# sys.exit()
# print(df.head(5))
# print(df.describe())
# print(df.columns)
# print(df.head(5))

# sys.exit()
# data_filtered = data_without_titles[
#     (data_without_titles["key"] == user_input["key"]) &
#     (data_without_titles["mode"] == user_input["mode"])
# ]

# distances = euclidean_distances(user_input_array.reshape((1,-1)), df)

def RecommendSong(user_input):
    user_input_array = np.array(list(user_input.values()))
    distances = euclidean_distances(user_input_array.reshape((1,-1)), df)
    # print(distances)
    nearest_songs_indices = distances[0].argsort()
    # print(type(nearest_songs_indices))  series
    print(data_with_titles.iloc[nearest_songs_indices[:3],-2:])

def scale_data(user_input, min_values, max_values):
    scaled_data = (user_input - min_values) / (max_values - min_values)
    return scaled_data

def ComboboxToDict(combo_box):
    dictionary={}
    current_selected_index = combo_box.currentIndex()
    for index in range(combo_box.count()):
        item_text = combo_box.itemText(index)
        if index!=current_selected_index:
            dictionary[item_text] = 0
        else:
            dictionary[item_text] = 1
    # print(dictionary)
    return dictionary

# app = QApplication(sys.argv)
#
# acousticness_edit = QLineEdit()
# danceability_edit = QLineEdit()
#
# # Sonuçları göstermek için bir QLabel oluşturun
# result_label = QLabel()
#
# # Butonu oluşturun ve tıklama olayı için metot bağlayın
# generate_button = QPushButton("Scale Et ve Göster")
# generate_button.clicked.connect(lambda: scale_and_show())
#
# # Layout oluşturun ve bileşenleri ekleyin
# layout = QVBoxLayout()
# layout.addWidget(QLabel("Acousticness:"))
# layout.addWidget(acousticness_edit)
# layout.addWidget(QLabel("Danceability:"))
# layout.addWidget(danceability_edit)
# # Diğer özellikler burada...
# layout.addWidget(generate_button)
# layout.addWidget(result_label)
#
# # Ana widget oluşturun ve layout'u ayarlayın
# window = QWidget()
# window.setLayout(layout)
#
#
# # Verilerin scale edilmesi ve sonuçların gösterilmesi için metot
# def scale_and_show():
#     try:
#         # Kullanıcı girişlerini alın
#         acousticness = float(acousticness_edit.text())
#         danceability = float(danceability_edit.text())
#         # Diğer özellikleri burada alın...
#
#         # Min ve max değerleri bulun (sizin verilerinizle değiştirin)
#         min_values = df[["acousticness", "danceability"]].min()
#         max_values = df[["acousticness", "danceability"]].max()
#
#         # Kullanıcı girişlerini scale edin
#         scaled_acousticness = scale_data(acousticness, min_values["acousticness"], max_values["acousticness"])
#         scaled_danceability = scale_data(danceability, min_values["danceability"], max_values["danceability"])
#         # Diğer özellikleri burada scale edin...
#
#         # Sonuçları QLabel üzerinde gösterin
#         result_label.setText(f"Scaled Acousticness: {scaled_acousticness}\nScaled Danceability: {scaled_danceability}")
#         # Diğer özellikleri burada gösterin...
#     except ValueError:
#         result_label.setText("Geçersiz giriş değerleri!")
#
# # Uygulamayı çalıştırın
# window.show()
# sys.exit(app.exec())

# PySide uygulaması oluşturun
app = QApplication(sys.argv)

# Kullanıcı girişleri için QSlider bileşenleri oluşturun
acousticness_slider = QSlider()
acousticness_slider.setOrientation(Qt.Horizontal)
acousticness_slider.setRange(0, 100)  # 0 ile 100 arasında değerler

danceability_slider = QSlider()
danceability_slider.setOrientation(Qt.Horizontal)
danceability_slider.setRange(0, 100)

energy_slider = QSlider()
energy_slider.setOrientation(Qt.Horizontal)
energy_slider.setRange(0, 100)

instrumentalness_slider = QSlider()
instrumentalness_slider.setOrientation(Qt.Horizontal)
instrumentalness_slider.setRange(0, 100)

liveness_slider = QSlider()
liveness_slider.setOrientation(Qt.Horizontal)
liveness_slider.setRange(0, 100)

loudness_slider = QSlider()
loudness_slider.setOrientation(Qt.Horizontal)
loudness_slider.setRange(0, 100)

tempo_slider = QSlider()
tempo_slider.setOrientation(Qt.Horizontal)
tempo_slider.setRange(0, 100)

speechiness_slider = QSlider()
speechiness_slider.setOrientation(Qt.Horizontal)
speechiness_slider.setRange(0, 100)

valence_slider = QSlider()
valence_slider.setOrientation(Qt.Horizontal)
valence_slider.setRange(0, 100)

key_combobox = QComboBox()
key_combobox.addItems(["key_" + str(i) for i in range(12)])  # key_0'dan key_11'e kadar seçenekler
# for index in range(key_combobox.count()):
#     print(key_combobox.itemText(index))

mode_combobox = QComboBox()
mode_combobox.addItems(["mode_0", "mode_1"])

time_signature_combobox = QComboBox()
time_signature_combobox.addItems(["time_signature_1.0", "time_signature_3.0", "time_signature_4.0", "time_signature_5.0"])

# Sonuçları göstermek için QLabel oluşturun
result_label = QLabel()

# Layout oluşturun ve bileşenleri ekleyin
submit_button = QPushButton("Submit")
layout = QVBoxLayout()
layout.addWidget(QLabel("Acousticness:"))
layout.addWidget(acousticness_slider)
layout.addWidget(QLabel("Danceability:"))
layout.addWidget(danceability_slider)
layout.addWidget(QLabel("Energy:"))
layout.addWidget(energy_slider)
layout.addWidget(QLabel("Instrumentalness:"))
layout.addWidget(instrumentalness_slider)
layout.addWidget(QLabel("Liveness:"))
layout.addWidget(liveness_slider)
layout.addWidget(QLabel("Loudness:"))
layout.addWidget(loudness_slider)
layout.addWidget(QLabel("Tempo:"))
layout.addWidget(tempo_slider)
layout.addWidget(QLabel("Speechiness:"))
layout.addWidget(speechiness_slider)
layout.addWidget(QLabel("Valence:"))
layout.addWidget(valence_slider)
layout.addWidget(QLabel("Key:"))
layout.addWidget(key_combobox)
layout.addWidget(QLabel("Mode:"))
layout.addWidget(mode_combobox)
layout.addWidget(QLabel("Time Signature:"))
layout.addWidget(time_signature_combobox)
layout.addWidget(submit_button)
layout.addWidget(result_label)



# Ana widget oluşturun ve layout
window = QWidget()
window.setLayout(layout)

# Slider değerleri değiştiğinde sonuçları güncelleme
def update_results():
    # Slider değerlerini 0-1 aralığında scale edin
    scaled_acousticness = acousticness_slider.value() / 100.0
    scaled_danceability = danceability_slider.value() / 100.0
    scaled_energy = energy_slider.value() / 100.0
    scaled_instrumentalness= instrumentalness_slider.value() / 100.0
    scaled_liveness = liveness_slider.value() / 100.0
    scaled_loudness = loudness_slider.value() / 100.0
    scaled_tempo = tempo_slider.value() / 100.0
    scaled_speechiness= speechiness_slider.value() / 100.0
    scaled_valence = valence_slider.value() / 100.0
    selected_key = key_combobox.currentText()
    selected_mode = mode_combobox.currentText()
    selected_time_signature = time_signature_combobox.currentText()
    # Sonuçları QLabel üzerinde gösterin
    result_label.setText(
        f"Scaled Acousticness: {scaled_acousticness:.2f}\n"
        f"Scaled Danceability: {scaled_danceability:.2f}\n"
        f"Scaled Energy: {scaled_energy:.2f}\n"
        f"Scaled Instrumentalness: {scaled_instrumentalness:.2f}\n"
        f"Scaled Liveness: {scaled_liveness:.2f}\n"
        f"Scaled Loudness: {scaled_loudness:.2f}\n"
        f"Scaled Tempo: {scaled_tempo:.2f}\n"
        f"Scaled Speechiness: {scaled_speechiness:.2f}\n"
        f"Scaled Valence: {scaled_valence:.2f}\n"
        f"Selected Key: {selected_key}\nSelected Mode: {selected_mode}\nSelected Time Signature: {selected_time_signature}"
    )

def on_submit_clicked():
    user_input = {
        "acousticness": acousticness_slider.value() / 100.0,
        "danceability": danceability_slider.value() / 100.0,
        "energy": energy_slider.value() / 100.0,
        "instrumentalness": instrumentalness_slider.value() / 100.0,
        "liveness": liveness_slider.value() / 100.0,
        "loudness": loudness_slider.value() / 100.0,
        "tempo": tempo_slider.value() / 100.0,
        "speechiness": speechiness_slider.value() / 100.0,
        "valence": valence_slider.value() / 100.0,
        # "key": key_combobox.currentText(),
        # "mode": mode_combobox.currentText(),
        # "time_signature": time_signature_combobox.currentText(),
    }
    user_input.update(ComboboxToDict(key_combobox))
    user_input.update(ComboboxToDict(mode_combobox))
    user_input.update(ComboboxToDict(time_signature_combobox))
    print(user_input)
    RecommendSong(user_input)

# Sliderların değer değişikliği sinyalini 'update_results' ile bağlama
acousticness_slider.valueChanged.connect(update_results)
danceability_slider.valueChanged.connect(update_results)
energy_slider.valueChanged.connect(update_results)
instrumentalness_slider.valueChanged.connect(update_results)
liveness_slider.valueChanged.connect(update_results)
loudness_slider.valueChanged.connect(update_results)
tempo_slider.valueChanged.connect(update_results)
speechiness_slider.valueChanged.connect(update_results)
valence_slider.valueChanged.connect(update_results)
key_combobox.currentIndexChanged.connect(update_results)
mode_combobox.currentIndexChanged.connect(update_results)
time_signature_combobox.currentIndexChanged.connect(update_results)
submit_button.clicked.connect(on_submit_clicked)


# Uygulamayı çalıştır
window.show()
sys.exit(app.exec())

# year
# selected_features=["year","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","tempo"]
# magical_features=["artist","genre"]
# df=df[selected_features]
# print(df.head())
# print(df.isnull().sum()) #0
# print(df.dtypes)









