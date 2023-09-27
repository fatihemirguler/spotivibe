import numpy as np
import pandas as pd
from PySide6.QtCore import Qt
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import euclidean_distances
import sys

from sklearn.preprocessing import MinMaxScaler

from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QSlider, QComboBox, QRadioButton, QButtonGroup, QHBoxLayout

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

data_2_df=pd.read_csv("data_2.csv")
df=data_2_df.copy()

data_with_titles=df.drop(columns=["index","duration_ms","target","key","time_signature"])
df = data_with_titles.drop(columns=["song_title", "artist",])

categorical_cols = ["mode"]

# df = pd.get_dummies(df, columns=categorical_cols)
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

# def show_song_with_spesific_key(key_index, data_frame, num_songs=5):
#     songs_with_key = data_frame[data_frame[f'key_{key_index}'] == 1]
#
#     if songs_with_key.empty:
#         print("Song Not Found.")
#         return
#     num_selected_songs = min(num_songs, len(songs_with_key))
#     random_songs = songs_with_key.sample(num_selected_songs)
#     selected_songs_with_titles = data_with_titles.loc[random_songs.index, ["song_title", "artist"]]
#     # print(type(random_songs))
#     print(selected_songs_with_titles)

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

def RecommendSong(user_input, mode):
    if len(user_input)==0:
        print("Please enter at least one feature.")
        return;
    user_input_features=user_input.keys()
    filtered_df=df[df['mode']==mode]
    filtered_df=filtered_df[user_input_features]
    user_input_array = np.array(list(user_input.values()))
    distances = euclidean_distances(user_input_array.reshape((1,-1)), filtered_df)
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
# 
# result_label = QLabel()
#
# 
# generate_button = QPushButton("Scale")
# generate_button.clicked.connect(lambda: scale_and_show())
#
# 
# layout = QVBoxLayout()
# layout.addWidget(QLabel("Acousticness:"))
# layout.addWidget(acousticness_edit)
# layout.addWidget(QLabel("Danceability:"))
# layout.addWidget(danceability_edit)
# # Diğer özellikler burada...
# layout.addWidget(generate_button)
# layout.addWidget(result_label)
#
#
# window = QWidget()
# window.setLayout(layout)
#
#
# 
# def scale_and_show():
#     try:
#         
#         acousticness = float(acousticness_edit.text())
#         danceability = float(danceability_edit.text())
#        
#
#         
#         min_values = df[["acousticness", "danceability"]].min()
#         max_values = df[["acousticness", "danceability"]].max()
#
#         
#         scaled_acousticness = scale_data(acousticness, min_values["acousticness"], max_values["acousticness"])
#         scaled_danceability = scale_data(danceability, min_values["danceability"], max_values["danceability"])
#         
#
#     
#         result_label.setText(f"Scaled Acousticness: {scaled_acousticness}\nScaled Danceability: {scaled_danceability}")
#         
#     except ValueError:
#         result_label.setText("!")
#
# window.show()
# sys.exit(app.exec())


app = QApplication(sys.argv)


acousticness_slider = QSlider()
acousticness_slider.setOrientation(Qt.Horizontal)
acousticness_slider.setRange(0, 100) 

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

# key_combobox = QComboBox()
# key_combobox.addItems(["key_" + str(i) for i in range(12)])  # key_0'dan key_11'e kadar seçenekler
# for index in range(key_combobox.count()):
#     print(key_combobox.itemText(index))

mode_combobox = QComboBox()
mode_combobox.addItems(["Down Mood", "Up Mood"])

# time_signature_combobox = QComboBox()
# time_signature_combobox.addItems(["time_signature_1.0", "time_signature_3.0", "time_signature_4.0", "time_signature_5.0"])

result_label = QLabel()

submit_button = QPushButton("Submit")

l_layout = QVBoxLayout()
r_layout=QVBoxLayout()
layout=QHBoxLayout()

acousticness_label = QLabel()
danceability_label = QLabel()
energy_label = QLabel()
instrumentalness_label = QLabel()
liveness_label = QLabel()
loudness_label = QLabel()
tempo_label = QLabel()
speechiness_label = QLabel()
valence_label = QLabel()
danceability_label = QLabel()

# acousticness_radio = QRadioButton()
# danceability_radio = QRadioButton()
# energy_radio = QRadioButton()
# instrumentalness_radio = QRadioButton()
# liveness_radio = QRadioButton()
# loudness_radio = QRadioButton()
# tempo_radio = QRadioButton()
# speechiness_radio = QRadioButton()
# valence_radio = QRadioButton()
# danceability_radio = QRadioButton()

l_layout.addWidget(acousticness_label)
l_layout.addWidget(acousticness_slider)
radio_group = QButtonGroup()
acousticness_radio_button_on = QRadioButton("On")
acousticness_radio_button_off = QRadioButton("Off")
l_layout.addWidget(acousticness_radio_button_on)
l_layout.addWidget(acousticness_radio_button_off)
radio_group.addButton(acousticness_radio_button_on)
radio_group.addButton(acousticness_radio_button_off)
acousticness_radio_button_off.setChecked(True)

