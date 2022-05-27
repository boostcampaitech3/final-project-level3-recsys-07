from matplotlib.colors import hex2color
import openpyxl
import colorgram
import requests
import webcolors
import warnings
import json

import pandas as pd

from rembg import remove
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from typing import List, Tuple, Union

warnings.filterwarnings(action='ignore')


# hex color 값을 색 이름으로 변경해주는 dictionary
def get_hex2color_json(path: str) -> json:
    hex2color = None
    with open('./color_map.json', 'r') as fp:
        hex2color = json.load(fp)
    return hex2color


# 이미지를 불러오는 함수
def get_img_from_url(url: str) -> Image:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


# 이미지에 포함된 상위 K개의 색상 가져오기
def topK_colors(img: Image, k: int) -> List:
    colors = colorgram.extract(img, k)
    # print (colors)
    rgb_lists = list()

    for idx in range(k):
        if idx == len(colors):
            break
        R = colors[idx].rgb.r
        G = colors[idx].rgb.g
        B = colors[idx].rgb.b
        rgb_lists.append([R, G, B])

    return rgb_lists


# 가장 가까운 이름있는 색상 가져오기
def get_hex_color(requested_colour: Tuple[int, int, int]) -> str:
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = key
    return min_colours[min(min_colours.keys())]


# 이미지의 중앙 부분을 crop
def center_crop(img: Image, new_width, new_height):
    width, height = img.size   # Get dimensions

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    # Crop the center of the image
    img = img.crop((left, top, right, bottom))
    return img


def color_preprocess(item_df: pd.DataFrame) -> pd.DataFrame:

    hex_color = list()

    # 이미지에서 색 추출 과정
    for img_url in tqdm(item_df['img_url']):
        try:
            img = get_img_from_url(img_url)
        except:
            hex_color.append("#000000")
            continue

        img = img.resize((240, 320))        # 이미지 크기 조정 (속도 향상)
        img = remove(img)                   # 배경제거
        img = center_crop(img, 100, 100)    # 이미지 중앙 crop
        color_list = topK_colors(img, 3)    # 이미지에 포함된 상위 K 개의 색 추출


        # 배경색 (짙은 검정색)을 상위 색으로 추출한 경우: 다음색을 선택
        idx = 0
        if color_list[idx][0] < 5 and color_list[idx][1] < 5 and color_list[idx][2] < 5 and len(color_list) > 1:
            idx = 1
        
        # R, G, B 값 가져오기
        R, G, B = color_list[idx]
        hex_color.append(get_hex_color((R, G, B)))
        

    #-- 이미지에서 선택된 hex 코드를 색상 이름으로 변경
    item_df['hex_color'] = hex_color
    item_df['color_name'] = item_df['hex_color'].apply(lambda x: hex2color[x])
    item_df.to_excel('./temp_preprocess_color.xlsx', engine='openpyxl', index=False)

    print ("Preprocessing Color Done..")