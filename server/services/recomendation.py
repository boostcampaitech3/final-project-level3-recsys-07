import pandas as pd
import numpy as np

from models.Rule_based.rule_based import *
from server.services.crud import *

'''
    구현된 추천 결과를 dict type로 반환
    {"상의" : [],"바지" : [],"아우터" : [], "신발" : [], "가방" : [], "모자" : []}

'''

LIGHTGCN_PROB_PATH = "./resource/cluster_item_prob.csv"
PROB_DATA = pd.read_csv(LIGHTGCN_PROB_PATH)

def get_rulebase_recommendation(item_id:int)-> dict:
    rule_base_rec = get_item_recommendation(item_id)
    return rule_base_rec
    

def get_lightGCN_recommendation(item_id:int)-> dict:
    print("lightGCN in")
    # GET CLUSTER ID
    cluster_id = get_cluster_id(item_id)

    TEMP_DATA = PROB_DATA[PROB_DATA['cluster_id'] == cluster_id]
    TEMP_DATA.sort_values(by=['prob'], ascending=False, ignore_index=True, inplace = True)
    item_ids = TEMP_DATA["item_id"].head(20).values
    
    # GET ITEM INFO
    item_info = get_item_info(item_ids)

    # item dict
    item_dict = {"상의" : [],"바지" : [],"아우터" : [], "신발" : [], "가방" : [], "모자" : []}
    
    for idx in range(0, 20):
        if item_info['item_ids'][idx] == item_id:
            continue
        _big_class = item_info['big_class'][idx]
        _item_id = item_info['item_ids'][idx]
        # _name = item_info['item_name'][idx]
        # _img_url = item_info['img_url'][idx]
        item_dict[_big_class].append(_item_id)

    return item_dict
