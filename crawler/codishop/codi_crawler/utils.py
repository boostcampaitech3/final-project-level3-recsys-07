import os
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By

from tqdm import tqdm
from typing import Tuple

# pip install openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


# 🚀 코디들을 뽑아올 페이지 지정
COORDI_LIST_PATH = "https://www.musinsa.com/app/styles/lists?sort=view_cnt&page="
COORDI_BASE_PATH = "https://www.musinsa.com/app/styles/views/"

# 🚀 (코디 링크, 스타일 정보, 코디 이미지 url) 리스트 받아오기
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

    # ⭐ 1. 코디 ID 정보 javascript function 인자로 부터 받아오기
    for link_element in codi_link_result:
        js_function = link_element.get_attribute("onclick")
        codi_id = js_function.split("'")[1]
        codi_id_list.append(codi_id)
        
    # ⭐ 2. style 정보 text로 추출하기
    for style_element in style_result:
        codi_style_list.append(style_element.text)
        
    # ⭐ 3. 코디의 이미지 url 받아오기
    for img_element in image_url_result:
        codi_url_list.append(img_element.get_attribute('src'))

    already_crawled_codi = list()
    with open("/opt/ml/input/data/already/codi.pickle", "rb") as f:
        try:
            already_crawled_codi = pickle.load(f)
        except:
            pass

    with open("/opt/ml/input/data/already/codi.pickle", "wb") as f:
        already_crawled_codi.extend(codi_url_list)
        pickle.dump(already_crawled_codi, f)

    # 4. 코디의 조회수 받아오기
    for popularity_element in codi_popularity:
        if "조회" in popularity_element.text:
            cnt = int(popularity_element.text[3:].replace(",", ""))
            pop_list.append(cnt)
        
    return codi_id_list, codi_style_list, codi_url_list, pop_list

"""
1. 현재 코디에 어떤 아이템들이 존재하는지 확인
2. 코디 정보 수집
3. 어떤 코디들을 크롤링 했는지 저장
"""


# 🚀 코디 링크에 하나씩 접속하면서, 연관된 상품 ID, 코디태그 받아오기
def make_crawl_xlsx(driver: webdriver.Chrome, sheets: Tuple[Worksheet, Worksheet, Worksheet]):
    
    sheet_codi = sheets[0]
    sheet_codi_tag = sheets[1]
    sheet_item_codi_id = sheets[2]
    
    # (코디 링크, 스타일 정보, 코디 이미지 url) 리스트 받아오기
    codi_id_list, codi_style_list, codi_url_list, pop_list = get_codi_info(driver)
    
    for codi_id, codi_style, codi_img_url, popularity in tqdm(zip(codi_id_list, codi_style_list, codi_url_list, pop_list), total=len(codi_id_list), desc="Codi crawling progress"):
            
        # 하나의 코디에 대한 information 저장
        codi_info = list()
        
        # ⭐ 4. 코디의 상세정보가 있는 url 받아오기
        codi_path = COORDI_BASE_PATH + codi_id
        
        # 코디의 경로 받아오고 코디 상세정보 페이지 진입하기
        driver.get(codi_path)
        
        # ⭐ 6. 현재 코디에 포함된 아이템 id 받아오기 (다른 sheet에 저장)
        item_elements = driver.find_elements(by=By.CSS_SELECTOR, value=".styling_img")
        if len(item_elements) <= 1:
            print ("현재 코디에 존재하는 아이템의 수가 1개 미만입니다.")
            print ("따라서, 현재 코디에 존재하는 아이템의 크롤링은 진행하지 않습니다.")
            continue

        for item_element in item_elements:
            item_id = item_element.get_attribute("href").split("/")[-2]
            print (f"Connecting  Item #{item_id} ----- Codi #{codi_id}")
            sheet_item_codi_id.append([item_id, codi_id])

        # ⭐ 5. 코디 태그 받아오기 (다른 sheet에 저장)
        coordi_tags = driver.find_elements(by=By.CSS_SELECTOR, value=".ui-tag-list")
        for tag_element in coordi_tags:
            sheet_codi_tag.append([codi_id, tag_element.text])
        
            
        codi_info.append(codi_id)
        codi_info.append(codi_style)
        codi_info.append(codi_img_url)
        codi_info.append(codi_path)
        codi_info.append(popularity)
        sheet_codi.append(codi_info)
        
        
# 🚀 크롤링 완료된 파일 저장
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
    
# 🚀 최상위 메인 페이지 불러오기 (코디 목록 60개 보여지는 페이지)
def do_crawling(
    workbooks: Tuple[Workbook, Workbook, Workbook],
    sheets: Tuple[Worksheet, Worksheet, Worksheet],
    num_crawl_pages: int = 5,
    ):
    
    # 🚀 Chrome option 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(argument='--headless')
    chrome_options.add_argument(argument='--no-sandbox')
    chrome_options.add_argument(argument='--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
    driver.implicitly_wait(1.5)

    if "sort" in COORDI_LIST_PATH:
        print ("codi sort by '조회순'")
    else:
        print ("codi sort by '최신순'")
    
    for page_idx in range(1, num_crawl_pages + 1):
        print (f"Crawling {page_idx} pages..\nurl={COORDI_LIST_PATH + str(page_idx)}")
        driver.get(COORDI_LIST_PATH + str(page_idx))
        
        # "남성"으로 성별 고정
        button_male = driver.find_element(By.CSS_SELECTOR, "button.global-filter__button--mensinsa")
        button_male.click()
                
        make_crawl_xlsx(driver, sheets)
    
    driver.close()
    
    save_as_xlsx(workbooks)
    print ("크롤링이 종료되었습니다. 모든 파일들이 저장되었습니다.")