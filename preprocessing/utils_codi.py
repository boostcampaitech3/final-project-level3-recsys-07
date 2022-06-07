import pandas as pd
from tqdm import tqdm

def synchronize_with_codi(codi:pd.DataFrame, raw_data: pd.DataFrame) -> pd.DataFrame:
    '''
    전처리 된 codi의 id와 현재 raw_data의 codi id를 동기화
    : raw_data - codi feature list dataframe (ex. codi_tag, ...)
    '''
    codi_ids = codi['id'].unique()
    new_data_list = []

    for codi_id in tqdm(codi_ids):
        data = raw_data[raw_data['id']==codi_id].values.tolist()
        if data:
            new_data_list.extend(data)
            
    return pd.DataFrame(new_data_list, columns=raw_data.columns)



def synchronize_with_item(item_codi_id:pd.DataFrame, codi: pd.DataFrame) -> pd.DataFrame:
    '''
    전처리 된 item과 상호작용한 codi의 id와 현재 raw_data의 codi id를 동기화
    : raw_data - codi feature list dataframe (ex. ccodi_tag, ...)
    '''
    codi_ids = item_codi_id['codi_id'].unique()
    new_data_list = []

    for codi_id in tqdm(codi_ids):
        data = codi[codi['id']==codi_id].values.tolist()
        if data:
            new_data_list.extend(data)

    return pd.DataFrame(new_data_list, columns=codi.columns)