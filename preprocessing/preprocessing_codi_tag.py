import pandas as pd
from utils_codi import synchronize_with_codi

if __name__ == "__main__":

    # -- option 설정
    _STORE_OPTION = 'codishop'
    _SORT_OPTION = 'view'

    ITEM_PATH = f'/opt/ml/input/data/raw_{_STORE_OPTION}/{_SORT_OPTION}/item/'
    CODI_PATH = f'/opt/ml/input/data/raw_{_STORE_OPTION}/{_SORT_OPTION}/codi/'
    SAVE_ITEM_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/item/'
    SAVE_CODI_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/codi/'

    codi = pd.read_csv(SAVE_CODI_PATH+"codi.csv")
    codi_tag = pd.read_excel(CODI_PATH+"codi_tag.xlsx", engine='openpyxl')

    # -- tag 데이터 전처리
    codi_tag = synchronize_with_codi(codi=codi, raw_data=codi_tag)

    # -- preprocessed data save
    codi_tag.to_csv(SAVE_CODI_PATH+"codi_tag.csv", index=False)