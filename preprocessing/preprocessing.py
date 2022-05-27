import numpy as np
import pandas as pd
from class_preprocess import class_preprocess
from likes_preprocess import likes_preprocess
from color_preprocess import color_preprocess
from rating_preprocess import rating_preprocess

raw_data = pd.read_excel("/opt/ml/input/data/raw_codishop/view/item/item.xlsx")

preprocessed_data, need_revision_data = class_preprocess(raw_data)
preprocessed_data = likes_preprocess(preprocessed_data)
preprocessed_data = color_preprocess(preprocessed_data)
preprocessed_data = rating_preprocess(preprocessed_data)

