import pandas as pd
from tqdm import tqdm


def transform_season_to_four_season(item: pd.DataFrame, item_four_season: pd.DataFrame) -> pd.DataFrame:
    '''
    season 정보를 사용해서 four_season 정보에 추가
    '''
    new_item = pd.merge(item, item_four_season, how='left')
    only_season = new_item[(new_item['season'].notnull()) & (new_item['four_season'].isnull())]
    four_season_list = []

    for item_id, season_info in tqdm(zip(only_season['id'], only_season['season'])):
        if season_info == 'S/S':
            four_season_list.append([item_id, '봄'])
            four_season_list.append([item_id, '여름'])
        elif season_info == 'F/W':
            four_season_list.append([item_id, '가을'])
            four_season_list.append([item_id, '겨울'])
        else: # ALL
            four_season_list.append([item_id, '사계절'])

    appended_item_four_season = pd.DataFrame(four_season_list, columns=['id', 'four_season'])
    updated_item_four_season = pd.concat([item_four_season, appended_item_four_season], ignore_index=True)
    return updated_item_four_season.drop_duplicates().reset_index(drop=True)


def preprocessing_null_season_data(item: pd.DataFrame, item_four_season:pd.DataFrame) -> pd.DataFrame:
    '''
    item의 season 정보와 four_season 정보가 모두 없는 결측지 데이터 전처리
    '''
    new_item = pd.merge(item, item_four_season, how='left')
    no_both_season = new_item[(new_item['season'].isnull()) & (new_item['four_season'].isnull())]
    four_season_list = []

    for item_id in tqdm(no_both_season['id']):
        four_season_list.append([item_id, '사게졀']) 

    appended_item_four_season = pd.DataFrame(four_season_list, columns=['id', 'four_season'])
    updated_item_four_season = pd.concat([item_four_season, appended_item_four_season], ignore_index=True)
    return updated_item_four_season.drop_duplicates().reset_index(drop=True)