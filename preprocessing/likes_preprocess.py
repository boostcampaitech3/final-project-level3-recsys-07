import numpy as np
import pandas as pd


def likes_preprocess(raw_data) :

    df= raw_data[["id","likes"]]
    raw_data["likes"] = raw_data["likes"].fillna(0)
    
    return raw_data