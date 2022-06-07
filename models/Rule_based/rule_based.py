import numpy as np
import pandas as pd

interaction_PATH = "/opt/ml/input/data/asset_codishop/itemInteractionMatrix.csv"
item_PATH = "/opt/ml/input/data/asset_codishop/view/item/item.csv"

interaction_matrix = pd.read_csv(interaction_PATH)
item_feature = pd.read_csv(item_PATH)
item_feature = item_feature[["id","name","url", "likes", "big_class","mid_class"]]
item_id_list = list(interaction_matrix.columns[1:])

def sort_rec_item(item_list : list) -> list :
    likes_list = list()
    result = list()

    for item in item_list : 
        item_id = int(item[0])
        item_likes = item_feature[item_feature["id"]==item_id]["likes"].iloc[0]
        likes_list.append([item_likes, item_id])
    
    likes_list.sort(reverse=True)
    for item in likes_list :
        result.append(item[1])

    return result

def data_preprocessing(item_feature : pd.DataFrame) -> None :
    upper = ["상의", "기타 상의"]
    lower = ["바지", "하의"]
    outer = ["아우터"]
    shoes = ["스니커즈", "신발", "스포츠신발"]
    accessory = ["선글라스/안경테", "액세서리", "주얼리", "시계", "가방", "여성 가방", "모자", "스포츠모자", "스포츠가방"]
    etc = ["양말/레그웨어", "디지털/테크", "뷰티", "속옷", "디지털/테크"]

    actual_big_class_list = list()
    for i in range(len(item_feature)) :
        item_info = item_feature.iloc[i]
        id = item_info["id"]
        big = item_info["big_class"]
        mid = item_info["mid_class"]
        if big in upper or mid in upper :
            actual_big_class = "상의"
        elif big in lower or mid in lower :
            actual_big_class = "하의"
        elif big in outer or mid in outer :
            actual_big_class = "아우터"
        elif big in shoes or mid in shoes :
            actual_big_class = "신발"
        elif big in accessory or mid in accessory :
            actual_big_class = "액세서리"
        else : 
            actual_big_class = "기타"
        actual_big_class_list.append(actual_big_class)

    item_feature["my_big_class"] = actual_big_class_list
    item_feature["likes"] = item_feature["likes"].fillna(0)

def get_item_recommendation(item_id)-> None :
    data_preprocessing(item_feature=item_feature)
    
    data = interaction_matrix[interaction_matrix["id"]==item_id]
    data = data.to_numpy()[0][1:] 

    index_list = list()
    for i in range(len(data)) :
        if data[i] != 0 :
            index_list.append(i)

    rec_result = {"상의" : [], "하의" : [], "아우터" : [], "신발" : [], "액세서리" : [], "기타" : []}
    for index in index_list :
        rec_item_id = item_id_list[index]
        rec_item_info = item_feature[item_feature["id"]==int(rec_item_id)]

        big_class = rec_item_info["my_big_class"].iloc[0]
        name = rec_item_info["name"].iloc[0]
        url = rec_item_info["url"].iloc[0]

        rec_result[big_class].append((rec_item_id, name, url))

    for key in rec_result.keys() :

        if len(rec_result[key]) > 0:
            rec_result[key] = sort_rec_item(rec_result[key])
    
    return rec_result
