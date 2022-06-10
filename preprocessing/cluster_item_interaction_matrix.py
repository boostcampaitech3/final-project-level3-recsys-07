import pandas as pd
import numpy as np
import openpyxl

from collections import Counter
from itertools import permutations
from tqdm import tqdm


# path 지정
ITEM_CODI_ID_XLSX_PATH  = '/opt/ml/input/data/raw_codishop/view/item/item_codi_id.xlsx'
ITEM_CSV_PATH           = '/opt/ml/input/data/asset_codishop/view/item/item.csv'
OUTPUT_PATH             = '/opt/ml/input/data/asset_codishop/view/item/cluseter_item_interaction_matrix.csv'


# dataframe 불러오기
item_codi_df    = pd.read_excel(ITEM_CODI_ID_XLSX_PATH, engine='openpyxl')
item_df = pd.read_csv(ITEM_CSV_PATH)


# 불러온 dataframe 확인
print ("[1] 불러온 dataframe 정보 확인")
print (f"1. 악세서리를 제외한 전체 Item의 수 : {len(item_df)}")
print (f"2. 고유한 중분류의 수 : {len(item_df['mid_class'].unique())}")
print (f"3. 클러스터 ID의 개수 : {len(item_df['cluster_id'].unique())}")
print (f"4. 고유한 색상 ID의 수 : {len(item_df['color_id'].unique())}")


# item_codi_df 와 item_df 의 item 일치시키기
print (f"[2] 불러온 2개의 dataframe에 존재하는 item 목록 일치시키기")
drop_indexes = list()
items_in_item_df = list(item_df['id'].unique())
for i in range(len(item_codi_df)):
    if item_codi_df.iloc[i]["id"] not in items_in_item_df:
        drop_indexes.append(i)
item_codi_df = item_codi_df.drop(drop_indexes)


# 코디 내에서 가능한 아이템들의 조합을 계산하는 코드
print (f"[3] 각 코디내에서 가능한 아이템들의 조합 계산")
possible_combinations = list()
items_in_codi = item_codi_df.groupby('codi_id')['id'].apply(list)
for val in tqdm(items_in_codi):
    val = sorted(val)
    comb_res = list(permutations(val, 2))
    possible_combinations.extend(comb_res)


print (f"[4] 생성된 item-item 조합을 cluster-item 리스트로 변환")
pivot_list = list()
for item1, item2 in possible_combinations:
    cluster_id = item_df[item_df['id'] == item1]['cluster_id'].values
    pivot_list.append((cluster_id[0], item2))

count_combination = list(Counter(pivot_list).most_common())
result = list()
for (cluster_id, item_id), cnt in count_combination:
    result.append((cluster_id, item_id, cnt))


print (f"[5] cluster-item 상호작용 matrix 생성 및 저장")
CIM = pd.DataFrame(result, columns=["id", "item", "count"]).pivot_table(index="id", columns="item", values="count").fillna(0)
CIM = CIM.astype(int)
CIM.to_csv(OUTPUT_PATH, index=True)


print (f"[6] Sparsity 계산")
ones = 0
zeros = 0
for i in range(len(CIM)) :
    oz_cnt = CIM.iloc[i].value_counts()
    zeros += oz_cnt[0]
    ones += sum(oz_cnt[1:])
print(f"Sparsity of this Data is : {zeros / (ones + zeros):.4}")