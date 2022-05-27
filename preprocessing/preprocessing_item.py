import numpy as np
import pandas as pd
from utils_item import *

if __name__ == "__main__":
    raw_data = pd.read_excel("/opt/ml/input/data/raw_codishop/view/item/item.xlsx")

    preprocessed_data, need_revision_data = class_preprocess(raw_data)
    preprocessed_data = likes_preprocess(preprocessed_data)
    preprocessed_data = color_preprocess(preprocessed_data)
    preprocessed_data = rating_preprocess(preprocessed_data)
    preprocessed_data = gender_preprocess(preprocessed_data)
    preprocessed_data = season_preprocess(preprocessed_data)