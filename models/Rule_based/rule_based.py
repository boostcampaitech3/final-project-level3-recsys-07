import numpy as np
import openpyxl
import pandas as pd

interaction_PATH = "/opt/ml/input/data/asset_codishop/view/item/itemInteractionMatrix_withColor.csv"
item_PATH = "/opt/ml/input/data/asset_codishop/view/item/item.xlsx"

interaction_matrix = pd.read_csv(interaction_PATH)
item_feature = pd.read_excel(item_PATH, engine="openpyxl")
item_feature = item_feature[["id","name","url", "likes", "big_class", "mid_class", "cluster_id"]]
item_id_list = list(interaction_matrix.columns[1:])

def sort_rec_item(item_list : list) -> list :
    likes_list = list()
    result = list()

    for item in item_list : 
        item_id = int(item[0])
        item_likes = item_feature[item_feature["id"] == item_id]["likes"].iloc[0]
        likes_list.append([item_likes, item_id])
    
    likes_list.sort(reverse=True)
    for item in likes_list :
        result.append(item[1])

    return result


def get_item_reccomendation(item_id) -> None :
    cluster_id = item_feature[item_feature["id" == item_id]]["cluster_id"]
    data = interaction_matrix[interaction_matrix["id"] == int(cluster_id)]
    data = data.columns.to_numpy()[1:] 

    index_list = list()
    for i in range(len(data)) :
        if data[i] != 0 :
            index_list.append(i)

    rec_result = {"상의" : [], "하의" : [], "아우터" : [], "신발" : [], "가방" : [], "모자" : []}
    for index in index_list :
        rec_item_id = item_id_list[index]
        rec_item_info = item_feature[item_feature["id"]==int(rec_item_id)]

        big_class = rec_item_info["big_class"].iloc[0]
        name = rec_item_info["name"].iloc[0]
        url = rec_item_info["url"].iloc[0]

        rec_result[big_class].append((rec_item_id, name, url))

    for key in rec_result.keys() :

        if len(rec_result[key]) > 0:
            rec_result[key] = sort_rec_item(rec_result[key])
    
    return rec_result
