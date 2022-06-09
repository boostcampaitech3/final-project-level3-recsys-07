import os
import openpyxl
import pandas as pd

from ..utils_codi import synchronize_with_codi, synchronize_with_item

# !important: path parameter
_STORE_OPTION = 'codishop'
_SORT_OPTION = 'view'

ITEM_PATH = f'/opt/ml/input/data/raw_{_STORE_OPTION}/{_SORT_OPTION}/item/'
CODI_PATH = f'/opt/ml/input/data/raw_{_STORE_OPTION}/{_SORT_OPTION}/codi/'
SAVE_ITEM_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/item/'
SAVE_CODI_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/codi/'


# codi_tag 전처리
def preprocess_codi_tag():
    print ("Doing preprocess_codi_tag..")

    codi = pd.read_csv(SAVE_CODI_PATH + "codi.csv")
    codi_tag = pd.read_excel(CODI_PATH + "codi_tag.xlsx", engine='openpyxl')

    # -- tag 데이터 전처리
    codi_tag = synchronize_with_codi(codi=codi, raw_data=codi_tag)

    # -- preprocessed data save
    codi_tag.to_csv(SAVE_CODI_PATH + "codi_tag.csv", index=False)


# item_codi_id.csv 전처리
def preprocess_codi():
    print ("Doing preprocess_codi..")


    item_codi_id = pd.read_csv(SAVE_ITEM_PATH + "item_codi_id.csv")  # 전처리 되어있는 item_codi_id
    codi = pd.read_excel(CODI_PATH + "codi.xlsx", engine='openpyxl')

    # -- tag 데이터 전처리
    codi = synchronize_with_item(item_codi_id=item_codi_id, codi=codi)

    # -- preprocessed data save
    if os.path.exists(SAVE_CODI_PATH) == False:
        os.makedirs(SAVE_CODI_PATH)
    codi.to_csv(SAVE_CODI_PATH + "codi.csv", index=False)