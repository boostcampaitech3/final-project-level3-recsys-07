import numpy as np
import pandas as pd
import os


def class_preprocess(raw_item_data) :

    base_big_class = ['아우터', '상의', '바지', '가방', '신발', '모자']
    df = raw_item_data[["id", "big_class", "mid_class"]]

    # 전처리 
    for mid_class in ['캔버스/단화', '패션스니커즈화', '기타 스니커즈', '농구화'] :
        df.loc[df["mid_class"]==mid_class, "big_class"] = "신발"

    for mid_class in ['안경', '선글라스', '양말', '팔찌', '반지', '목걸이/펜던트', '발찌', '스포츠잡화', '디지털', '쿼츠 아날로그', '오토매틱 아날로그', '카메라/카메라용품', '우산'] :
        df.loc[df["mid_class"]==mid_class, "big_class"] = "액세서리"

    df.loc[df["mid_class"]=="스포츠신발", "big_class"] = "신발"

    for mid_class in ["스포츠가방",'백팩', '크로스백'] :
        df.loc[df["mid_class"]==mid_class, "big_class"] = "가방"

    # 전처리한 대분류, 중분류 원 데이터에 반영
    raw_item_data["big_class"] = df["big_class"]
    raw_item_data["mid_class"] = df["mid_class"]

    # 액세서리, 속옷 대분류 제거 
    accessory_index = raw_item_data[raw_item_data["big_class"]=="액세서리"].index
    underwear_index = raw_item_data[raw_item_data["big_class"]=="속옷"].index
    raw_item_data.drop(accessory_index, inplace=True)
    raw_item_data.drop(underwear_index, inplace=True)

    # 출력 엑셀의 형식을 원래 데이터의 형식과 동일하게 맞춰주기 위한 부분
    raw_item_data["id"] = raw_item_data["id"].apply(str)

    # 한번도 보지 못한 대분류 아이템 제거
    unique_big_class = list(raw_item_data["big_class"].unique())
    new_big_class = list(set(unique_big_class) - set(base_big_class))

    need_revision_total_df = pd.DataFrame([], columns=list(raw_item_data.columns))
    for new_class in new_big_class :
        need_revision_df = raw_item_data.loc[raw_item_data["big_class"]==new_class]
        need_revision_total_df = pd.concat([need_revision_total_df, need_revision_df])

        left_out_index = need_revision_df.index
        raw_item_data.drop(left_out_index, inplace=True)

    need_revision_total_df["revision"] = ["big_class"] * len(need_revision_total_df)

    return raw_item_data, need_revision_total_df