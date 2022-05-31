import pandas as pd
import json
from typing import List


def get_nearest_color(rgb) -> str:
    sim_list = list()
    f = open('./color.json')
    color_json = json.load(f)
    
    for color in color_json.values():
        dist = (color[0] - rgb[0]) ** 2 + (color[1] - rgb[1]) ** 2 + (color[2] - rgb[2]) ** 2
        sim_list.append(dist)

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