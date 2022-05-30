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
    item_rel_coid_url = pd.read_excel(ITEM_PATH+"item_rel_codi_url.xlsx", engine='openpyxl')

    # -- related codi url 데이터 전처리
    item_rel_coid_url = synchronize_with_item(item=item, raw_data=item_rel_coid_url)

    # -- preprocessed data save
    item_rel_coid_url.to_excel(SAVE_ITEM_PATH+"item_rel_coid_url.xlsx", index=False)