import numpy as np
import pandas as pd
from utils_item import *

if __name__ == "__main__":

    # -- option 설정
    _PREPROCESS = 'raw'
    _STORE_OPTION = 'codishop'
    _SORT_OPTION = 'view'

    ITEM_PATH = f'/opt/ml/input/data/{_PREPROCESS}_{_STORE_OPTION}/{_SORT_OPTION}/item/'
    CODI_PATH = f'/opt/ml/input/data/{_PREPROCESS}_{_STORE_OPTION}/{_SORT_OPTION}/codi/'

    raw_data = pd.read_excel(ITEM_PATH+"item.xlsx")

    preprocessed_data, need_revision_data = class_preprocess(raw_data)
    preprocessed_data = likes_preprocess(preprocessed_data)
    preprocessed_data = color_preprocess(preprocessed_data)
    preprocessed_data = rating_preprocess(preprocessed_data)
    preprocessed_data = gender_preprocess(preprocessed_data)
    preprocessed_data = season_preprocess(preprocessed_data)
    preprocessed_data = buy_age_preprocess(preprocessed_data, ITEM_PATH)
    preprocessed_data = buy_gender_preprocess(preprocessed_data, ITEM_PATH)
