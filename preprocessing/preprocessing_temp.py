import pandas as pd
import openpyxl

from color_class_preprocess import color_class_preprocess

PATH = '/opt/ml/input/data/asset_codishop/view/item/item.xlsx'
df = pd.read_excel(PATH, engine='openpyxl')

df = color_class_preprocess(df)

df.to_excel('./temp_color.xlsx', index=False)