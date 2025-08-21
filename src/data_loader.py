import pandas as pd

def load_sample_data():
    data = {
        "Day": [1, 2, 3, 4, 5],
        "Progress": [1, 2, 3, 4, 5]
    }
    df = pd.DataFrame(data)
    return df

