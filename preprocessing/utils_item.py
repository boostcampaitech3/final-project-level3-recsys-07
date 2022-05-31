import openpyxl
import colorgram
import requests
import warnings
import re

import pandas as pd

from rembg import remove
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from typing import List
import json

warnings.filterwarnings(action='ignore')


def synchronize_with_item(item:pd.DataFrame, raw_data: pd.DataFrame) -> pd.DataFrame:
    '''
    전처리 된 item의 id와 현재 raw_data의 item id를 동기화
    대분류 전처리에서 drop 했던 item id를 제거
    : raw_data - item feature list dataframe (ex. item_fit, item_tag, item_four_season, ...)
    '''
    item_ids = item['id'].unique()
    new_data_list = []

    for item_id in tqdm(item_ids):
        data = raw_data[raw_data['id']==item_id].values.tolist()
        if data:
            new_data_list.extend(data)

    return pd.DataFrame(new_data_list, columns=raw_data.columns)


def get_img_from_url(url: str) -> Image:
    """
    url을 통해서 imgae를 풀러오는 함수
    반환형태는 PIL 이미지
    """
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def topK_colors(img: Image, k: int) -> List:
    """
    현재 img 에 포함된 상위 K개의 색상을 가져오기
    K개의 색상을 추출할 수 없을 때는, 추출된 색상 개수만큼 진행
    """
    colors = colorgram.extract(img, k)
    rgb_lists = list()

    for idx in range(min(k, len(colors))):
        R = colors[idx].rgb.r
        G = colors[idx].rgb.g
        B = colors[idx].rgb.b
        rgb_lists.append([R, G, B])

    return rgb_lists


def color_preprocess(item_df: pd.DataFrame) -> pd.DataFrame:
    """
    현재 이미지가 어떤 색을 가지고 있는지 처리하는 color main function
    item_df에 R, G, B 속성을 추가하여 반환

    현재 이미지를 로드할 수 없는 경우, 검정색을 넣도록 지시
    """
    color_r = list()
    color_g = list()
    color_b = list()

    # 이미지에서 색 추출 과정s
    for img_url in tqdm(item_df['img_url']):
        try:
            img = get_img_from_url(img_url)
        except:
            print (f"Failed to load img {img_url}")
            color_r.append("0")
            color_g.append("0")
            color_b.append("0")
            continue

        img = img.resize((240, 320))        # 이미지 크기 조정 (속도 향상)
        img = remove(img)                   # 배경제거
        color_list = topK_colors(img, 5)    # 이미지에 포함된 상위 K 개의 색 추출
     
        # R, G, B 값 가져오기
        R, G, B = color_list[1]
        color_r.append(R)
        color_g.append(G)
        color_b.append(B)
        

    #-- RGB 값 속성 추가
    item_df['R'] = color_r
    item_df['G'] = color_g
    item_df['B'] = color_b
    item_df.to_excel('./temp_preprocess_color.xlsx', engine='openpyxl', index=False)

    print ("Preprocessing Color Done..")

    return item_df


# 평점 결측치 처리
def rating_preprocess(item_df: pd.DataFrame) -> pd.DataFrame:
    """
    결측치가 있는 평점에 대해서는 나머지 평점의 평균으로 계산한다.
    """
    avg_rating = round(item_df[item_df['rating'].notnull()]['rating'].mean(), 2)
    item_df['rating'] = item_df['rating'].fillna(avg_rating)
    return item_df



def class_preprocess(raw_item_data: pd.DataFrame) -> pd.DataFrame:

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




# 좋아요 수 전처리
def likes_preprocess(raw_data: pd.DataFrame) -> pd.DataFrame:
    raw_data["likes"] = raw_data["likes"].fillna(0)
    return raw_data



# 성별 전처리
def gender_preprocess(raw_data: pd.DataFrame) -> pd.DataFrame:

    def preprocessing_gender_info(gender_info):
        '''
        성병 정보 추출 및 변환
        : gender_info - 하나의 아이템에 대한 gener 정보 (str or nan)
        '''
        if type(gender_info) == str:
            if gender_info != '남 여': return gender_info
        return '유니섹스'

    # -- gender 데이터 전처리
    raw_data['gender'] = raw_data.gender.transform(preprocessing_gender_info)
    return raw_data


def season_preprocess(raw_data: pd.DataFrame) -> pd.DataFrame:

    def make_season_day(season_info):
        '''
        season 정보를 사용하여 season day 추출 및 생성
        : season_info - 하나의 item에 대한 season 정보 (str or nan)
        '''
        if type(season_info) == str:
            day = re.search('[0-9]{4}', season_info)
            if day: return int(day.group())
        return None

    def preprosessing_season_info(season_info):
        '''
        season_info에서 S/S, F/W, ALL 정보 추출 및 변환
        : season_info - 하나의 item에 대한 season 정보 (str or nan)
        '''
        if type(season_info) == str:
            if re.search('[A-Z]\/[A-Z]', season_info): # S/S format의 str이 있는 경우 해당 정보를 뽑아냄
                return re.search('[A-Z]\/[A-Z]', season_info).group()
            elif re.search('[A-Z]{3}', season_info):   # ALL인 경우 해당 정보를 뽑아냄
                return re.search('[A-Z]{3}', season_info).group()
        return None

    # -- season_day feature 생성
    raw_data['season_day'] = raw_data.season.transform(make_season_day)
    # -- season 데이터 전처리
    raw_data['season'] = raw_data.season.transform(preprosessing_season_info)

    return raw_data


