from selenium import webdriver
from selenium.webdriver.common.by import By
from torch import set_autocast_enabled

def get_brand(product_info):
    try :
        brand = product_info[0].find_element(By.CSS_SELECTOR, value="a").text
    except :
        brand = None
    return brand

def get_serial_number(product_info):
    serial_number = product_info[0].get_attribute('innerHTML').split()[-1]
    return serial_number

def get_big_class(category : webdriver.Chrome) -> str : 
    try :
        big_class = category[0].text
    except :
        big_class = None
    return big_class

def get_mid_class(category : webdriver.Chrome) -> str : 
    try :
        mid_class = category[1].text
    except :
        mid_class = None
    return mid_class

def get_season(product_info):
    try:
        #season = product_info[1].find_element(By.CSS_SELECTOR, "strong").text
        season = product_info[1].text
        if len(season) == 0 :
            season = None
    except:
        season = None
    
    return season

def get_gender(driver):
    try :
        gender = driver.find_element(By.CSS_SELECTOR, "ul.product_article > li > p.product_article_contents > span.txt_gender").text
    except :
        gender = None
    return gender

def get_view(driver) :
    view = driver.find_element(By.CSS_SELECTOR, "ul.product_article > li > p.product_article_contents > strong#pageview_1m").text
    if len(view) == 0 : 
        view = None
    return view

def get_cum_sale(driver):
    try:
        cum_sale = driver.find_element(By.CSS_SELECTOR, value="ul.product_article > li > p.product_article_contents > strong#sales_1y_qty").text
        if len(cum_sale) == 0 :
            cum_sale = None
    except :
        cum_sale = None
    
    return cum_sale

def get_likes(driver) :
    try:
        likes = int(driver.find_element(By.CSS_SELECTOR, value="ul.product_article > li > p.product_article_contents span.prd_like_cnt").text)
    except:
        likes = None
    return likes

def get_rating(driver) :
    try:
        rating = float(driver.find_element(By.CSS_SELECTOR, "span.prd-score__rating").text)
    except:
        rating = None
    return rating

def get_color(menu):
    color = []
    if not menu or len(menu) == 1: return None
    colors = menu[0].find_elements(By.CSS_SELECTOR, "option")
    
    for i in range(1, len(colors)):
        if colors[i].text: color.append(colors[i].text)
    return color

def get_size(menu):
    size = [] 
    if not menu: return None
    if len(menu) == 1: sizes = menu[0].find_elements(By.CSS_SELECTOR, "option")
    else: sizes = menu[1].find_elements(By.CSS_SELECTOR, "option")
    
    for i in range(1, len(sizes)):
        if sizes[i].text: size.append(sizes[i].text)
    return size

def get_price(driver):
    price = driver.find_element(By.CSS_SELECTOR, "span.product_article_price").text[:-1]
    price = int(price.replace(',', ''))
    return price

def get_buy_age_list(driver):
    buy_age_raw = driver.find_elements(By.CSS_SELECTOR, value="ul.bar_wrap > li span.bar_num")
    buy_age_list = list()
    for buy_age in buy_age_raw :
        percent = buy_age.text[:-1]
        if percent :
            buy_age_list.append(int(percent))
    if len(buy_age_list) == 0:
        buy_age_list = None

    return buy_age_list

def get_buy_gender_list(driver): 
    buy_gender_raw = driver.find_elements(By.CSS_SELECTOR, value="dl.label_info > dd")
    buy_gender_list = list()
    for buy_gender in buy_gender_raw :
        percent = buy_gender.text[:-1]
        if percent :
            buy_gender_list.append(int(percent))
    if len(buy_gender_list) == 0:
        buy_gender_list = None
    return buy_gender_list

def get_fs_and_fit(driver) :
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

def get_tags_list(driver) :
    tags_list = list()
    tags_raw = driver.find_elements(By.CSS_SELECTOR, value="li.article-tag-list a.listItem")
    for tag in tags_raw :
        tags_list.append(tag.text[1:])
    if len(tags_list) == 0:
        tags_list = None
    return tags_list

def get_four_season(driver) :
    guide_all = driver.find_elements(By.CSS_SELECTOR, value="table.table-simple tr")
    four_season = list()
    for guide in guide_all :
        t = guide.find_element(By.CSS_SELECTOR, value="th").text
        if t == "계절" :
            seasons = guide.find_elements(By.CSS_SELECTOR, value="td.active")
            for season in seasons :
                four_season.append(season.text)
    if len(four_season) == 0:
        four_season=None
    return four_season