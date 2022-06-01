from fastapi import FastAPI
from pydantic import BaseModel, Field
from .services.crud import *

app = FastAPI()

# TODO : DB 연결

# TEST
@app.get("/")
def server_test():
    return {"server" : "test"}

# TODO : 아이템의 이미지 url 가져오기

@app.get('/item/images/{item_id}')
def read_images_url(item_id : str):
    return get_images_url(item_id)

# TODO : 아이템의 옷 이름 가져오기
@app.get('/item/names/{item_id}')
def read_clothes_name(item_id:str):
    return get_clothes_name(item_id)

# TODO : 원하는 아이템을 고른 후 적절한 코디를 추천
@app.get('/codi/{codi_Id}')
def read_codi():
    pass

# TODO : 코디의 이미지 url 가져오기
@app.post('/codi/images')
def read_codi_image_url():
    pass

# TODO : key word 검색
@app.get('/item/{key_word}')
def read_item_recommendation():
    pass

# TODO : 태그 리스트 가져오기
@app.get("/tags")
def read_item_tags():
    pass

# TODO : 필요한 데이터셋 가져오기

# TODO : 추천된 코디 클릭시 implicit feedback 저장

# TODO : 만족도 평가 받기
