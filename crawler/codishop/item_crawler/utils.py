import os
import openpyxl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from typing import List, Optional, Tuple, Union
from easydict import EasyDict
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

# 🚀 item의 id를 받아오는 함수
def get_item_id(item_url: str) -> str:
    return item_url.split('/')[-2]


# 🚀 item의 이름을 받아오는 함수
def get_item_name(driver: webdriver.Chrome) -> str:
    return driver.find_element(By.CSS_SELECTOR, "span.product_title > em").text


# 🚀 item의 대분류
def get_big_class(category : List[WebElement]) -> Optional[str]:
    try :
        big_class = category[0].text
    except :
        big_class = None
        
    return big_class


# 🚀 item의 중분류
def get_mid_class(category : List[WebElement]) -> Optional[str]:
    try :
        mid_class = category[1].text
    except :
        mid_class = None
    
    return mid_class


# 🚀 item의 브랜드
def get_brand(product_info: List[WebElement]) -> str:
    try :
        brand = product_info[0].find_element(By.CSS_SELECTOR, value="a").text
    except :
        brand = None
    return brand


# 🚀 item의 시리얼번호
def get_serial_number(product_info: List[WebElement]) -> Optional[str]:
    serial_number = product_info[0].get_attribute('innerHTML').split("</span>")[-1]
    if serial_number =="제품번호+컬러번호":
        serial_number = None 

    return serial_number


# 🚀 item의 시즌 정보
def get_season(driver: webdriver.Chrome) -> Optional[str]:

    # 시즌 정보가 존재하는 페이지인지 확인
    result = driver.find_elements(By.XPATH, '//*[@id="product_order_info"]/div[1]/ul/li[2]/p[1]/span[1]/a')
    if len(result) == 0:
        return None

    return driver.find_element(By.XPATH, '//*[@id="product_order_info"]/div[1]/ul/li[2]/p[2]/strong').text


# 🚀 item의 성별 정보
def get_gender(driver : webdriver.Chrome) -> Optional[str]:
    try :
        gender = driver.find_element(By.CSS_SELECTOR, "ul.product_article > li > p.product_article_contents > span.txt_gender").text
    except :
        gender = None

    if gender not in ["남", "남 여", "여"]:
        gender = None

    return gender


# 🚀 item의 조회 횟수
def get_view(driver : webdriver.Chrome) -> Optional[str]:
    view = driver.find_element(By.CSS_SELECTOR, "ul.product_article > li > p.product_article_contents > strong#pageview_1m").text
    if len(view) == 0 : 
        view = None
    return view


# 🚀 item의 누적 판매 횟수
def get_cum_sale(driver : webdriver.Chrome) -> Optional[str]:
    try:
        cum_sale = driver.find_element(By.CSS_SELECTOR, value="ul.product_article > li > p.product_article_contents > strong#sales_1y_qty").text
        if len(cum_sale) == 0 :
            cum_sale = None
    except :
        cum_sale = None
    
    return cum_sale


# 🚀 item의 좋아요 횟수
def get_likes(driver : webdriver.Chrome) -> Optional[str]:
    try:
        likes = int(driver.find_element(By.CSS_SELECTOR, value="ul.product_article > li > p.product_article_contents span.prd_like_cnt").text)
    except:
        likes = None
    return likes


# 🚀 item의 평점
def get_rating(driver : webdriver.Chrome) -> Optional[str]:
    try:
        rating = float(driver.find_element(By.CSS_SELECTOR, "span.prd-score__rating").text)
    except:
        rating = None
    return rating


# 🚀 item의 가격
def get_price(driver : webdriver.Chrome) -> Optional[str]:
    price = driver.find_element(By.CSS_SELECTOR, "span.product_article_price").text[:-1]
    price = int(price.replace(',', ''))
    return price


# 🚀 item의 이미지 url 링크
def get_img_url(driver: webdriver.Chrome) -> str:
    return driver.find_element(By.CSS_SELECTOR, "div.product-img > img").get_attribute('src')


# 🚀 idx 번째 dropbox
def get_dropbox(menu: List[WebElement], idx:int) -> Optional[List]:
    if len(menu) <= idx:
        return None

    option_list = list()
    options = menu[idx].find_elements(By.CSS_SELECTOR, "option")
    for i in range(1, len(options)):
        if options[i].text:
            option_list.append(options[i].text)

    return option_list

# 🚀 item의 색상 -- not used
def get_color(menu : List[WebElement]) -> Optional[str]:
    color = []
    if not menu or len(menu) == 1: return None
    colors = menu[0].find_elements(By.CSS_SELECTOR, "option")
    
    for i in range(1, len(colors)):
        if colors[i].text: color.append(colors[i].text)
    return color


