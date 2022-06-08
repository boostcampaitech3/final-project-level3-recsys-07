import numpy as np
import pandas as pd

interaction_PATH = "./resource/CCIM.csv"
item_PATH = "./resource/item.csv"
cluster_prob_PATH = "./resource/cluster_item_prob.csv"

interaction_matrix = pd.read_csv(interaction_PATH)
item_feature = pd.read_csv(item_PATH)
cluster_item_prob = pd.read_csv(cluster_prob_PATH)
item_feature = item_feature[["id","name","url", "likes", "big_class","mid_class", "cluster_id"]]
item_cluster_list = list(interaction_matrix.columns[1:])

def sort_item_by_likes(item_list : list) -> list :
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

def sort_item_by_prob(item_list : list, cluster_id : int) -> list :

    prob_list = list()
    result = list()

    for item in item_list :
        item_id = int(item)
        cluster_condition = (cluster_item_prob["cluster_id"] == cluster_id)
        item_condition = (cluster_item_prob["item_id"] == item_id)
        item_prob = cluster_item_prob.loc[cluster_condition & item_condition, "prob"].iloc[0]
        prob_list.append([item_prob, item_id])
    
    prob_list.sort(reverse=True)

    for item in prob_list :
        result.append(item[1])
    
    if len(result) > 10 :
        result = result[:10]

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
            rec_result[key] = sort_item_by_prob(rec_result[key], cluster_id)
    
    return rec_result