l_layout.addWidget(danceability_label)
l_layout.addWidget(danceability_slider)
danceability_radio_group = QButtonGroup()
danceability_radio_button_on = QRadioButton("On")
danceability_radio_button_off = QRadioButton("Off")
l_layout.addWidget(danceability_radio_button_on)
l_layout.addWidget(danceability_radio_button_off)
danceability_radio_group.addButton(danceability_radio_button_on)
danceability_radio_group.addButton(danceability_radio_button_off)
danceability_radio_button_off.setChecked(True)

l_layout.addWidget(energy_label)
l_layout.addWidget(energy_slider)
energy_radio_group = QButtonGroup()
energy_radio_button_on = QRadioButton("On")
energy_radio_button_off = QRadioButton("Off")
l_layout.addWidget(energy_radio_button_on)
l_layout.addWidget(energy_radio_button_off)
energy_radio_group.addButton(energy_radio_button_on)
energy_radio_group.addButton(energy_radio_button_off)
energy_radio_button_off.setChecked(True)

l_layout.addWidget(instrumentalness_label)
l_layout.addWidget(instrumentalness_slider)
instrumentalness_radio_group = QButtonGroup()
instrumentalness_radio_button_on = QRadioButton("On")
instrumentalness_radio_button_off = QRadioButton("Off")
l_layout.addWidget(instrumentalness_radio_button_on)
l_layout.addWidget(instrumentalness_radio_button_off)
instrumentalness_radio_group.addButton(instrumentalness_radio_button_on)
instrumentalness_radio_group.addButton(instrumentalness_radio_button_off)
instrumentalness_radio_button_off.setChecked(True)

r_layout.addWidget(liveness_label)
r_layout.addWidget(liveness_slider)
liveness_radio_group = QButtonGroup()
liveness_radio_button_on = QRadioButton("On")
liveness_radio_button_off = QRadioButton("Off")
r_layout.addWidget(liveness_radio_button_on)
r_layout.addWidget(liveness_radio_button_off)
liveness_radio_group.addButton(liveness_radio_button_on)
liveness_radio_group.addButton(liveness_radio_button_off)
liveness_radio_button_off.setChecked(True)

r_layout.addWidget(loudness_label)
r_layout.addWidget(loudness_slider)
loudness_radio_group = QButtonGroup()
loudness_radio_button_on = QRadioButton("On")
loudness_radio_button_off = QRadioButton("Off")
r_layout.addWidget(loudness_radio_button_on)
r_layout.addWidget(loudness_radio_button_off)
loudness_radio_group.addButton(loudness_radio_button_on)
loudness_radio_group.addButton(loudness_radio_button_off)
loudness_radio_button_off.setChecked(True)

r_layout.addWidget(tempo_label)
r_layout.addWidget(tempo_slider)
tempo_radio_group = QButtonGroup()
tempo_radio_button_on = QRadioButton("On")
tempo_radio_button_off = QRadioButton("Off")
r_layout.addWidget(tempo_radio_button_on)
r_layout.addWidget(tempo_radio_button_off)
tempo_radio_group.addButton(tempo_radio_button_on)
tempo_radio_group.addButton(tempo_radio_button_off)
tempo_radio_button_off.setChecked(True)

r_layout.addWidget(speechiness_label)
r_layout.addWidget(speechiness_slider)
speechiness_radio_group = QButtonGroup()
speechiness_radio_button_on = QRadioButton("On")
speechiness_radio_button_off = QRadioButton("Off")
r_layout.addWidget(speechiness_radio_button_on)
r_layout.addWidget(speechiness_radio_button_off)
speechiness_radio_group.addButton(speechiness_radio_button_on)
speechiness_radio_group.addButton(speechiness_radio_button_off)
speechiness_radio_button_off.setChecked(True)

r_layout.addWidget(valence_label)
r_layout.addWidget(valence_slider)
valence_radio_group = QButtonGroup()
valence_radio_button_on = QRadioButton("On")
valence_radio_button_off = QRadioButton("Off")
r_layout.addWidget(valence_radio_button_on)
r_layout.addWidget(valence_radio_button_off)
valence_radio_group.addButton(valence_radio_button_on)
valence_radio_group.addButton(valence_radio_button_off)
valence_radio_button_off.setChecked(True)

# layout.addWidget(QLabel("Key:"))
# layout.addWidget(key_combobox)

layout.addWidget(QLabel("Mode:"))
layout.addWidget(mode_combobox)

# layout.addWidget(QLabel("Time Signature:"))
# layout.addWidget(time_signature_combobox)

layout.addWidget(submit_button)
layout.addWidget(result_label)

