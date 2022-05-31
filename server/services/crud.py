import pymysql
import yaml
from easydict import EasyDict
#여기에서 만들어둔 것을 main에서 사용
with open('./server/config.yaml') as f:
    config=yaml.load(f, Loader=yaml.FullLoader)
    config=EasyDict(config)
    print(config)
    item_db = pymysql.connect(
        user=config.mysql.user, 
        passwd=config.mysql.password, 
        host=config.mysql.host,  # GCP instance
        db=config.mysql.db, # 나중에 파일로 가져오기
        charset='utf8'
    )
    cursor = item_db.cursor(pymysql.cursors.DictCursor)
    print(cursor)
    sql='SELECT * FROM "item" where "id"=25868'
    # cursor.execute(sql, item_db) # error남
    cursor.close()