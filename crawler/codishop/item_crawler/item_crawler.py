import openpyxl
import pickle
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from easydict import EasyDict
from utils import *

#-----------------------------------------
# π κΌ­ μ€μ ν΄μΌ νλ νλΌλ―Έν°!
_VERBOSE = False

_SORT_OPTION = 'view'
# _SORT_OPTION = 'recent'

_STORE_OPTION = 'raw_codishop'
# _STORE_OPTION = 'raw_codimap'

# μμ΄ν ν¬λ‘€λ§ μ§ν λ²μ μ€μ 
START_CODI_NUM = 0
END_CODI_NUM = 0
#-----------------------------------------

URL_PATH = None
if _SORT_OPTION == 'view':
    if _STORE_OPTION == 'raw_codishop':
        print ("μ½λμμμ μ‘°νμμΌλ‘ μ λ ¬")
        URL_PATH = "https://www.musinsa.com/app/styles/lists?sort=view_cnt"
    else:
        print ("μ½λλ§΅μμ μ‘°νμμΌλ‘ μ λ ¬")
        URL_PATH = "https://www.musinsa.com/app/codimap/lists?sort=view_cnt"
else:
    if _STORE_OPTION == 'raw_codishop':
        print ("μ½λμμμ μ΅μ μμΌλ‘ μ λ ¬")
        URL_PATH = "https://www.musinsa.com/app/styles/lists"
    else:
        print ("μ½λλ§΅μμ μ‘°νμμΌλ‘ μ λ ¬")
        URL_PATH = "https://www.musinsa.com/app/codimap/lists"
        


# π ν¬λ‘€λ¬ μ΅μ μ€μ 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(argument='--headless') 
chrome_options.add_argument(argument='--no-sandbox')
chrome_options.add_argument(argument='--disable-dev-shm-usage')

# π ν¬λ‘€λ¬ μ§μ 
driver = webdriver.Chrome('chromedriver', options=chrome_options)
driver.implicitly_wait(3) #νμ΄μ§λ₯Ό λ‘λ©νλ μκ°λμ λκΈ°
driver.get(URL_PATH)

# π ν¬λ‘€λ§ μλ£λ μ λ³΄λ₯Ό μ μ₯ν  excel sheet_codi μ§μ 
workbooks = make_workbooks()
sheets = make_worksheets(workbooks)

# π λ¨μ± μ½λλ§ ν¬λ‘€λ§ νκΈ° μν΄μ λ²νΌ ν΄λ¦­
button = driver.find_element(By.CSS_SELECTOR, "button.global-filter__button--mensinsa")
button.click()

# π μ½λ μ λ³΄λ₯Ό κ°μ Έμ¬ url λ°μμ€κΈ°
codi_info = pd.read_excel('/opt/ml/input/data/' + _STORE_OPTION + '/' + _SORT_OPTION + '/codi/codi.xlsx', engine='openpyxl')
# codi_info = codi_info.iloc[START_CODI_NUM : END_CODI_NUM]
codi_urls = codi_info["url"].to_list()
codi_ids = codi_info["id"].to_list()

# π κ° μ½λμ λν ν¬λ‘€λ§ μ§ν
cnt = 0
seen_list = list()
crawled_codi_list = list()

for codi_id, codi_url in zip(codi_ids, codi_urls) :
    print(f"μ½λμ μ‘΄μ¬νλ μμ΄ν ν¬λ‘€λ§ CODI URL : {codi_url}")
    print(f"{cnt} out of {len(codi_urls)} codi crawled...")

    # μ½λμ νλμ© μ κ·Ό
    try :
        driver.get(codi_url)
    except :
        print("μ΄ μλ¬κ° λ°μνλ©΄ λ€μ μ½λλΆν° λ°λ‘ ν¬λ‘€λ§ ν΄μ£ΌμκΈΈ λ°λλλ€!", flush=True)
        continue
    
    crawled_codi_list.append(str(codi_id))
    # μ½λ μμ μλ μμ΄νμ λν element λ°μμ€κΈ°
    item_list = driver.find_elements(By.CSS_SELECTOR, 'div.styling_list > div.swiper-slide')
    item_urls = []
    
    if len(item_list) <= 1:
        print ("μ½λ λ΄μ μ‘΄μ¬νλ μμ΄νμ μκ° 1κ° μ΄νμ΄λ―λ‘ ν¬λ‘€λ§μ μ§ννμ§ μμ΅λλ€.")
        continue

    # κ° μμ΄νλ€μ url μΆμΆ
    for item in item_list:

        item_url = item.find_element(By.CSS_SELECTOR, "a.brand_item").get_attribute('href')

        # μ΄λ―Έ ν¬λ‘€λ§ μ§νν itemμ pass
        if item_url in seen_list:
            print ("νμ¬ μμ΄νμ μ΄λ―Έ ν¬λ‘€λ§μ΄ μλ£λ μνμ΄λ―λ‘ κ±΄λλλλ€.")
            continue

        seen_list.append(item_url)
        item_urls.append(item_url)

    # κ° μμ΄νλ€μ μννλ©΄μ ν¬λ‘€λ§ μ§ν
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
        
        # μμμ ν¬λ‘€λ§ν μ λ³΄λ₯Ό sheetμ append
        save_to_sheets(sheets, item_info)

        # νμ¬ μμ΄ν crawling κ²°κ³Ό μΆλ ₯
        if _VERBOSE:
            print_crawled_item_info(item_info)

    cnt += 1

    # ν¬λ‘€λ§ κ²°κ³Ό νμΌλ‘ μ μ₯
    save_workbooks(workbooks, _SORT_OPTION, _STORE_OPTION)

driver.close()

with open("../pickles/item.pickle", "wb") as f:
    pickle.dump(seen_list, f)