# 🚀 item의 사이즈 -- not used
def get_size(menu : List[WebElement]) -> Optional[str]:
    size = [] 
    if not menu: return None
    if len(menu) == 1: sizes = menu[0].find_elements(By.CSS_SELECTOR, "option")
    else: sizes = menu[1].find_elements(By.CSS_SELECTOR, "option")
    
    for i in range(1, len(sizes)):
        if sizes[i].text: size.append(sizes[i].text)
    return size


# 🚀 item의 태그
def get_tags_list(driver : webdriver.Chrome) -> List:
    tags_list = list()
    tags_raw = driver.find_elements(By.CSS_SELECTOR, value='li.article-tag-list > p > a.listItem')
    
    for tag in tags_raw :
        tags_list.append(tag.text[1:])
    
    if len(tags_list) == 0:
        tags_list = None
    
    return tags_list


# 🚀 item의 계절 정보와, 핏 정보
def get_fs_and_fit(driver : webdriver.Chrome) -> Union[List, List]:
    guide_all = driver.find_elements(By.CSS_SELECTOR, value="table.table-simple tr")
    four_season_list = list()
    fit_list = list()
    for guide in guide_all :
        t = guide.find_element(By.CSS_SELECTOR, value="th").text
        if t == "계절" :
            seasons = guide.find_elements(By.CSS_SELECTOR, value="td.active")
            for season in seasons :
                four_season_list.append(season.text)
        elif t == "핏" :
            fits = guide.find_elements(By.CSS_SELECTOR, value="td.active")
            for fit in fits :
                fit_list.append(fit.text)
    if len(four_season_list)==0 :
        four_season_list = None
    
    if len(fit_list)==0 :
        fit_list = None
    return four_season_list, fit_list


# 🚀 item을 구매하는 연령층 비율
def get_buy_age_list(driver : webdriver.Chrome) -> Optional[str]:
    buy_age_raw = driver.find_elements(By.CSS_SELECTOR, value="ul.bar_wrap > li span.bar_num")
    buy_age_list = list()
    for buy_age in buy_age_raw :
        percent = buy_age.text[:-1]
        if percent :
            buy_age_list.append(int(percent))
    if len(buy_age_list) == 0:
        buy_age_list = None

    return buy_age_list


# 🚀 item을 구매하는 성별 비율
def get_buy_gender_list(driver : webdriver.Chrome) -> Optional[str]: 
    buy_gender_raw = driver.find_elements(By.CSS_SELECTOR, value="dl.label_info > dd")
    buy_gender_list = list()
    for buy_gender in buy_gender_raw :
        percent = buy_gender.text[:-1]
        if percent :
            buy_gender_list.append(int(percent))

    if len(buy_gender_list) == 0:
        buy_gender_list = None

    return buy_gender_list

def get_rel_codi_url_list(driver: webdriver.Chrome, item_id, codi_id) -> Optional[str]:
    url_list = driver.find_elements(By.CSS_SELECTOR, value='div.tab.coordi > ul.style_list > li.list_item > a.img-block')
    
    # 현재 아이템과 연결된 다른 코디들의 url을 가져오기
    # 같은 제품이지만 다른 색상들도 모두 포함
    for i in range(len(url_list)):
        url_list[i] = url_list[i].get_attribute('href')

    # 하나씩 코디 URL을 돌면서 확인
    rel_codi_url_list = list()
    for rel_codi_url in url_list:

        ## 이미 크롤링 된 적 있는 코디인지 확인
        rel_codi_id = rel_codi_url.split("/")[-1]
        if str(rel_codi_id) in codi_id:
            print ("현재 이 아이템과 연결된 코디는 이미 크롤링 된 적이 있는 코디입니다.")
            continue

        ## 해당 코디에 진짜 동일한 아이템이 존재하는지 확인
        contains_item = False
        driver.get(rel_codi_url)
        rel_codi_items = driver.find_elements(By.CSS_SELECTOR, value='.swiper-slide > .box-img > .styling_img')
        for rel_items in rel_codi_items:
            rel_item_url = rel_items.get_attribute('href')
            rel_item_id = rel_item_url.split("/")[-2]
           
            if rel_item_id == item_id:
                contains_item = True
                break
    
        ## 진짜로 동일한 아이템이 존재하는 경우
        if contains_item == True:
            print (f"현재 아이템 #{item_id}와 연결된 코디 #{rel_codi_id} 에 동일한 아이템이 존재합니다. 연결 코디로 저장합니다.")
            rel_codi_url_list.append(rel_codi_url)
        else:
            print (f"현재 아이템 #{item_id}와 연결된 코디 #{rel_codi_id} 에는 동일한 아이템이 존재하지 않습니다. 색상이 다른데 연결된 코디의 경우 크롤링을 따로 진행하지 않습니다.")

    return rel_codi_url_list
        

