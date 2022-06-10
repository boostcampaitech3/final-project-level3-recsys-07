# Introduction
패션사이트인 MUSINSA에서 코디샵 또는 코디맵의 코디와 아이템들을 크롤링하는 소스입니다. Python의 Selenium을 통해서 크롤링을 진행하고 있습니다. 필요한 패키지는 `requirements.txt` 에서 다운 받을 수 있으며, 드라이버는 아래 [ChromeDriver 설치 페이지](#installing-chrome-driver)에서 자세한 내용을 확인할 수 있습니다.

## How to Run?

1. Codi Crawling

    ```
    python3 ./codishop/codi_crawler/crawl_codi.py
    python3 ./codimap/codi_crawler/crawl_codi.py
    ```
2. Item Crawling

    ```
    python3 ./codishop/item_crawler/crawl_item.py
    ```

더 많은 파일은 [크롤링 디렉토리 구조 설명](#directory-explanation)을 참고 부탁드립니다.

<br>

## 디렉토리 구조

```
📦crawler
 ┣ 📂codimap
 ┃ ┗ 📂codi_crawler
 ┃ ┃ ┣ 📜crawl_codi.py
 ┃ ┃ ┗ 📜utils.py
 ┣ 📂codishop
 ┃ ┣ 📂codi_crawler
 ┃ ┃ ┣ 📜crawl_codi.py
 ┃ ┃ ┣ 📜extra_crawling.py
 ┃ ┃ ┗ 📜utils.py
 ┃ ┗ 📂item_crawler
 ┃ ┃ ┣ 📜item_crawler.py
 ┃ ┃ ┣ 📜item_crawler_depth.py
 ┃ ┃ ┣ 📜utils.py
 ┃ ┃ ┗ 📜utils_depth.py
 ┗ 📜README.md
```

<br>

## Directory Explanation

- 📂 codimap : MUSINSA 에서 codimap에 존재하는 코디 또는 아이템을 크롤링합니다.
- 📂 codishop : MUSINSA 에서 codishop 에 존재하는 코디 또는 아이템을 크롤링합니다.
    - 📂 codi_crawler : 코디 크롤링을 진행합니다. `extra_crawling.py`를 통해 특정 url의 코디들을 크롤링할 수도 있습니다.
    - 📂 item_crawler : 아이템 크롤링을 진행합니다.  
        - 📜 `item_crawler_detph.py` : 아이템을 크롤링할 때, 연관된 코디의 아이템들까지 모두 크롤링을 진행합니다. 아이템과 코디의 연관정보를 얻고 싶을 때 사용됩니다.

<br>

## Installing Chrome Driver
Chrome Driver 설치링크: https://chromedriver.chromium.org/downloads

- 위 링크에서 사용하는 chrome 버전에 맞춰 설치를 진행합니다.
- `chromedriver.exe`는 `/crawler` 폴더 내부에 위치해야합니다.
- chrome 버전 확인  
    `chrome://settings/help` 에서 확인

<br>

## Installing Selenium

```bash
pip install selenium
apt install chromium-chromedriver
```
