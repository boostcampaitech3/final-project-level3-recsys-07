import pymysql
import yaml
from easydict import EasyDict
from typing import Dict, List, Optional

from pydantic import BaseModel


with open('./server/config.yaml') as f:
    config=yaml.load(f, Loader=yaml.FullLoader)
    config=EasyDict(config)
    # print(config)
    db = pymysql.connect(
        user=config.mysql.user, 
        passwd=config.mysql.password, 
        host=config.mysql.host,  # GCP instance
        db=config.mysql.db, # 나중에 파일로 가져오기
        charset='utf8'
    )


def get_item_info(item_ids:List)->dict:
    '''
        item_ids : List[int]
        -> return id, name, img_url
    '''
    item_ids = tuple(item_ids)
    sql = f"SELECT id, name, img_url  FROM item WHERE id IN {item_ids}"
    cursor = db.cursor()
    cursor.execute(sql)
    
    result = cursor.fetchall()
    
    out = {"item_id" : [], "item_name" : [], 'img_url' : []}
    cursor.close()
    
    #tuple to dict
    for item in result:
        out['item_id'].append(item[0])
        out['item_name'].append(item[1])
        out['img_url'].append(item[2])
    
    return out 

def get_images_url(item_id:List)->List:
    sql=f"SELECT img_url FROM item WHERE id IN {item_id}"
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    
    result = cursor.fetchall()

    # print('result for images url',result)
    cursor.close()
    return result['img_url']

def get_clothes_name(item):

    item_id=tuple(item.item_id)
    sql=f"SELECT name FROM item where id IN {item_id}"
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    item.image_url=result['name']
    cursor.close()
    print('item',item)
    return item


def get_item_tags()-> List:
    sql = f"SELECT tag FROM item_tag"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    result = [item[0] for item in result]
    cursor.close()
    return result

def get_item_from_tag(tag : str)-> List:
    sql = f"SELECT id FROM item_tag WHERE tag = '{tag}'"
    
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    result = [item[0] for item in result]
    cursor.close()
    return result
