import numpy as np
import pandas as pd
from class_preprocess import class_preprocess
from likes_preprocess import likes_preprocess

raw_data = pd.read_excel("/opt/ml/input/data/raw_codishop/view/item/item.xlsx")

for i in range(5) :
    print(raw_data.iloc[i])

preprocessed_data = class_preprocess(raw_data)
preprocessed_data = likes_preprocess(preprocessed_data)

for i in range(5):
    print(preprocessed_data.iloc[i])

