import os
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By

from tqdm import tqdm
from typing import Tuple

# pip install openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


# ๐ ์ฝ๋๋ค์ ๋ฝ์์ฌ ํ์ด์ง ์ง์ 
COORDI_LIST_PATH = "https://www.musinsa.com/app/styles/lists?sort=view_cnt&page="
COORDI_BASE_PATH = "https://www.musinsa.com/app/styles/views/"

# ๐ (์ฝ๋ ๋งํฌ, ์คํ์ผ ์ ๋ณด, ์ฝ๋ ์ด๋ฏธ์ง url) ๋ฆฌ์คํธ ๋ฐ์์ค๊ธฐ
def get_codi_info(driver: webdriver.Chrome) -> Tuple[list, list, list]:
    
    codi_link_result = driver.find_elements(by=By.CSS_SELECTOR, value=".style-list-item__thumbnail > a")
    style_result = driver.find_elements(by=By.CSS_SELECTOR, value=".style-list-information__text")
    image_url_result = driver.find_elements(by=By.CSS_SELECTOR, value=".style-list-item__thumbnail > a > div.style-list-thumbnail > img")
    codi_popularity = driver.find_elements(by=By.CSS_SELECTOR, value='.post-information > .post-information__text')

    print (f"""
           # of codi_links : {len(codi_link_result)}
           # of style : {len(style_result)}
           # of img_urls : {len(image_url_result)}
           """)

    codi_id_list = list()
    codi_style_list = list()
    codi_url_list = list()
    pop_list = list()

    # โญ 1. ์ฝ๋ ID ์ ๋ณด javascript function ์ธ์๋ก ๋ถํฐ ๋ฐ์์ค๊ธฐ
    for link_element in codi_link_result:
        js_function = link_element.get_attribute("onclick")
        codi_id = js_function.split("'")[1]
        codi_id_list.append(codi_id)
        
    # โญ 2. style ์ ๋ณด text๋ก ์ถ์ถํ๊ธฐ
    for style_element in style_result:
        codi_style_list.append(style_element.text)
        
    # โญ 3. ์ฝ๋์ ์ด๋ฏธ์ง url ๋ฐ์์ค๊ธฐ
    for img_element in image_url_result:
        codi_url_list.append(img_element.get_attribute('src'))

    already_crawled_codi = list()
    with open("../pickles/codi.pickle", "rb") as f:
        try:
            already_crawled_codi = pickle.load(f)
        except:
            pass

    with open("../pickles/codi.pickle", "wb") as f:
        already_crawled_codi.extend(codi_url_list)
        pickle.dump(already_crawled_codi, f)

    # 4. ์ฝ๋์ ์กฐํ์ ๋ฐ์์ค๊ธฐ
    for popularity_element in codi_popularity:
        if "์กฐํ" in popularity_element.text:
            cnt = int(popularity_element.text[3:].replace(",", ""))
            pop_list.append(cnt)
        
    return codi_id_list, codi_style_list, codi_url_list, pop_list

"""
1. ํ์ฌ ์ฝ๋์ ์ด๋ค ์์ดํ๋ค์ด ์กด์ฌํ๋์ง ํ์ธ
2. ์ฝ๋ ์ ๋ณด ์์ง
3. ์ด๋ค ์ฝ๋๋ค์ ํฌ๋กค๋ง ํ๋์ง ์ ์ฅ
"""


