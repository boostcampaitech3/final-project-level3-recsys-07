import pandas as pd
from tqdm import tqdm

def make_item_fit_from_tag(item_tag:pd.DataFrame) -> pd.DataFrame:
    '''
    item의 tag에서 fit 정보를 추출
    reuturn 값 - [id, fit_from_tag] dataframe
    '''
    fit_list = ["핏", "와이드", "오버", "슬림", "레귤러", "스키니", "루즈", "릴렉스", "퍼팩트", "스트레이트", "캐롯핏", "코어", "벌룬"]
    tag_fit_list = list()

    for id, tag in zip(item_tag['id'], item_tag['tag']) :
        for fit in fit_list :
            if fit in tag : tag_fit_list.append((id, tag))

    item_fit_from_tag = pd.DataFrame(tag_fit_list, columns=["id","fit_from_tag"])
    remove_carryover = item_fit_from_tag[item_fit_from_tag["fit_from_tag"]=="캐리오버"].index
    remove_corefit = item_fit_from_tag[item_fit_from_tag["fit_from_tag"]=="코어핏"].index
    item_fit_from_tag.drop(remove_carryover, inplace=True)
    item_fit_from_tag.drop(remove_corefit, inplace=True)

    for idx in tqdm(item_fit_from_tag.index):
        tag = item_fit_from_tag.loc[idx,'fit_from_tag']
        for fit in fit_list[1:]:
            if fit not in tag: continue
            if fit == "캐롯핏":
                item_fit_from_tag.loc[idx,'fit_from_tag'] = "슬림"
            elif fit in ["퍼팩트", "스탠다드핏", "스트레이트"]:
                item_fit_from_tag.loc[idx,'fit_from_tag'] = "레귤러"
            elif fit in ["벌룬", "오버"]:
                item_fit_from_tag.loc[idx,'fit_from_tag'] = "오버 사이즈"
            elif  fit == "릴렉스":
                item_fit_from_tag.loc[idx,'fit_from_tag'] = "루즈"
            else:
                item_fit_from_tag.loc[idx,'fit_from_tag'] = fit

    return item_fit_from_tag.drop_duplicates().reset_index(drop=True)


def transform_fit_from_tag_to_fit(item:pd.DataFrame, item_fit:pd.DataFrame, item_fit_from_tag: pd.DataFrame) -> pd.DataFrame:
    '''
    tag에 있는 fit 정보를 사용해서 fit에 데이터 추가
    : item_fit_from_tag [id, fit_from_tag] - tag에 있는 fit 정보가 담겨 있는 데이터프레임
    '''
    new_item = pd.merge(item, item_fit, how='left', on='id')
    new_item = pd.merge(new_item, item_fit_from_tag, how='left', on='id')
    only_fit_from_tag = new_item[(new_item['fit'].isnull()) & (new_item['fit_from_tag'].notnull())]
    id_fit_list = []

    for id, tag in tqdm(zip(only_fit_from_tag['id'], only_fit_from_tag['fit_from_tag'])):
        if tag == '오버': id_fit_list.append([id, '오버 사이즈'])
        else: id_fit_list.append([id, tag])

    appended_item_fit = pd.DataFrame(id_fit_list, columns=['id', 'fit'])
    updated_item_fit = pd.concat([item_fit, appended_item_fit], ignore_index=True)
    return updated_item_fit.drop_duplicates().reset_index(drop=True)


def preprocessing_null_fit_data(item:pd.DataFrame, item_fit:pd.DataFrame, item_fit_from_tag: pd.DataFrame) -> pd.DataFrame:
    '''
    item의 fit 정보와 fit_from_tag 정보가 모두 없는 결측지 데이터 전처리
    : item_fit_from_tag [id, fit_from_tag] - tag에 있는 fit 정보가 담겨 있는 데이터프레임
    '''
    new_item = pd.merge(item, item_fit, how='left', on='id')
    new_item = pd.merge(new_item, item_fit_from_tag, how='left', on='id')
    no_both_fit = new_item[(new_item['fit'].isnull()) & (new_item['fit_from_tag'].isnull())]
    id_fit_list = []
    
    for item_id in tqdm(no_both_fit['id']):
        id_fit_list.append([item_id, '프리'])

    appended_item_fit = pd.DataFrame(id_fit_list, columns=['id', 'fit'])
    updated_item_fit = pd.concat([item_fit, appended_item_fit], ignore_index=True)
    return updated_item_fit.drop_duplicates().reset_index(drop=True)
