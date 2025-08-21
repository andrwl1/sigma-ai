import pandas as pd

def load_data():
    # Загружаем CSV-файл (при необходимости поменяешь путь)
    data = pd.read_csv("data/dataset.csv")
    return data