# 🚀 크롤링 결과를 저장할 excel 파일 생성
def make_workbooks() -> Tuple[Workbook, ...]:
    workbooks = list()

    for _ in range(7):
        workbook = openpyxl.Workbook()
        workbooks.append(workbook)
    
    return tuple(workbooks)
    

# 🚀 위에서 만든 엑셀파일들에 대해서 하나의 sheet들을 생성
def make_worksheets(workbooks: Tuple[Workbook, ...]) -> Tuple[Worksheet, ...]:
    worksheets = list()
    for workbook in workbooks:
        worksheet = workbook.active
        worksheets.append(worksheet)

    # rel_codi_url 을 제외하고 나머지 xlsx 불러오기        
    worksheets[0].append(["id",  "name", "big_class", "mid_class", "brand", "serial_number", "gender",
                   "season", "cum_sale", "view_count", "likes", "rating", "price", "url", "img_url"])
    worksheets[1].append(["id", "tag"])
    worksheets[2].append(["id", "four_season"])
    worksheets[3].append(["id", "fit"])
    worksheets[4].append(["id", "buy_age_18", "buy_age_19_23", "buy_age_24_28", 
                           "buy_age_29_33", "buy_age_34_39", "buy_age_40"])
    worksheets[5].append(["id", "buy_men", "buy_women"])
    worksheets[6].append(["id", "rel_codi_url"])

    return tuple(worksheets)


# 🚀 크롤링 완료된 정보들을 파일로 저장
def save_workbooks(workbooks: Tuple[Workbook, ...], sort_opt: str, store_opt: str) -> None:


    path = '/opt/ml/input/data/' + store_opt + '/' + sort_opt + '/item'

    os.makedirs(path, exist_ok=True)
    
    workbooks[0].save(os.path.join(path, "item.xlsx"))
    workbooks[1].save(os.path.join(path, "item_tag.xlsx"))
    workbooks[2].save(os.path.join(path, "item_four_season.xlsx"))
    workbooks[3].save(os.path.join(path, "item_fit.xlsx"))
    workbooks[4].save(os.path.join(path, "item_buy_age.xlsx"))
    workbooks[5].save(os.path.join(path, "item_buy_gender.xlsx"))
    workbooks[6].save(os.path.join(path, "item_rel_codi_url.xlsx"))

    print ("Saving Done..")


# 🚀 각 알맞는 sheet에 크롤링된 정보들 추가
def save_to_sheets(worksheets: Tuple[Worksheet, ...], item_info: EasyDict) -> None:
    # item.xlsx 정보
    worksheets[0].append([
        item_info.id,
        item_info.name,
        item_info.big_class,
        item_info.mid_class,
        item_info.brand,
        item_info.serial_number,
        item_info.gender,
        item_info.season,
        item_info.cum_sale,
        item_info.view_count,
        item_info.likes,
        item_info.rating,
        item_info.price,
        item_info.item_url,
        item_info.img_url,
    ])

    # item_tag.xlsx 정보
    if item_info.tags_list:
        for tag in item_info.tags_list:
             worksheets[1].append([item_info.id, tag])

    # item_four_season.xlsx 정보
    if item_info.four_season_list:
        for four_season in item_info.four_season_list:
            worksheets[2].append([item_info.id, four_season])

    # item_fit.xlsx 정보
    if item_info.fit_list:
        for fit in item_info.fit_list:
            worksheets[3].append([item_info.id, fit])

    # item_buy_age.xlsx 정보
    if item_info.buy_age_list:
        worksheets[4].append([item_info.id] + item_info.buy_age_list)

    # item_buy_gender.xlsx 정보
    if item_info.buy_gender_list: 
        worksheets[5].append([item_info.id] + item_info.buy_gender_list)

    if item_info.rel_codi_url_list:
        item_info.rel_codi_url_list = set(item_info.rel_codi_url_list)
        for rel_codi_url in item_info.rel_codi_url_list:
            worksheets[6].append([item_info.codi_id, rel_codi_url])


# 🚀 디버깅: 크롤링 결과 출력
def print_crawled_item_info(item_info: EasyDict) -> None:
    print ("-" * 15, "crawled item information..")
    for key, value in zip(item_info.keys(), item_info.values()):
        print (key, ":", value)
    print()