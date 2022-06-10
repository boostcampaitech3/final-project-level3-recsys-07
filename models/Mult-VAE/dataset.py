import os
import pandas as pd
from scipy import sparse
import numpy as np

def get_count(tp, id):
    playcount_groupbyid = tp[[id]].groupby(id, as_index=False)
    # raw_data[["item"]].groupby("item", as_index=False) 
    # raw_data["item"] -> series 반환
    # raw_data[["item"]] -> dataframe 반환
    # raw_data[["user"]].groupby("user", as_index=False)
    count = playcount_groupbyid.size() # count = 유저/아이템 별 리뷰 개수
    return count

# 특정한 횟수 이상의 리뷰가 존재하는(사용자의 경우 min_uc 이상, 아이템의 경우 min_sc이상) 
# 데이터만을 추출할 때 사용하는 함수입니다.
# 현재 데이터셋에서는 결과적으로 원본그대로 사용하게 됩니다.
def filter_triplets(tp, min_uc=5, min_sc=0):
    if min_sc > 0:
        itemcount = get_count(tp, 'item')
        tp = tp[tp['item'].isin(itemcount.index[itemcount >= min_sc])]

    if min_uc > 0:
        usercount = get_count(tp, 'user')
        tp = tp[tp['user'].isin(usercount.index[usercount >= min_uc])]

    usercount, itemcount = get_count(tp, 'user'), get_count(tp, 'item')
    return tp, usercount, itemcount

#훈련된 모델을 이용해 검증할 데이터를 분리하는 함수입니다.
#100개의 액션이 있다면, 그중에 test_prop 비율 만큼을 비워두고, 그것을 모델이 예측할 수 있는지를
#확인하기 위함입니다.
def split_train_test_proportion(data, test_prop=0.5):
    data_grouped_by_user = data.groupby('user')
    tr_list, te_list = list(), list()

    np.random.seed(98765)
    
    for _, group in data_grouped_by_user: # user_id, user가 시청한 영화 data (user, item, time) 형식으로 반환됨

        n_items_u = len(group) # 유저가 시청한 영화의 개수
        print(n_items_u)
        if n_items_u >= 5: # 시청한 영화의 개수가 5개 이상이라면
            idx = np.zeros(n_items_u, dtype='bool') # dataframe은 boolean 값으로 indexing 할 수 있다
            idx[np.random.choice(n_items_u, size=int(test_prop * n_items_u), replace=False).astype('int64')] = True
            # test_prop = 0.2 : 시청한 영화 중 20%를 따로 빼 놓은다. 
            # np.random.choice(a, size, replace) a가 array라면 array안에서 원소를 무작위 추출, a가 자연수라면 0 ~ a 사이 값 중에 무작위 추출
            tr_list.append(group[np.logical_not(idx)])
            te_list.append(group[idx])
        
        else: #만약 시청한 영화의 수가 5개 미만이라면 split하지 않는다.
            tr_list.append(group)
    
    data_tr = pd.concat(tr_list) # tr_list 안에 (user, item, time) dataframe이 여러 개 담겨져 있는 2차원 배열인데, 안에 있는 dataframe들을 열 기준으로 합쳐준다.
    data_te = pd.concat(te_list) # 만약 axis=1로 설졍해주면 행 기준으로 concat 해준다.

    return data_tr, data_te

def numerize(tp, profile2id, show2id): # id to index
    uid = tp['user'].apply(lambda x: profile2id[x])
    sid = tp['item'].apply(lambda x: show2id[x])
    return pd.DataFrame(data={'uid': uid, 'sid': sid}, columns=['uid', 'sid'])


