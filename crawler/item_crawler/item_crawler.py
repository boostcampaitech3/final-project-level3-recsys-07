from selenium import webdriver
from selenium.webdriver.common.by import By
from easydict import EasyDict
from utils import *

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(argument='--headless') 
chrome_options.add_argument(argument='--no-sandbox')
chrome_options.add_argument(argument='--disable-dev-shm-usage')

URL_PATH = "https://www.musinsa.com/app/styles/lists"
driver = webdriver.Chrome('/opt/ml/workspace/crawler/item_crawler/chromedriver',chrome_options=chrome_options)
driver.get(URL_PATH)
driver.implicitly_wait(2) #페이지를 로딩하는 시간동안 대기

button = driver.find_element(By.CSS_SELECTOR, "button.global-filter__button--mensinsa")
button.click()

container =  driver.find_elements(By.CSS_SELECTOR, "ul.style-list > li")
BASE_CODI_URL = "https://www.musinsa.com/app/styles/views/"

codi = []
for codi_element in container:
    img_src = codi_element.find_element(By.CSS_SELECTOR, 'div.style-list-item__thumbnail > a').get_attribute('onclick')
    codi_id = img_src.split("'")[1]
    codi_url = BASE_CODI_URL + codi_id
    codi.append((codi_id, codi_url))

cnt = 0
for codi_id, codi_url in codi:
    print(f"Crawling for CODI ID : {codi_id}\n")

    driver.get(codi_url)
    driver.implicitly_wait(0.5)
    item_list = driver.find_elements(By.CSS_SELECTOR, 'div.styling_list > div.swiper-slide')
    item_urls = []
    
    for item in item_list:
        item_url = item.find_element(By.CSS_SELECTOR, "a.brand_item").get_attribute('href')
        item_urls.append(item_url)

    for item_url in item_urls:
        driver.get(item_url)
        driver.implicitly_wait(0.5) #페이지를 로딩하는 시간동안 대기
        print(f"Crawling item : {item_url}")

        rating = get_rating(driver)
        likes = get_likes(driver)
        cum_sale = get_cum_sale(driver)
        buy_age_list = get_buy_age_list(driver)
        buy_gender_list = get_buy_gender_list(driver)
        four_season_list, fit_list = get_fs_and_fit(driver)
        tags_list = get_tags_list(driver)
        id = item_url.split('/')[-2]
        name = driver.find_element(By.CSS_SELECTOR, "span.product_title > em").text
        category = driver.find_elements(By.CSS_SELECTOR, "p.item_categories > a")
        big_class = category[0].text
        mid_class = category[1].text
        product_info = driver.find_elements(By.CSS_SELECTOR, "ul.product_article > li > p.product_article_contents")
        brand = product_info[0].find_element(By.CSS_SELECTOR, "strong > a").text
        serial_number = product_info[0].find_element(By.CSS_SELECTOR, "strong").get_attribute('innerHTML').split()[-1]
        season = product_info[1].find_element(By.CSS_SELECTOR, "strong").text
        gender = product_info[1].find_element(By.CSS_SELECTOR, "span.txt_gender").text
        #view = product_info[2].find_element(By.CSS_SELECTOR, "strong#pageview_1m").text
        view = get_view(driver)
        price = driver.find_element(By.CSS_SELECTOR, value="span.product_article_price").text
        img_url = driver.find_element(By.CSS_SELECTOR, "div.product-img > img").get_attribute('src')
        
        features = [rating,likes, cum_sale, buy_age_list, buy_gender_list,
            four_season_list, tags_list, id, name, big_class,
            mid_class, brand, serial_number, season, gender,
            view, price, img_url]

        print(features)
        print()
        driver.get(codi_url)
    cnt +=1
    if cnt == 2 :
        break


driver.close()

