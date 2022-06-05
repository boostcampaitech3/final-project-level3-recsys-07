from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional,Dict,List

from server.services.crud import *
from models.Rule_based.rule_based import *

app = FastAPI()

class Item(BaseModel):
    item_id: list
    image_url: Optional[list]
    item_name: Optional[list]

class ItemIn(BaseModel):
    item_ids: List[int]

class ItemOut(BaseModel):
    item_ids: List
    img_url: Optional[List]
    item_name: Optional[List]

# TEST
@app.get("/")
def server_test():
    return {"server" : "test"}

# Item info id, name, img_url
@app.post('/items/info/', response_model=ItemOut)
async def read_images_url(item: ItemIn):
    return get_item_info(item.item_ids)

# recommendation from item_id
@app.get('/rule_base/recommendation/{item_id}')
def rule_base_recommendation(item_id : int):
    return get_item_recommendation(item_id)

# TODO : lightGCN recommendation
@app.get('/lightGCN/recommendation/{item_id}')
def lightGCN_recommendation(item_id : int):
    pass

# TODO : MultiVAE recommendation
@app.get('/MultiVAE/recommendation/{item_id}')
def MultiVAE_recommendation(item_id : int):
    pass

# 아이템의 옷 이름 가져오기
@app.post('/items/names/', response_model=Item)
async def read_clothes_name(item: Item):
    return get_clothes_name(item)

@app.get('/codi/')
def read_codi(select_item: int, pick_item: int):
    return get_codi(select_item,pick_item)

# 원하는 아이템을 고른 후 적절한 코디를 추천
@app.post('/codis/', response_model=ItemOut)
def read_codis_info(select_item: int, pick_item: int):
    return get_codi_images_url(select_item, pick_item)

# key word 검색
@app.get('/item/{key_word}')
def read_item_from_tag(key_word : str):
    return get_item_from_tag(key_word)

# 태그 리스트 가져오기
@app.get("/tags")
def read_item_tags():
    return get_item_tags()

# TODO : 추천된 코디 클릭시 implicit feedback 저장

# TODO : 만족도 평가 받기