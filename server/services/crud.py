from sqlite3 import Cursor
import pymysql
import yaml
from easydict import EasyDict
from typing import Dict, List
import numpy as np

with open('./server/config.yaml') as f:
    config=yaml.load(f, Loader=yaml.FullLoader)
    config=EasyDict(config)

def get_db(config):
    
    db = pymysql.connect(
        user=config.mysql.user, 
        passwd=config.mysql.password, 
        host=config.mysql.host,  # GCP instance
        db=config.mysql.db, # 나중에 파일로 가져오기
        charset='utf8'
    )
    return db
    


def get_item_info(item_ids:List)->dict:
    '''
        item_ids : List[int]
        -> dict {return id, name, img_url, big_class}
    '''
    item_ids = tuple(item_ids)
    
    if len(item_ids) == 1:
        item_ids = "('" + str(item_ids[0]) + "')"
    else:
        item_ids = tuple(item_ids)

    sql = f"SELECT id, name, img_url, big_class, url FROM item WHERE id IN {item_ids}"
    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    finally:
        db.close()
    
    out = {"item_ids" : [], "item_name" : [], 'img_url' : [], 'big_class' : [], 'item_url': []}
    #tuple to dict
    for item in result:
        out['item_ids'].append(item[0])
        out['item_name'].append(item[1])
        out['img_url'].append(item[2])
        out['big_class'].append(item[3])
        out['item_url'].append(item[4])
    
    return out 

def get_image_url(item_id:int)->str:
    sql= f"SELECT img_url FROM item WHERE id = {item_id}"
    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)
        
        result = cursor.fetchall()
    finally:
        db.close()

    return result[0]


def get_codi(select_item:int, pick_item:int)->list:

    select_cluster = get_cluster_id(select_item)
    pick_cluster = get_cluster_id(pick_item)

    sql= f"""
            SELECT DISTINCT ct1.codi_id
            FROM(
		            SELECT codi_id
		            FROM item i left outer join item_codi_id ici on i.id = ici.id
		            WHERE i.cluster_id = {select_cluster}
	            ) ct1,
	            (
                    SELECT codi_id
                    FROM item i left outer join item_codi_id ici on i.id = ici.id
                    WHERE i.cluster_id = {pick_cluster}
	            ) ct2
            WHERE ct1.codi_id = ct2.codi_id
        """
    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)

        result = cursor.fetchall() # codi_id
    finally:
        db.close()
    
    result = np.array(result)  # [codi_id, ....]
    result = result[:,0].tolist()

    return result

def get_codi_info(codi_ids:List)->dict:

    codi_ids=tuple(codi_ids)

    if len(codi_ids) == 1:
        codi_ids = "('" + str(codi_ids[0]) + "')"
    else:
        codi_ids = tuple(codi_ids)
    sql= f"SELECT id, img_url, style, url FROM codi WHERE id IN {codi_ids}"
    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

    finally:
        db.close()

    out = {"item_ids" : [], "item_name" : [], 'img_url' : [], 'item_url': []}

    #tuple to dict
    for item in result:
        out['item_ids'].append(item[0])
        out['img_url'].append(item[1])
        out['item_name'].append(item[2])
        out['item_url'].append(item[3])

    return out

def get_clothes_name(item):

    item_id=tuple(item.item_id)
    sql=f"SELECT name FROM item where id IN {item_id}"
    try:
        db = get_db(config)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        result = cursor.fetchall()
    finally:
        db.close()
    
    item.image_url=result['name']
    
    return item

def get_item_mid_class()-> list:
    sql = f"""
            SELECT DISTINCT mid_class 
            FROM item 
            ORDER BY mid_class 
           """
    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        result = [item[0] for item in result]
    finally:
        db.close()
    
    return result

def get_item_tags()-> list:
    sql = f"SELECT tag FROM item_tag ORDER BY tag"
    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        result = [item[0] for item in result]
    finally:
        db.close()

    return result


def get_item_from_tag(tag_list : list)-> list:
    
    if len(tag_list) == 1:
        tag_list = "('" + tag_list[0] + "')"
    else:
        tag_list = tuple(tag_list)
    sql = f"SELECT id FROM item_tag WHERE tag IN {tag_list}"

    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        result = [item[0] for item in result]
    finally:
        db.close()

    return result


def get_item_from_mid_class(mid_class_list : list)-> list:
    
    if len(mid_class_list) == 1:
        mid_class_list = "('" + mid_class_list[0] + "')"
    else:
        mid_class_list = tuple(mid_class_list)
    sql = f"SELECT id FROM item WHERE mid_class IN {mid_class_list}"
    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        result = [item[0] for item in result]
    finally:
        db.close()

    return result

def get_cluster_id(item_id:int)-> int:

    sql = f"SELECT cluster_id FROM item WHERE id = {item_id}"
    
    try:
        db = get_db(config)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        result = result[0]
    finally:
        db.close()
    
    return result