import numpy as np
import pandas as pd

interaction_PATH = "/opt/ml/input/data/itemInteractionMatrix.csv"
item_PATH = "/opt/ml/workspace/crawler/item_crawler_ver2/total_asset/item.xlsx"

interaction_matrix = pd.read_csv("/opt/ml/workspace/model/Rule Based/IIM.csv")
item_feature = pd.read_csv("/opt/ml/workspace/model/Rule Based/item.csv")
item_feature = item_feature[["id","name","url", "likes", "big_class","mid_class", "cluster_id"]]
item_cluster_list = list(interaction_matrix.columns[1:])

def sort_rec_item(item_list : list) -> list :
    likes_list = list()
    result = list()

    for item in item_list : 
        item_id = int(item)
        item_likes = item_feature[item_feature["id"]==item_id]["likes"].iloc[0]
        likes_list.append([item_likes, item_id])
    
    likes_list.sort(reverse=True)
    for item in likes_list :
        result.append(item[1])

    return result

def get_item_reccomendation(item_id)-> dict :

    cluster_id = int(item_feature.loc[item_feature["id"]==item_id]["cluster_id"])
    data = interaction_matrix[interaction_matrix["id"]==cluster_id]
    data = data.to_numpy()[0][1:] 

    index_list = list()
    for i in range(len(data)) :
        if data[i] != 0 :
            index_list.append(i)

    rec_result = {"상의" : [], "바지" : [], "아우터" : [], "신발" : [], "가방" : [], "모자" : []}
    for index in index_list :
        rec_cluster_id = item_cluster_list[index]
        rec_item_info = item_feature.loc[item_feature["cluster_id"]==int(rec_cluster_id), "id"]

        for id in rec_item_info :
            big_class = item_feature.loc[item_feature["id"]==id, "big_class"].iloc[0]
            name = item_feature.loc[item_feature["id"]==id, "name"].iloc[0]
            url = item_feature.loc[item_feature["id"]==id, "url"].iloc[0]
            rec_result[big_class].append(id)

    for key in rec_result.keys() :

        if len(rec_result[key]) > 0:
            rec_result[key] = sort_rec_item(rec_result[key])
    
    return rec_result

