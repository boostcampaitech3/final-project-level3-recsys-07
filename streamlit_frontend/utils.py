from turtle import st
import requests
from io import BytesIO
from PIL import Image
import json
from itertools import chain
from collections import defaultdict

import yaml
from easydict import EasyDict
with open('./config.yaml') as f:
    config=yaml.load(f, Loader=yaml.FullLoader)
    config=EasyDict(config)

BACKEND_SERVER = config.backend_url

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


def get_item_mid_class()->list:
    response_data = requests.get(url = BACKEND_SERVER + "/mid_class").json()
    response_data = list(set(response_data))  # set 제거하면 오름차순 정렬 가능
    return response_data


def get_mid_class_id(mid_class_list:list)->list:
    
    params = {"mid_class_list" : mid_class_list}
    params = json.dumps(params)
    response_data = requests.post(url = BACKEND_SERVER + "/items", data = params).json()

    return response_data


def get_tag_id(tag_list:list)->list:
    
    params = {"tag_list" : tag_list}
    params = json.dumps(params)
    response_data = requests.post(url = BACKEND_SERVER + "/items", data = params).json()

    return response_data


def get_image(url:str) -> Image:
    try:
        response = requests.get(url, stream=True)
        img = Image.open(BytesIO(response.content))
    except:
        response = requests.get("https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg", stream=True)
        img = Image.open(BytesIO(response.content))

    img = img.resize((500, 600), Image.ANTIALIAS) # ratio 5 : 6

    return img

def get_recommendation(item_id: int)-> dict:
    
    rec_result = {"상의" : [],"바지" : [],"아우터" : [], "신발" : [], "가방" : [], "모자" : []}

    #rule_base recommendation
    response = requests.get(url = BACKEND_SERVER + f"/rule_base/recommendation/{item_id}").json()
    rule_base_result = response

    # response = requests.get(url = BACKEND_SERVER + f"/lightGCN/recommendation/{item_id}").json()
    # lightGCN_result = response

    #TODO : append
    # for k, v in chain(dict1.items(), dict2.items()):
    #     rec_result[k].append(v)
    # for k,v in lightGCN_result.items():

    return rule_base_result
    # return lightGCN_result

def cluster_id(item_id:int):
    response_data = requests.get(url = BACKEND_SERVER + f"/item/cluster/{item_id}").json()
    return response_data

def get_prob_info(cluster_id:int,item_ids: list) -> dict:
    params = {"cluster_id" : cluster_id, "item_ids" : item_ids}
    params = json.dumps(params)
    response_data = requests.post(url = BACKEND_SERVER + "/items/prob/", data = params).json()
    item_dict = response_data
    return item_dict