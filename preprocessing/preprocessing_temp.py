import pandas as pd
import openpyxl

from utils_item import *

PATH = '/opt/ml/input/data/asset_codishop/view/item/item.xlsx'
df = pd.read_excel(PATH, engine='openpyxl')

df = color_class_preprocess(df)
df = mid_class_preprocess(df)
df = cluster_preprocess(df)

df.to_excel('./temp_color_midclass.xlsx', index=False)