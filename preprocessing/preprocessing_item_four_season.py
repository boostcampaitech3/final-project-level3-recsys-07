import pandas as pd
from utils_item_four_season import *
from utils_item import synchronize_with_item

if __name__ == "__main__":

    # -- option 설정
    _PREPROCESS = 'raw'
    _STORE_OPTION = 'codishop'
    _SORT_OPTION = 'view'

    ITEM_PATH = f'/opt/ml/input/data/{_PREPROCESS}_{_STORE_OPTION}/{_SORT_OPTION}/item/'
    CODI_PATH = f'/opt/ml/input/data/{_PREPROCESS}_{_STORE_OPTION}/{_SORT_OPTION}/codi/'
    SAVE_ITEM_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/item/'
    SAVE_CODI_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/codi/'

    item = pd.read_csv(SAVE_ITEM_PATH+"item.csv")
    item_four_season = pd.read_excel(ITEM_PATH+"item_four_season.xlsx", engine='openpyxl')

    # -- four season 데이터 전처리
    item_four_season = synchronize_with_item(item=item, raw_data=item_four_season)
    item_four_season = transform_season_to_four_season(item, item_four_season)
    item_four_season = preprocessing_null_season_data(item, item_four_season)

    # -- preprocessed data save
    item_four_season.to_csv(SAVE_ITEM_PATH+"item_four_season.csv", index=False)