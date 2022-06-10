import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm


# !important data path
CODI_PATH = '/opt/ml/input/data/asset_codishop/view/codi/codi.csv'
codi_df = pd.read_csv(CODI_PATH)

# selenium crawler
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(argument='--headless')
chrome_options.add_argument(argument='--no-sandbox')
chrome_options.add_argument(argument='--disable-dev-shm-usage')

# chrome driver setting
driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
driver.implicitly_wait(1.5)


img_url_list = list()
for idx, data in tqdm(codi_df.iterrows(), total=len(codi_df)):
    codi_id = data['id']
    codi_url = data['url']

    # 코디의 정보가 있는 페이지로 접속한다.
    # 하지만, 이 코디 이미지들 중 어떤 것들이 best 샷인지 모르기 때문에 다른 아이템으로 이동한다.
    driver.get(codi_url)
    item_in_codi = driver.find_elements(by=By.CSS_SELECTOR, value=".styling_list > .swiper-slide > .box-img > .styling_img")
    if len(item_in_codi) == 0:
        print (f"현재 코디 ID {codi_id} 에는 연결된 아이템의 정보가 존재하지 않습니다.. url={codi_url}")
        img_url_list.append(data['img_url'])
        continue
    item_in_codi_url = item_in_codi[0].get_attribute('href')

    #  아이템에 포함된 코디의 정보들을 가져온다.
    driver.get(item_in_codi_url)
    codi_in_item = driver.find_elements(by=By.CSS_SELECTOR, value='.style_list > .list_item > .img-block')
    codi_img_in_item = driver.find_elements(by=By.CSS_SELECTOR, value='.style_list > .list_item > .img-block > .coordi_img')

    for codi_url_tag, codi_img_url_tag in zip(codi_in_item, codi_img_in_item):
        current_id = codi_url_tag.get_attribute('href').split("/")[-1]
        if str(current_id) == str(codi_id):
            current_img_url = codi_img_url_tag.get_attribute('src')
            img_url_list.append(current_img_url)
            break
        
    img_url_list.append(data['img_url'])
codi_df['img_url'] = img_url_list

# save to codi_path as csv
codi_df.to_csv(CODI_PATH, index=False)