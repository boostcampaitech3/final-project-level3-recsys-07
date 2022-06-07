import requests
from io import BytesIO
from PIL import Image
import json
from itertools import chain
from collections import defaultdict

BACKEND_SERVER = "http://127.0.0.1:8001" #http://34.82.21.15:8001/

def get_image_url(item_id: int) -> dict:

    response_data = requests.get(url = BACKEND_SERVER + f"/item/image/{item_id}").json()
    return response_data

def get_item_info(item_ids: list) -> dict:

    params = {"item_ids" : item_ids}
    
    params = json.dumps(params)
    response_data = requests.post(url = BACKEND_SERVER + "/items/info/", data = params).json()
    item_dict = response_data

    return item_dict

def get_codi(select_item:int,pick_item:int):
    response_data = requests.get(url = BACKEND_SERVER + f"/codi?select_item={select_item}&pick_item={pick_item}").json()
    
    codi_ids = response_data
    return codi_ids

def get_codi_info(codi_ids:list):
    params = {"item_ids" : codi_ids}
    
    params = json.dumps(params)
    response_data = requests.post(url = BACKEND_SERVER + "/codis/info", data = params).json()
    codi_dict = response_data

    return codi_dict

def get_item_tags()->list:
    response_data = requests.get(url = BACKEND_SERVER + "/tags").json()
    response_data = list(set(response_data))
    return response_data

def get_tag_id(tag_list:list)->list:
    
    params = {"tag_list" : tag_list}
    params = json.dumps(params)
    response_data = requests.post(url = BACKEND_SERVER + "/items", data = params).json()

    return response_data


def get_image(url:str) -> Image:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    img = img.resize((500, 600), Image.ANTIALIAS) # ratio 5 : 6

    return img

def get_recommendation(item_id: int)-> dict:
    
    rec_result = {"상의" : [],"바지" : [],"아우터" : [], "신발" : [], "가방" : [], "모자" : []}

    #rule_base recommendation
    # response = requests.get(url = BACKEND_SERVER + f"/rule_base/recommendation/{item_id}").json()
    # rule_base_result = response

    response = requests.get(url = BACKEND_SERVER + f"/lightGCN/recommendation/{item_id}").json()
    lightGCN_result = response

    #TODO : append
    # for k, v in chain(dict1.items(), dict2.items()):
    #     rec_result[k].append(v)
    # for k,v in lightGCN_result.items():

    return lightGCN_result

def cluster_id(item_id:int):
    response_data = requests.get(url = BACKEND_SERVER + f"/item/cluster/{item_id}").json()
    return response_data