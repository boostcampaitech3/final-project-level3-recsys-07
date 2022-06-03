from fastapi import FastAPI
from pydantic import BaseModel, Field
from .services.crud import *
from pydantic import BaseModel
from typing import Optional,Dict,List

app = FastAPI()

class Item(BaseModel):
    item_id: list
    image_url: Optional[list]
    item_name: Optional[list]

# TEST
@app.get("/")
def server_test():
    return {"server" : "test"}

# TODO : 아이템의 이미지 url 가져오기

@app.post('/items/images/')
async def read_images_url(item: Item)->dict:
    item_dict=item.dict()
    print('item_dict["item_id"]',item_dict['item_id'])
    # get_images_url(item_dict['item_id'])
    # print(s)
    return {'d':['25868','16']}

# TODO : 아이템의 옷 이름 가져오기
@app.post('/items/names/', response_model=Item)
async def read_clothes_name(item: Item):
    return get_clothes_name(item)

# TODO : 원하는 아이템을 고른 후 적절한 코디를 추천
@app.get('/codi/{codi_Id}')
def read_codi():
    pass

# TODO : 코디의 이미지 url 가져오기
@app.post('/codi/images')
def read_codi_image_url():
    pass

#key word 검색
@app.get('/item/{key_word}')
def read_item_from_tag(key_word : str):
    return get_item_from_tag(key_word)

# 태그 리스트 가져오기
@app.get("/tags")
def read_item_tags():
    return get_item_tags()

# TODO : 필요한 데이터셋 가져오기

# TODO : 추천된 코디 클릭시 implicit feedback 저장

# TODO : 만족도 평가 받기
