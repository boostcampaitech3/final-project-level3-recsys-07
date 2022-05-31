import os
import pandas as pd
from utils_item import *

if __name__ == "__main__":

    # -- option 설정
    _PREPROCESS = 'raw'
    _STORE_OPTION = 'codishop'
    _SORT_OPTION = 'view'

    ITEM_PATH = f'/opt/ml/input/data/{_PREPROCESS}_{_STORE_OPTION}/{_SORT_OPTION}/item/'
    CODI_PATH = f'/opt/ml/input/data/{_PREPROCESS}_{_STORE_OPTION}/{_SORT_OPTION}/codi/'

    # -- 데이터 불러오기
    raw_data = pd.read_excel(os.path.join(ITEM_PATH, "item.xlsx"), engine='openpyxl')

    # -- 데이터 전처리
    preprocessed_data, need_revision_data = class_preprocess(raw_data)
    preprocessed_data = likes_preprocess(preprocessed_data)
    preprocessed_data = color_preprocess(preprocessed_data)
    preprocessed_data = rating_preprocess(preprocessed_data)
    preprocessed_data = gender_preprocess(preprocessed_data)
    preprocessed_data = season_preprocess(preprocessed_data)
    preprocessed_data = view_preprocess(preprocessed_data)
    preprocessed_data = cum_sale_preprocess(preprocessed_data)
    preprocessed_data = buy_age_preprocess(preprocessed_data, ITEM_PATH)
    preprocessed_data = buy_gender_preprocess(preprocessed_data, ITEM_PATH)
    preprocessed_data = color_class_preprocess(preprocessed_data)
    preprocessed_data = mid_class_preprocess(preprocessed_data)
    preprocessed_data = cluster_preprocess(preprocessed_data)

    print('Done')

    # -- preprocessed data save
    SAVE_ITEM_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/item/'
    SAVE_CODI_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/codi/'
    
    if os.path.exists(os.path.join(SAVE_ITEM_PATH, "item.xlsx")) == False:
        os.makedirs(SAVE_ITEM_PATH)
    preprocessed_data.to_csv(os.path.join(SAVE_ITEM_PATH, "item.csv"), index=False)