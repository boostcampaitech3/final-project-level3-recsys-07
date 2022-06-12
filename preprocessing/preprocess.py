from utils.codi.codi_preprocess_functions import *
from utils.item.item_preprocess_functions import *

# item 과 관련된 전처리
def preprocess_item():
    preprocess_item_basic()
    preprocess_item_fit()
    preprocess_item_four_season()
    preprocess_item_tag()
    preprocess_item_relative_codi_url()
    preprocess_item_codi_id()
    preprocess_item_by_gender()
    preprocess_item_by_age()


# codi 와 관련된 전처리
def preprocess_codi():
    preprocess_codi()
    preprocess_codi_tag()


if __name__ == "__main__":
    print ("[1] 아이템 전처리를 진행합니다.")
    preprocess_item()

    print ("[2] 코디 전처리를 진행합니다.")
    preprocess_codi()