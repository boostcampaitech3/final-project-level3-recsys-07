import openpyxl
import pickle
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from easydict import EasyDict
from utils import *

#-----------------------------------------
# 🌟 꼭 설정해야 하는 파라미터!
_VERBOSE = False

_SORT_OPTION = 'view'
# _SORT_OPTION = 'recent'

_STORE_OPTION = 'raw_codishop'
# _STORE_OPTION = 'raw_codimap'

# 아이템 크롤링 진행 범위 설정
START_CODI_NUM = 0
END_CODI_NUM = 0
#-----------------------------------------

URL_PATH = None
if _SORT_OPTION == 'view':
    if _STORE_OPTION == 'raw_codishop':
        print ("코디숍에서 조회순으로 정렬")
        URL_PATH = "https://www.musinsa.com/app/styles/lists?sort=view_cnt"
    else:
        print ("코디맵에서 조회순으로 정렬")
        URL_PATH = "https://www.musinsa.com/app/codimap/lists?sort=view_cnt"
else:
    if _STORE_OPTION == 'raw_codishop':
        print ("코디숍에서 최신순으로 정렬")
        URL_PATH = "https://www.musinsa.com/app/styles/lists"
    else:
        print ("코디맵에서 조회순으로 정렬")
        URL_PATH = "https://www.musinsa.com/app/codimap/lists"
        


# 🚀 크롤러 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(argument='--headless') 
chrome_options.add_argument(argument='--no-sandbox')
chrome_options.add_argument(argument='--disable-dev-shm-usage')

# 🚀 크롤러 지정
driver = webdriver.Chrome('chromedriver', options=chrome_options)
driver.implicitly_wait(3) #페이지를 로딩하는 시간동안 대기
driver.get(URL_PATH)

# 🚀 크롤링 완료된 정보를 저장할 excel sheet_codi 지정
workbooks = make_workbooks()
sheets = make_worksheets(workbooks)

# 🚀 남성 코디만 크롤링 하기 위해서 버튼 클릭
button = driver.find_element(By.CSS_SELECTOR, "button.global-filter__button--mensinsa")
button.click()

# 🚀 코디 정보를 가져올 url 받아오기
codi_info = pd.read_excel('/opt/ml/input/data/' + _STORE_OPTION + '/' + _SORT_OPTION + '/codi/codi.xlsx', engine='openpyxl')
# codi_info = codi_info.iloc[START_CODI_NUM : END_CODI_NUM]
codi_urls = codi_info["url"].to_list()
codi_ids = codi_info["id"].to_list()

# 🚀 각 코디에 대한 크롤링 진행
cnt = 0
seen_list = list()
crawled_codi_list = list()

for codi_id, codi_url in zip(codi_ids, codi_urls) :
    print(f"코디에 존재하는 아이템 크롤링 CODI URL : {codi_url}")
    print(f"{cnt} out of {len(codi_urls)} codi crawled...")

    # 코디에 하나씩 접근
    try :
        driver.get(codi_url)
    except :
        print("이 에러가 발생하면 다음 코디부터 따로 크롤링 해주시길 바랍니다!", flush=True)
        continue
    
    crawled_codi_list.append(str(codi_id))
    # 코디 안에 있는 아이템에 대한 element 받아오기
    item_list = driver.find_elements(By.CSS_SELECTOR, 'div.styling_list > div.swiper-slide')
    item_urls = []
    
    if len(item_list) <= 1:
        print ("코디 내에 존재하는 아이템의 수가 1개 이하이므로 크롤링을 진행하지 않습니다.")
        continue

    # 각 아이템들의 url 추출
    for item in item_list:

        item_url = item.find_element(By.CSS_SELECTOR, "a.brand_item").get_attribute('href')

        # 이미 크롤링 진행한 item은 pass
        if item_url in seen_list:
            print ("현재 아이템은 이미 크롤링이 완료된 상태이므로 건너뜁니다.")
            continue

        seen_list.append(item_url)
        item_urls.append(item_url)

    # 각 아이템들을 순회하면서 크롤링 진행
    for item_url in item_urls:
        try : 
            driver.get(item_url)
        except :
            print (f"Failed to load item (item_url = {item_url})", flush=True)
            continue
        
        print(f"Crawling item : {item_url}")
        item_info = EasyDict()
        item_info.item_url = item_url
        item_info.codi_id  = codi_id


        item_info.id            = get_item_id(item_url)
        item_info.name          = get_item_name(driver)

        category                = driver.find_elements(By.CSS_SELECTOR, "p.item_categories > a")
        item_info.big_class     = get_big_class(category)
        item_info.mid_class     = get_mid_class(category)

        product_info                = driver.find_elements(By.CSS_SELECTOR, "ul.product_article > li > p.product_article_contents > strong")
        item_info.brand             = get_brand(product_info)
        item_info.serial_number     = get_serial_number(product_info)
        item_info.season            = get_season(driver)
        item_info.gender            = get_gender(driver)
        item_info.view_count        = get_view(driver)
        item_info.cum_sale          = get_cum_sale(driver)
        item_info.likes             = get_likes(driver)
        item_info.rating            = get_rating(driver)  
        item_info.price             = get_price(driver)
        item_info.img_url           = get_img_url(driver)
        item_info.tags_list         = get_tags_list(driver)
        item_info.buy_age_list      = get_buy_age_list(driver)
        item_info.buy_gender_list   = get_buy_gender_list(driver)
        item_info.rel_codi_url_list = get_rel_codi_url_list(driver, item_info.id, crawled_codi_list)  
        item_info.four_season_list, item_info.fit_list = get_fs_and_fit(driver)    
        
        # 위에서 크롤링한 정보를 sheet에 append
        save_to_sheets(sheets, item_info)

        # 현재 아이템 crawling 결과 출력
        if _VERBOSE:
            print_crawled_item_info(item_info)

    cnt += 1

    # 크롤링 결과 파일로 저장
    save_workbooks(workbooks, _SORT_OPTION, _STORE_OPTION)

driver.close()

with open("../pickles/item.pickle", "wb") as f:
    pickle.dump(seen_list, f)
