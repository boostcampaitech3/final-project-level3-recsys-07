import pymysql
import yaml
from easydict import EasyDict
from typing import List

#여기에서 만들어둔 것을 main에서 사용
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

def get_images_url(item_id:str)->str:
    sql=f"SELECT img_url FROM item where id = {item_id}"
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result[0]['img_url']

def get_clothes_name(item_id:str)->str:
    sql=f"SELECT name FROM item where id = {item_id}"
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    print(result)
    return result[0]['name']


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