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

    item = pd.read_csv(SAVE_ITEM_PATH+"item.csv")
    item_codi_id = pd.read_excel(ITEM_PATH+"item_codi_id.xlsx", engine='openpyxl')

    # -- tag 데이터 전처리
    item_codi_id = synchronize_with_item(item=item, raw_data=item_codi_id)

    # -- preprocessed data save
    item_codi_id.to_csv(SAVE_ITEM_PATH+"item_codi_id.csv", index=False)