def view_preprocess(raw_data: pd.DataFrame) -> pd.DataFrame:

    def preprocessing_view_info(view_info):
        '''
        view_info 데이터를 실수로 변환 및 전처리
        : view_info - 하나의 item에 대한 view 정보 (str or nan)
        '''
        if type(view_info) == str:
            view_info = view_info.replace('회 이상', '').strip()
            view_info = view_info.replace('회 미만', '').strip()
            if view_info[-1] == '천':
                return float(view_info[:-1])*1000
            elif view_info[-1] == '만':
                return float(view_info[:-1])*10000
            return float(view_info)
        return view_info

    # -- view 데이터 전처리
    raw_data['view'] = raw_data.view.transform(preprocessing_view_info)

    return raw_data


def cum_sale_preprocess(raw_data: pd.DataFrame) -> pd.DataFrame:
    
    def preprocessing_cum_sale_info(cum_sale_info):
        '''
        cum_sale_info 데이터를 실수로 변환 및 전처리
        : cum_sale_info - 하나의 item에 대한 view 정보 (str or nan)
        '''
        if type(cum_sale_info) == str:
            cum_sale_info = cum_sale_info.replace('개 이상', '').strip()
            cum_sale_info = cum_sale_info.replace('개 미만', '').strip()
            if cum_sale_info[-1] == '천':
                return float(cum_sale_info[:-1])*1000
            elif cum_sale_info[-1] == '만':
                return float(cum_sale_info[:-1])*10000
            return float(cum_sale_info)
        return cum_sale_info
    
    # -- cum_sale 데이터 전처리
    raw_data['cum_sale'] = raw_data.cum_sale.transform(preprocessing_cum_sale_info)

    return raw_data


def buy_age_preprocess(item_data : pd.DataFrame, ITEM_PATH : str) -> pd.DataFrame :
    
    buy_age_data = pd.read_excel(ITEM_PATH + "item_buy_age.xlsx", engine='openpyxl')
    print(buy_age_data)

    most_bought_age_dict = dict()
    for i in range(len(buy_age_data)) :
        user_id = buy_age_data["id"].iloc[i]
        user_data = buy_age_data.iloc[i].drop("id")
        index = user_data.argmax()
        most_bought_age_dict[user_id] = index

    most_bought_age_list = list()
    for user in item_data["id"] :
        try :
            most_bought_age_list.append(most_bought_age_dict[int(user)])
        except :
            most_bought_age_list.append(6)

    item_data["most_bought_age_class"] = most_bought_age_list

    return item_data

def buy_gender_preprocess(item_data : pd.DataFrame, ITEM_PATH : str) -> pd.DataFrame :
    buy_gender_df = pd.read_excel(ITEM_PATH + "item_buy_gender.xlsx", engine='openpyxl')
    print(buy_gender_df)

    gender_ratio_dict = dict()
    for i in range(len(buy_gender_df)) :
        user_id = buy_gender_df["id"].iloc[i]
        men_ratio = buy_gender_df["buy_men"].iloc[i]
        gender_ratio_dict[user_id] = men_ratio
    
    gender_ratio_list = list()
    for user in item_data["id"] :
        try :
            gender_ratio_list.append(gender_ratio_dict[int(user)])
        except :
            gender_ratio_list.append(50)
    
    item_data["men_bought_ratio"] = gender_ratio_list

    return item_data

def get_nearest_color(rgb) -> str:
    sim_list = list()
    f = open('./color.json')
    color_json = json.load(f)
    
    for color in color_json.values():
        dist = [(color[0] - rgb[0]) ** 2, (color[1] - rgb[1]) ** 2, (color[2] - rgb[2]) ** 2]
        dist.append(max(dist))
        sim_list.append(sum(dist))

    index = sim_list.index(min(sim_list))
    color_name = list(color_json.keys())[index]
    return color_name

def get_cube_color(rgb) -> int:
    cube_id = (rgb[0] // 16) * 16 * 16 + (rgb[1] // 16) * 16 + (rgb[2] // 16)
    return cube_id

    
def color_class_preprocess(input_df: pd.DataFrame) -> pd.DataFrame:
    color_category = list()
    for row in input_df.iterrows():
        # print (row[1])
        r, g, b = row[1]['R'], row[1]['G'], row[1]['B']
        # print (r, g, b)
        color = get_cube_color([r, g, b])
        # color = get_nearest_color([r, g, b])
        color_category.append(color)

    # input_df["color_class"] = color_category
    input_df['color_id'] = color_category
    return input_df

def mid_class_preprocess(item_df: pd.DataFrame) -> pd.DataFrame :

    for i in range(len(item_df)) :
        if item_df["mid_class"].iloc[i] in ["겨울 더블 코트", "겨울 싱글 코트", "겨울 기타 코트"] :
            item_df["mid_class"].iloc[i] = "겨울 코트"
        elif item_df["mid_class"].iloc[i] in ["레더/라이더스 재킷", "무스탕/퍼"] :
            item_df["mid_class"].iloc[i] = "레더 재킷"
        elif item_df["mid_class"].iloc[i] in ['나일론/코치 재킷', '아노락 재킷', '트레이닝 재킷'] :
            item_df["mid_class"].iloc[i] = "트레이닝 재킷" 
        elif item_df["mid_class"].iloc[i] == "기타 스니커즈" :
            item_df["mid_class"].iloc[i] = "패션스니커즈화"
        elif item_df["mid_class"].iloc[i] == "농구화" :
            item_df["mid_class"].iloc[i] = "스포츠 신발"
    return item_df