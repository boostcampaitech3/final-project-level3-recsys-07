import pandas as pd
from utils_item_fit import *
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
    item_fit = pd.read_excel(ITEM_PATH+"item_fit.xlsx", engine='openpyxl')
    item_tag = pd.read_excel(ITEM_PATH+"item_tag.xlsx", engine='openpyxl')

    # -- fit 데이터 전처리
    item_fit = synchronize_with_item(item=item, raw_data=item_fit)
    item_fit_from_tag = make_item_fit_from_tag(item_tag=item_tag)
    item_fit = transform_fit_from_tag_to_fit(item, item_fit, item_fit_from_tag)
    item_fit = preprocessing_null_fit_data(item, item_fit, item_fit_from_tag)

    # -- preprocessed data save
    item_fit.to_excel(SAVE_ITEM_PATH+"item_fit.xlsx", index=False)