layout.addLayout(l_layout)
layout.addLayout(r_layout)

window = QWidget()
window.setLayout(layout)

def show_updated_data():
    scaled_acousticness = acousticness_slider.value() / 100.0
    scaled_danceability = danceability_slider.value() / 100.0
    scaled_energy = energy_slider.value() / 100.0
    scaled_instrumentalness= instrumentalness_slider.value() / 100.0
    scaled_liveness = liveness_slider.value() / 100.0
    scaled_loudness = loudness_slider.value() / 100.0
    scaled_tempo = tempo_slider.value() / 100.0
    scaled_speechiness= speechiness_slider.value() / 100.0
    scaled_valence = valence_slider.value() / 100.0
    # selected_key = key_combobox.currentText()
    # selected_mode = mode_combobox.currentText()

    acousticness_label.setText(f"Acousticness: {scaled_acousticness:.2f}")
    danceability_label.setText(f"Danceability: {scaled_danceability:.2f}")
    energy_label.setText(f"Energy: {scaled_energy:.2f}")
    instrumentalness_label.setText(f"Instrumentalness: {scaled_instrumentalness:.2f}")
    liveness_label.setText(f"Liveness: {scaled_liveness:.2f}")
    loudness_label.setText(f"Loudness: {scaled_loudness:.2f}")
    tempo_label.setText(f"Tempo: {scaled_tempo:.2f}")
    speechiness_label.setText(f"Speechiness: {scaled_speechiness:.2f}")
    valence_label.setText(f"Valence: {scaled_valence:.2f}")

    # selected_time_signature = time_signature_combobox.currentText()
    # Sonuçları QLabel üzerinde gösterin
def on_submit_clicked():
    user_input={}
    if acousticness_radio_button_on.isChecked():
        user_input["acousticness"]=acousticness_slider.value() / 100.0
    if danceability_radio_button_on.isChecked():
        user_input["danceability"]=danceability_slider.value() / 100.0
    if energy_radio_button_on.isChecked():
        user_input["energy"]=energy_slider.value() / 100.0
    if instrumentalness_radio_button_on.isChecked():
        user_input["instrumentalness"] = instrumentalness_slider.value() / 100.0
    if liveness_radio_button_on.isChecked():
        user_input["liveness"] = liveness_slider.value() / 100.0
    if loudness_radio_button_on.isChecked():
        user_input["loudness"] = loudness_slider.value() / 100.0
    if tempo_radio_button_on.isChecked():
        user_input["tempo"] = tempo_slider.value() / 100.0
    if speechiness_radio_button_on.isChecked():
        user_input["speechiness"] = speechiness_slider.value() / 100.0
    if valence_radio_button_on.isChecked():
        user_input["valence"] = valence_slider.value() / 100.0

    # user_input = {
    #     "acousticness": acousticness_slider.value() / 100.0,
    #     "danceability": danceability_slider.value() / 100.0,
    #     "energy": energy_slider.value() / 100.0,
    #     "instrumentalness": instrumentalness_slider.value() / 100.0,
    #     "liveness": liveness_slider.value() / 100.0,
    #     "loudness": loudness_slider.value() / 100.0,
    #     "tempo": tempo_slider.value() / 100.0,
    #     "speechiness": speechiness_slider.value() / 100.0,
    #     "valence": valence_slider.value() / 100.0,
    #     # "key": key_combobox.currentText(),
    #     # "mode": mode_combobox.currentText(),
    #     # "time_signature": time_signature_combobox.currentText(),
    # }
    # user_input.update(ComboboxToDict(key_combobox))
    # user_input.update(ComboboxToDict(mode_combobox))
    # user_input.update(ComboboxToDict(time_signature_combobox))
    current_mode=mode_combobox.currentIndex()
    print(f"user input: {user_input}")
    RecommendSong(user_input,current_mode)
    
acousticness_slider.valueChanged.connect(show_updated_data())
danceability_slider.valueChanged.connect(show_updated_data)
energy_slider.valueChanged.connect(show_updated_data)
instrumentalness_slider.valueChanged.connect(show_updated_data)
liveness_slider.valueChanged.connect(show_updated_data)
loudness_slider.valueChanged.connect(show_updated_data)
tempo_slider.valueChanged.connect(show_updated_data)
speechiness_slider.valueChanged.connect(show_updated_data)
valence_slider.valueChanged.connect(show_updated_data)
#key_combobox.currentIndexChanged.connect(update_results)
#mode_combobox.currentIndexChanged.connect(update_results)
#time_signature_combobox.currentIndexChanged.connect(update_results)
submit_button.clicked.connect(on_submit_clicked)

window.show()
sys.exit(app.exec())

# year
# selected_features=["year","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","tempo"]
# magical_features=["artist","genre"]
# df=df[selected_features]
# print(df.head())
# print(df.isnull().sum()) #0
# print(df.dtypes)
