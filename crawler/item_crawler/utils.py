from selenium import webdriver
from selenium.webdriver.common.by import By

def get_rating(driver) :
    try :
        rating = float(driver.find_element(By.CSS_SELECTOR, value="div.estimate-point > p span").text)
    except :
        rating = None
    return rating

def get_likes(driver) :
    try :
        likes = int(driver.find_element(By.CSS_SELECTOR, value="li.product_section_like span").text)
    except :
        likes = None
    return likes
    
def get_cum_sale(driver):
    try:
        cum_sale = int(driver.find_element(By.CSS_SELECTOR, value="li#li_sales_1y strong").text)
    except :
        cum_sale = None
    return cum_sale

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
    return four_season

def get_color(driver) :
    color = []
    colors = driver.find_elements(By.CSS_SELECTOR, "div#goods_opt_area > select#option1 > option")
    for i in range(1, len(colors)):
        color.append(colors[i].text)
    if len(color) == 0:
        color = None
    return color

def get_size(driver) :
    size = []
    sizes = driver.find_elements(By.CSS_SELECTOR, "div#goods_opt_area > select#option2 > option")
    for i in range(1, len(sizes)):
        size.append(sizes[i].text)
    if len(size) == 0:
        size = None
    return size