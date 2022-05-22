import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from easydict import EasyDict
from utils import *

# 🌟 꼭 설정해야 하는 파라미터!
_VERBOSE = True
URL_PATH = "https://www.musinsa.com/app/styles/lists"

# 🚀 크롤러 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(argument='--headless') 
chrome_options.add_argument(argument='--no-sandbox')
chrome_options.add_argument(argument='--disable-dev-shm-usage')

# 🚀 크롤러 지정
driver = webdriver.Chrome('chromedriver', options=chrome_options)
driver.get(URL_PATH)
driver.implicitly_wait(3) #페이지를 로딩하는 시간동안 대기

# 🚀 크롤링 완료된 정보를 저장할 excel sheet_codi 지정
workbooks = make_workbooks()
sheets = make_worksheets(workbooks)

# 🚀 남성 코디만 크롤링 하기 위해서 버튼 클릭
button = driver.find_element(By.CSS_SELECTOR, "button.global-filter__button--mensinsa")
button.click()

# 🚀 코디 정보를 가져올 url 받아오기
codi_info = pd.read_excel("../codi_crawler/asset/codi.xlsx")
codi_urls = codi_info["url"].to_list()
codi_ids = codi_info["id"].to_list()

# 🚀 각 코디에 대한 크롤링 진행
cnt = 0
for codi_id, codi_url in zip(codi_ids, codi_urls) :
    print(f"Crawling for CODI URL : {codi_url}\n")
    print(f"{cnt} out of {len(codi_urls)} codi crawled...")

    # 코디에 하나씩 접근
    try :
        driver.get(codi_url)
        driver.implicitly_wait(3)
    except :
        print("이 에러가 발생하면 다음 코디부터 따로 크롤링 해주시길 바랍니다!")
        continue
    
    # 코디 안에 있는 아이템에 대한 element 받아오기
    item_list = driver.find_elements(By.CSS_SELECTOR, 'div.styling_list > div.swiper-slide')
    item_urls = []
    
    # 각 아이템들의 url 추출
    for item in item_list:
        item_url = item.find_element(By.CSS_SELECTOR, "a.brand_item").get_attribute('href')
        item_urls.append(item_url)

    # 각 아이템들을 순회하면서 크롤링 진행
    for item_url in item_urls:
        try : 
            driver.get(item_url)
            driver.implicitly_wait(0.5) #페이지를 로딩하는 시간동안 대기
        except :
            continue
        
        print(f"Crawling item : {item_url}")
        item_info = EasyDict()
        item_info.item_url = item_url
        item_info.codi_id  = codi_id


        item_info.id            = get_item_id(item_url)
        item_info.name          = get_item_name(driver)

        category      = driver.find_elements(By.CSS_SELECTOR, "p.item_categories > a")
        item_info.big_class     = get_big_class(category)
        item_info.mid_class     = get_mid_class(category)

        product_info  = driver.find_elements(By.CSS_SELECTOR, "ul.product_article > li > p.product_article_contents > strong")
        item_info.brand         = get_brand(product_info)
        item_info.serial_number = get_serial_number(product_info)
        item_info.season        = get_season(driver, product_info)
        item_info.gender        = get_gender(driver)
        item_info.view          = get_view(driver)
        item_info.cum_sale      = get_cum_sale(driver)
        item_info.likes         = get_likes(driver)
        item_info.rating        = get_rating(driver)  
        item_info.price         = get_price(driver)
        item_info.img_url       = get_img_url(driver)
        
        #-- 주의: 크롤링의 일관성이 높지 않음
        try: menu = driver.find_elements(By.CSS_SELECTOR, "div#goods_opt_area > select")
        except: menu = None
        item_info.color_list    = get_color(menu)
        item_info.size_list     = get_size(menu)

        item_info.tags_list       = get_tags_list(driver)
        item_info.buy_age_list    = get_buy_age_list(driver)
        item_info.buy_gender_list = get_buy_gender_list(driver)
        item_info.four_season_list, item_info.fit_list = get_fs_and_fit(driver)      
        
        # 위에서 크롤링한 정보를 sheet에 append
        save_to_sheets(sheets, item_info)

        # 현재 아이템 crawling 결과 출력
        if _VERBOSE:
            print_crawled_item_info(item_info)

    cnt += 1

# 크롤링 결과 파일로 저장
save_workbooks(workbooks)
driver.close()
