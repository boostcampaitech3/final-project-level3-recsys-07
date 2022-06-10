import os
import openpyxl
import pandas as pd

from ..utils_item import *
from ..utils_item_fit import *
from ..utils_item_four_season import *

# !important: path parameter
_PREPROCESS = 'raw'
_STORE_OPTION = 'codishop'
_SORT_OPTION = 'view'

ITEM_PATH = f'/opt/ml/input/data/{_PREPROCESS}_{_STORE_OPTION}/{_SORT_OPTION}/item/'
CODI_PATH = f'/opt/ml/input/data/{_PREPROCESS}_{_STORE_OPTION}/{_SORT_OPTION}/codi/'
SAVE_ITEM_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/item/'
SAVE_CODI_PATH = f'/opt/ml/input/data/asset_{_STORE_OPTION}/{_SORT_OPTION}/codi/'


# age 전처리
def preprocess_item_by_age():
    print ("Doing preproces_item_by_age..")

    item = pd.read_csv(SAVE_ITEM_PATH + "item.csv")
    item_buy_age = pd.read_excel(ITEM_PATH + "item_buy_age.xlsx", engine='openpyxl')

    # -- buy age 데이터 전처리
    item_buy_age = synchronize_with_item(item=item, raw_data=item_buy_age)

    # -- preprocessed data save
    item_buy_age.to_csv(SAVE_ITEM_PATH + "item_buy_age.csv", index=False)


# gender 전처리
def preprocess_item_by_gender():
    print ("Doing preprocess_item_by_gender..")

    item = pd.read_csv(SAVE_ITEM_PATH + "item.csv")
    item_buy_gender = pd.read_excel(ITEM_PATH+"item_buy_gender.xlsx", engine='openpyxl')

    # -- buy gender 데이터 전처리
    item_buy_gender = synchronize_with_item(item=item, raw_data=item_buy_gender)

    # -- preprocessed data save
    item_buy_gender.to_csv(SAVE_ITEM_PATH + "item_buy_gender.csv", index=False)


# item - codi 전처리
def preprocess_item_codi_id():
    print ("Doing preprocess_item_codi_id..")

    item = pd.read_csv(SAVE_ITEM_PATH + "item.csv")
    item_codi_id = pd.read_excel(ITEM_PATH + "item_codi_id.xlsx", engine='openpyxl')

    # -- tag 데이터 전처리
    item_codi_id = synchronize_with_item(item=item, raw_data=item_codi_id)

    # -- preprocessed data save
    item_codi_id.to_csv(SAVE_ITEM_PATH + "item_codi_id.csv", index=False)


# fit 전처리
def preprocess_item_fit():
    print ("Doing preprocess_item_fit..")

    item = pd.read_csv(SAVE_ITEM_PATH + "item.csv")
    item_fit = pd.read_excel(ITEM_PATH + "item_fit.xlsx", engine='openpyxl')
    item_tag = pd.read_excel(ITEM_PATH + "item_tag.xlsx", engine='openpyxl')

    # -- fit 데이터 전처리
    item_fit = synchronize_with_item(item=item, raw_data=item_fit)
    item_fit_from_tag = make_item_fit_from_tag(item_tag=item_tag)
    item_fit = transform_fit_from_tag_to_fit(item, item_fit, item_fit_from_tag)
    item_fit = preprocessing_null_fit_data(item, item_fit, item_fit_from_tag)

    # -- preprocessed data save
    item_fit.to_csv(SAVE_ITEM_PATH + "item_fit.csv", index=False)


# four_season 전처리
def preprocess_four_season():
    print ("Doing preprocess_four_season..")

    item = pd.read_csv(SAVE_ITEM_PATH + "item.csv")
    item_four_season = pd.read_excel(ITEM_PATH + "item_four_season.xlsx", engine='openpyxl')

    # -- four season 데이터 전처리
    item_four_season = synchronize_with_item(item=item, raw_data=item_four_season)
    item_four_season = transform_season_to_four_season(item, item_four_season)
    item_four_season = preprocessing_null_season_data(item, item_four_season)

    # -- preprocessed data save
    item_four_season.to_csv(SAVE_ITEM_PATH + "item_four_season.csv", index=False)


# 연결 codi_url 전처리
def preprocess_item_relative_codi_url():
    print ("Doing preprocess_item_relative_codi_url..")

    item = pd.read_csv(SAVE_ITEM_PATH + "item.csv")
    item_rel_coid_url = pd.read_excel(ITEM_PATH + "item_rel_codi_url.xlsx", engine='openpyxl')

    # -- related codi url 데이터 전처리
    item_rel_coid_url = synchronize_with_item(item=item, raw_data=item_rel_coid_url)

    # -- preprocessed data save
    item_rel_coid_url.to_csv(SAVE_ITEM_PATH + "item_rel_codi_url.csv", index=False)


# item tag 전처리
def preprocess_item_tag():
    print ("Doing preprocess_item_tag..")

    item = pd.read_csv(SAVE_ITEM_PATH + "item.csv")
    item_tag = pd.read_excel(ITEM_PATH + "item_tag.xlsx", engine='openpyxl')

    # -- tag 데이터 전처리
    item_tag = synchronize_with_item(item=item, raw_data=item_tag)

    # -- preprocessed data save
    item_tag.to_csv(SAVE_ITEM_PATH + "item_tag.csv", index=False)


# 전체적인 item.csv 전처리
def preprocess_item_basic():
    print ("Doing preprocess_item_basic..")
    
    raw_data = pd.read_excel(os.path.join(ITEM_PATH, "item.xlsx"), engine='openpyxl')

    # -- 데이터 전처리
    preprocessed_data, need_revision_data = class_preprocess(raw_data)
    preprocessed_data = likes_preprocess(preprocessed_data)
    preprocessed_data = color_preprocess(preprocessed_data)
    preprocessed_data = rating_preprocess(preprocessed_data)
    preprocessed_data = gender_preprocess(preprocessed_data)
    preprocessed_data = season_preprocess(preprocessed_data)
    preprocessed_data = view_preprocess(preprocessed_data)
    preprocessed_data = cum_sale_preprocess(preprocessed_data)
    preprocessed_data = buy_age_preprocess(preprocessed_data, ITEM_PATH)
    preprocessed_data = buy_gender_preprocess(preprocessed_data, ITEM_PATH)
    preprocessed_data = color_class_preprocess(preprocessed_data)
    preprocessed_data = mid_class_preprocess(preprocessed_data)
    preprocessed_data = cluster_preprocess(preprocessed_data)

    if os.path.exists(SAVE_ITEM_PATH) == False:
        os.makedirs(SAVE_ITEM_PATH)

    preprocessed_data.to_csv(os.path.join(SAVE_ITEM_PATH, "item.csv"), index=False)