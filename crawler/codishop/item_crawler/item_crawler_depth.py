import openpyxl
import pickle
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from easydict import EasyDict
from utils_depth import *

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





#### μ½λ - μμ΄ν λ¦¬μ€νΈ ####
already_worksheet = openpyxl.load_workbook("/opt/ml/input/data/raw_codishop/view/item/item_codi_id.xlsx").active
already_codi_item_list = list()
for item_id, codi_id in zip(already_worksheet['A'], already_worksheet['B']):
    already_codi_item_list.append((item_id.value, codi_id.value))
already_codi_item_list = already_codi_item_list[1:]

print (f"νμ¬ λ³΄μ ν μ°κ²°μ λ³΄ : {len(already_codi_item_list)} κ°")

already_crawled_codi = list()
already_crawled_item = list()

# κΈ°μ‘΄μ μ΄λ€ μ½λλ€μ ν¬λ‘€λ§ νμλμ§
with open("../pickles/codi.pickle", "rb") as f:
    already_crawled_codi = pickle.load(f)

# κΈ°μ‘΄μ μ΄λ€ μμ΄νλ€μ ν¬λ‘€λ§ νμλμ§
with open("../pickles//item.pickle", "rb") as f:
    try: already_crawled_item = pickle.load(f)
    except: pass
    
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
codi_info = pd.read_excel('/opt/ml/input/data/raw_codishop/view/item/item_rel_codi_url.xlsx', engine='openpyxl')

codi_urls = codi_info["rel_codi_url"].to_list()

# π κ° μ½λμ λν ν¬λ‘€λ§ μ§ν
cnt = 1
for codi_url in codi_urls:
    print(f"\nCrawling for CODI URL : {codi_url}")
    print(f"{cnt} out of {len(codi_urls)} codi crawled...")

    codi_id = codi_url.split("/")[-1]
    cnt += 1
    # μ½λμ νλμ© μ κ·Ό
    try :
        driver.get(codi_url)
    except :
        print("[ERROR] νμ¬ μ½λμ μ λ³΄λ₯Ό λΆλ¬μ€λλ° μ€λ₯κ° λ°μνμ΅λλ€.", flush=True)
        continue
    
    # μ½λ μμ μλ μμ΄νμ λν element λ°μμ€κΈ°
    item_list = driver.find_elements(By.CSS_SELECTOR, 'div.styling_list > div.swiper-slide')
    item_urls = []

    if len(item_list) <= 1:
        print ("[WARNING] νμ¬ μ½λμλ 1κ° λ―Έλ§μ μμ΄νμ΄ μ‘΄μ¬νκΈ° λλ¬Έμ ν¬λ‘€λ§μ μ§ννμ§ μμ΅λλ€.", flush=True)
        continue

    if codi_url in already_crawled_codi:
        print ("[WARNING] μ΄ μ½λλ μ΄λ―Έ ν¬λ‘€λ§ λμ μ΄ μμ΅λλ€.", flush=True)
        continue

    # νμ¬ μ΄ μ½λλ₯Ό ν¬λ‘€λ§ ν  κ²μ΄κΈ° λλ¬Έμ ν¬λ‘€λ§ λ¦¬μ€νΈμ μ½μ
    already_crawled_codi.append(str(codi_url))
    
    # κ° μμ΄νλ€μ url μΆμΆ
    for item in item_list:
        item_url = item.find_element(By.CSS_SELECTOR, "a.brand_item").get_attribute('href')
        item_urls.append(item_url)

    # κ° μμ΄νλ€μ μννλ©΄μ ν¬λ‘€λ§ μ§ν
    for item_url in item_urls:
        try : 
            driver.get(item_url)
        except :
            print (f"[ERROR] νμ¬ μμ΄νμ λΆλ¬μ€λλ° μ€ν¨νμμ΅λλ€. (item url: {item_url})", flush=True)
            continue
        
        item_id = get_item_id(item_url)
        if (item_id, codi_id) in already_codi_item_list:
            print (f"\n[INFO] μ½λ(#{codi_id}) ----- μμ΄ν(#{item_id}) μ μ°κ²°μ λ³΄κ° μ΄λ―Έ μμ΅λλ€.")
        else:
            print (f"\n[INFO] μ½λ(#{codi_id}) ----- μμ΄ν(#{item_id}) μ μ°κ²°μ λ³΄κ° μμ΅λλ€.")
            already_codi_item_list.append((item_id, codi_id))


        print(f"[INFO] μμ΄ν #{item_id} μ λν ν¬λ‘€λ§μ μμν©λλ€. μΉ URL : {item_url}")
        if item_url in already_crawled_item:
            print (f"[WARNING] νμ¬ μμ΄ν #{item_id} λ μ΄λ―Έ ν¬λ‘€λ§μ΄ μλ£λ μνμ΄λ―λ‘ κ±΄λλλλ€.")
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
        
        #-- μ£Όμ: ν¬λ‘€λ§μ μΌκ΄μ±μ΄ λμ§ μμ
        try: menu = driver.find_elements(By.CSS_SELECTOR, "div#goods_opt_area > select")
        except: menu = None

        item_info.tags_list       = get_tags_list(driver)
        item_info.buy_age_list    = get_buy_age_list(driver)
        item_info.buy_gender_list = get_buy_gender_list(driver)
        item_info.four_season_list, item_info.fit_list = get_fs_and_fit(driver)    
        item_info.rel_codi_url_list = get_rel_codi_url_list(driver, item_info.id, already_crawled_codi)  
        
        # μμμ ν¬λ‘€λ§ν μ λ³΄λ₯Ό sheetμ append
        save_to_sheets(sheets, item_info)

        # ν¬λ‘€λ§ κ²°κ³Ό νμΌλ‘ μ μ₯
        # save_workbooks(workbooks, _SORT_OPTION, _STORE_OPTION)

        # νμ¬ μμ΄ν crawling κ²°κ³Ό μΆλ ₯
        if _VERBOSE:
            print_crawled_item_info(item_info)

    save_workbooks(workbooks, _SORT_OPTION, _STORE_OPTION)
driver.close()


with open("../pickles/codi.pickle", "wb") as f:
    pickle.dump(already_crawled_codi, f)

with open("../pickles/item.pickle", "wb") as f:
    pickle.dump(already_crawled_item, f)

already_workbook = openpyxl.Workbook()
already_worksheet = already_workbook.active
already_worksheet.append(['id', 'codi_id'])
for (item_id, codi_id) in already_codi_item_list:
    already_worksheet.append([item_id, codi_id])
already_workbook.save('/opt/ml/input/data/raw_codishop/view/item/item_codi_id.xlsx')

