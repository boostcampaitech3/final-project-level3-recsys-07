import numpy as np
import pandas as pd
from class_preprocess import class_preprocess
from likes_preprocess import likes_preprocess
from color_preprocess import color_preprocess
from rating_preprocess import rating_preprocess

raw_data = pd.read_excel("/opt/ml/input/data/raw_codishop/view/item/item.xlsx")

print("Starting Data Preprocessing!")
print("1. Preprocessing for class...")
preprocessed_data, need_revision_data = class_preprocess(raw_data)
print("2. Preprocessing for likes...")
preprocessed_data = likes_preprocess(preprocessed_data)
print("3. Preprocessing for color...")
preprocessed_data = color_preprocess(preprocessed_data)
print("4. Preprocessing for rating")
preprocessed_data = rating_preprocess(preprocessed_data)
print("Preprocess Finished!")

print(preprocessed_data.head(10))