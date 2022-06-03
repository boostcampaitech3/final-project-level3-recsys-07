import openpyxl
import pickle
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from easydict import EasyDict
from utils_depth import *

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





#### 코디 - 아이템 리스트 ####
already_worksheet = openpyxl.load_workbook("/opt/ml/input/data/raw_codishop/view/item/item_codi_id.xlsx").active
already_codi_item_list = list()
for item_id, codi_id in zip(already_worksheet['A'], already_worksheet['B']):
    already_codi_item_list.append((item_id, codi_id))
already_codi_item_list = already_codi_item_list[1:]
print (f"현재 보유한 연결정보 : {len(already_codi_item_list)} 개")


already_crawled_codi = list()
already_crawled_item = list()

with open("/opt/ml/input/data/already/codi.pickle", "rb") as f:
    already_crawled_codi = pickle.load(f)

with open("/opt/ml/input/data/already/item.pickle", "rb") as f:
    try:
        already_crawled_item = pickle.load(f)
    except:
        pass
    
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
codi_info = pd.read_excel('/opt/ml/input/data/raw_codishop/view/item/item_rel_codi_url.xlsx', engine='openpyxl')
# codi_info = codi_info.iloc[START_CODI_NUM : END_CODI_NUM]

codi_urls = codi_info["rel_codi_url"].to_list()

# 🚀 각 코디에 대한 크롤링 진행
cnt = 0
for codi_url in codi_urls :
    print(f"\nCrawling for CODI URL : {codi_url}")
    print(f"{cnt} out of {len(codi_urls)} codi crawled...")

    codi_id = codi_url.split("/")[-1]
    cnt += 1
    # 코디에 하나씩 접근
    try :
        driver.get(codi_url)
    except :
        print("이 에러가 발생하면 다음 코디부터 따로 크롤링 해주시길 바랍니다!", flush=True)
        continue
    
    # 코디 안에 있는 아이템에 대한 element 받아오기
    item_list = driver.find_elements(By.CSS_SELECTOR, 'div.styling_list > div.swiper-slide')
    item_urls = []

    if len(item_list) <= 1:
        print ("현재 코디에는 1개 미만의 아이템이 존재하기 때문에 크롤링을 진행하지 않습니다.", flush=True)

    if codi_url in already_crawled_codi:
        print ("[item_crawler_depth.py] 이 코디는 이미 크롤링 된적이 있습니다.", flush=True)
        continue

    already_crawled_codi.append(str(codi_url))
    
    # 각 아이템들의 url 추출
    for item in item_list:
        item_url = item.find_element(By.CSS_SELECTOR, "a.brand_item").get_attribute('href')
        item_urls.append(item_url)

    # 각 아이템들을 순회하면서 크롤링 진행
    for item_url in item_urls:
        try : 
            driver.get(item_url)
        except :
            print (f"Failed to load item (item_url = {item_url})", flush=True)
            continue
        
        item_id = get_item_id(item_url)
        if (item_id, codi_id) in already_codi_item_list:
            print (f"\n[item_crawler_depth.py] 코디 #{codi_id} ----- 아이템 #{item_id} 의 연결정보가 이미 있습니다.")
        else:
            print (f"\n[item_crawler_depth.py] 코디 #{codi_id} --X-- 아이템 #{item_id} 의 연결정보가 없습니다.")
            already_codi_item_list.append((item_id, codi_id))


        print(f"아이템 #{item_id} 에 대한 크롤링을 진행합니다!! 웹 URL : {item_url}")
        if item_url in already_crawled_item:
            print (f"현재 아이템 #{item_id} 는 이미 크롤링이 완료된 상태이므로 건너뜁니다.")
            continue

        already_crawled_item.append(item_url)

        item_info = EasyDict()
        item_info.item_url = item_url
        item_info.codi_id  = codi_id

        item_info.id            = item_id
        item_info.name          = get_item_name(driver)

        category      = driver.find_elements(By.CSS_SELECTOR, "p.item_categories > a")
        item_info.big_class     = get_big_class(category)
        item_info.mid_class     = get_mid_class(category)

        product_info  = driver.find_elements(By.CSS_SELECTOR, "ul.product_article > li > p.product_article_contents > strong")
        item_info.brand         = get_brand(product_info)
        item_info.serial_number = get_serial_number(product_info)
        item_info.season        = get_season(driver)
        item_info.gender        = get_gender(driver)
        item_info.view_count    = get_view(driver)
        item_info.cum_sale      = get_cum_sale(driver)
        item_info.likes         = get_likes(driver)
        item_info.rating        = get_rating(driver)  
        item_info.price         = get_price(driver)
        item_info.img_url       = get_img_url(driver)
        
        #-- 주의: 크롤링의 일관성이 높지 않음
        try: menu = driver.find_elements(By.CSS_SELECTOR, "div#goods_opt_area > select")
        except: menu = None

        item_info.tags_list       = get_tags_list(driver)
        item_info.buy_age_list    = get_buy_age_list(driver)
        item_info.buy_gender_list = get_buy_gender_list(driver)
        item_info.four_season_list, item_info.fit_list = get_fs_and_fit(driver)    
        item_info.rel_codi_url_list = get_rel_codi_url_list(driver, item_info.id, already_crawled_codi)  
        
        # 위에서 크롤링한 정보를 sheet에 append
        save_to_sheets(sheets, item_info)

        # 크롤링 결과 파일로 저장
        # save_workbooks(workbooks, _SORT_OPTION, _STORE_OPTION)

        # 현재 아이템 crawling 결과 출력
        if _VERBOSE:
            print_crawled_item_info(item_info)

    save_workbooks(workbooks, _SORT_OPTION, _STORE_OPTION)
driver.close()


with open("/opt/ml/input/data/already/codi.pickle", "wb") as f:
    pickle.dump(already_crawled_codi, f)

with open("/opt/ml/input/data/already/item.pickle", "wb") as f:
    pickle.dump(already_crawled_item, f)

already_worksheet = openpyxl.Workbook().active
already_worksheet.append(['id', 'codi_id'])
for (item_id, codi_id) in already_codi_item_list:
    already_worksheet.append([item_id, codi_id])
already_worksheet.save('/opt/ml/input/data/raw_codishop/view/item/item_codi_id.xlsx')

