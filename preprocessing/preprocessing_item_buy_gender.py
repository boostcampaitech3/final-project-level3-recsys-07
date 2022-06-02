import pandas as pd
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

    item = pd.read_excel(SAVE_ITEM_PATH+"item.xlsx", engine='openpyxl')
    item_buy_gender = pd.read_excel(ITEM_PATH+"item_buy_gender.xlsx", engine='openpyxl')

    # -- buy gender 데이터 전처리
    item_buy_gender = synchronize_with_item(item=item, raw_data=item_buy_gender)

    # -- preprocessed data save
    item_buy_gender.to_csv(SAVE_ITEM_PATH+"item_buy_gender.csv", index=False)