import streamlit as st
import numpy as np
import pandas as pd

ITEM_PATH = "/opt/ml/input/data/raw_codishop/item.xlsx"
ITEM_DATA = pd.read_excel(ITEM_PATH,engine='openpyxl')
CODI_ITEM_PATH= "/opt/ml/input/data/raw_codishop/codi_item_id.xlsx"
CODI_ITEM_DATA = pd.read_excel(CODI_ITEM_PATH,engine='openpyxl')
CODI_PATH='/opt/ml/input/data/raw_codishop/codi.xlsx'
CODI_DATA=pd.read_excel(CODI_PATH,engine='openpyxl')

def get_images_url(item_ids: list) -> dict:
    image_dict = dict()
    
    for id in item_ids:
        image_dict[id] = ITEM_DATA[ITEM_DATA['id'] == id]['img_url'].unique().tolist()[0]
    
    return image_dict

def get_clothes_name(item_id: int) -> str:
    name = ITEM_DATA[ITEM_DATA['id'] == item_id]['name'].values[0]
    return name

def get_codi(select_item:int,pick_item:int):
    codi_data=CODI_ITEM_DATA.groupby('id')['item_id'].apply(list)

    codi_ids=list()
    for i in range(len(codi_data)):
        is_in = False
        if pick_item in codi_data.iloc[i]:
            is_in = True
        if is_in:
            if select_item in codi_data.iloc[i]:
                codi_ids.append(codi_data.index[i])
    return codi_ids

def get_codi_images_url(codi_ids:list):
    codi_dict=dict()

    for id in codi_ids:
        codi_dict[id]=CODI_DATA[CODI_DATA['id'] == id]['img_url'].tolist()[0]

    return codi_dict