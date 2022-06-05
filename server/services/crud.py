from sqlite3 import Cursor
import pymysql
import yaml
from easydict import EasyDict
from typing import Dict, List
import numpy as np

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
        -> dict {return id, name, img_url}
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
    sql= f"SELECT id, img_url FROM item WHERE id IN {item_id}"
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    
    result = cursor.fetchall()

    cursor.close()
    return result['img_url']

def get_codi(select_item:int, pick_item:int)->List:
    ids = (select_item,pick_item)
    sql= f"""
            SELECT id, codi_id 
            FROM item_codi_id 
            WHERE id IN {ids}
        """
    cursor = db.cursor()
    cursor.execute(sql)

    result = cursor.fetchall() # id, codi_id
    
    result = np.array(result) #[[id, codi_id]]
    # codi_id 등장 횟수 check
    unique, counts = np.unique(result[:,1], return_counts=True)

    result = np.asarray((unique, counts)).T

    # 2번 이상 등장한 codi_id check
    idx = np.where(result[:,1] >= 2)

    codi_ids = result[idx][:, 0]
    return codi_ids

def get_codi_images_url(codi_ids:List)->Dict:
    
    codi_ids=tuple(codi_ids)
    sql= f"SELECT id, img_url FROM codi WHERE id IN {codi_ids}"
    cursor = db.cursor()
    cursor.execute(sql)
    
    result = cursor.fetchall()
    
    out = {"codi_id" : [], 'img_url' : []}
    cursor.close()
    
    #tuple to dict
    for item in result:
        out['codi_id'].append(item[0])
        out['img_url'].append(item[1])
    
    return out

def get_clothes_name(item):

    item_id=tuple(item.item_id)
    sql=f"SELECT name FROM item where id IN {item_id}"
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    item.image_url=result['name']
    cursor.close()
    
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