import numpy as np
import pandas as pd

def buy_age_preprocess(item_data : pd.DataFrame) -> pd.DataFrame :
    
    buy_age_data = pd.read_excel("/opt/ml/input/data/raw_codishop/view/item/item_buy_age.xlsx")

    most_bought_age_dict = dict()
    for i in range(len(buy_age_data)) :
        user_id = buy_age_data["id"].iloc[i]
        user_data = buy_age_data.iloc[i].drop("id")
        index = user_data.argmax()
        most_bought_age_dict[user_id] = index

    most_bought_age_list = list()
    for user in item_data["id"] :
        try :
            most_bought_age_list.append(most_bought_age_dict[user])
        except :
            most_bought_age_list.append(6)

    item_data["most_bought_age_class"] = most_bought_age_list

    return item_data