# ๐ ์ฝ๋ ๋งํฌ์ ํ๋์ฉ ์ ์ํ๋ฉด์, ์ฐ๊ด๋ ์ํ ID, ์ฝ๋ํ๊ทธ ๋ฐ์์ค๊ธฐ
def make_crawl_xlsx(driver: webdriver.Chrome, sheets: Tuple[Worksheet, Worksheet, Worksheet]):
    
    sheet_codi = sheets[0]
    sheet_codi_tag = sheets[1]
    sheet_item_codi_id = sheets[2]
    
    # (์ฝ๋ ๋งํฌ, ์คํ์ผ ์ ๋ณด, ์ฝ๋ ์ด๋ฏธ์ง url) ๋ฆฌ์คํธ ๋ฐ์์ค๊ธฐ
    codi_id_list, codi_style_list, codi_url_list, pop_list = get_codi_info(driver)
    
    for codi_id, codi_style, codi_img_url, popularity in tqdm(zip(codi_id_list, codi_style_list, codi_url_list, pop_list), total=len(codi_id_list), desc="Codi crawling progress"):
            
        # ํ๋์ ์ฝ๋์ ๋ํ information ์ ์ฅ
        codi_info = list()
        
        # โญ 4. ์ฝ๋์ ์์ธ์ ๋ณด๊ฐ ์๋ url ๋ฐ์์ค๊ธฐ
        codi_path = COORDI_BASE_PATH + codi_id
        
        # ์ฝ๋์ ๊ฒฝ๋ก ๋ฐ์์ค๊ณ  ์ฝ๋ ์์ธ์ ๋ณด ํ์ด์ง ์ง์ํ๊ธฐ
        driver.get(codi_path)
        
        # โญ 6. ํ์ฌ ์ฝ๋์ ํฌํจ๋ ์์ดํ id ๋ฐ์์ค๊ธฐ (๋ค๋ฅธ sheet์ ์ ์ฅ)
        item_elements = driver.find_elements(by=By.CSS_SELECTOR, value=".styling_img")
        if len(item_elements) <= 1:
            print ("ํ์ฌ ์ฝ๋์ ์กด์ฌํ๋ ์์ดํ์ ์๊ฐ 1๊ฐ ๋ฏธ๋ง์๋๋ค.")
            print ("๋ฐ๋ผ์, ํ์ฌ ์ฝ๋์ ์กด์ฌํ๋ ์์ดํ์ ํฌ๋กค๋ง์ ์งํํ์ง ์์ต๋๋ค.")
            continue

        for item_element in item_elements:
            item_id = item_element.get_attribute("href").split("/")[-2]
            print (f"Connecting  Item #{item_id} ----- Codi #{codi_id}")
            sheet_item_codi_id.append([item_id, codi_id])

        # โญ 5. ์ฝ๋ ํ๊ทธ ๋ฐ์์ค๊ธฐ (๋ค๋ฅธ sheet์ ์ ์ฅ)
        coordi_tags = driver.find_elements(by=By.CSS_SELECTOR, value=".ui-tag-list")
        for tag_element in coordi_tags:
            sheet_codi_tag.append([codi_id, tag_element.text])
        
            
        codi_info.append(codi_id)
        codi_info.append(codi_style)
        codi_info.append(codi_img_url)
        codi_info.append(codi_path)
        codi_info.append(popularity)
        sheet_codi.append(codi_info)
        
        
# ๐ ํฌ๋กค๋ง ์๋ฃ๋ ํ์ผ ์ ์ฅ
def save_as_xlsx(workbooks: Tuple[Workbook, Workbook, Workbook]):
    wb_codi = workbooks[0]
    wb_codi_tag = workbooks[1]
    wb_item_codi_id = workbooks[2]
        
    subpath = 'recent'
    if "sort" in COORDI_LIST_PATH:
        subpath = 'view'
    
    PATH = '/opt/ml/input/data/raw_codishop/' + subpath + '/codi/'
    ITEM_PATH = '/opt/ml/input/data/raw_codishop/' + subpath + '/item/'
    os.makedirs(PATH, exist_ok=True)
    wb_codi.save(os.path.join(PATH, "codi.xlsx"))
    wb_codi_tag.save(os.path.join(PATH, "codi_tag.xlsx"))
    wb_item_codi_id.save(os.path.join(ITEM_PATH, "item_codi_id.xlsx"))
    
# ๐ ์ต์์ ๋ฉ์ธ ํ์ด์ง ๋ถ๋ฌ์ค๊ธฐ (์ฝ๋ ๋ชฉ๋ก 60๊ฐ ๋ณด์ฌ์ง๋ ํ์ด์ง)
def do_crawling(
    workbooks: Tuple[Workbook, Workbook, Workbook],
    sheets: Tuple[Worksheet, Worksheet, Worksheet],
    num_crawl_pages: int = 5,
    ):
    
    # ๐ Chrome option ์ค์ 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(argument='--headless')
    chrome_options.add_argument(argument='--no-sandbox')
    chrome_options.add_argument(argument='--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
    driver.implicitly_wait(1.5)

    if "sort" in COORDI_LIST_PATH:
        print ("codi sort by '์กฐํ์'")
    else:
        print ("codi sort by '์ต์ ์'")
    
    for page_idx in range(1, num_crawl_pages + 1):
        print (f"Crawling {page_idx} pages..\nurl={COORDI_LIST_PATH + str(page_idx)}")
        driver.get(COORDI_LIST_PATH + str(page_idx))
        
        # "๋จ์ฑ"์ผ๋ก ์ฑ๋ณ ๊ณ ์ 
        button_male = driver.find_element(By.CSS_SELECTOR, "button.global-filter__button--mensinsa")
        button_male.click()
                
        make_crawl_xlsx(driver, sheets)
    
    driver.close()
    
    save_as_xlsx(workbooks)
    print ("ํฌ๋กค๋ง์ด ์ข๋ฃ๋์์ต๋๋ค. ๋ชจ๋  ํ์ผ๋ค์ด ์ ์ฅ๋์์ต๋๋ค.")