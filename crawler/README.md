## ChromeDriver 설치

https://chromedriver.chromium.org/downloads

- 위 링크에서 사용하는 chrome 버전에 맞춰 설치 진행

- `chromedriver.exe`는 `/crawler` 폴더 내부에 위치해야함

- chrome 버전 확인  
    `chrome://settings/help`
    에서 확인 가능

## selenium 설치
pip install selenium

apt install chromium-chromedriver

## 변경사항
```
2022.5.31 (by som)
[crawl_codi]
1. codi_item_id -> item_codi_id로 name 변경
2. item_codi_id column: ['id', 'codi_id'] -> ['item_id', 'codi_id']로 변경
3. item_codi_id save path: raw/codishop/view/codi -> raw/codishop/view/item 으로 변경

[crawl_item]
1. item column : 'view' -> 'view_count'로 변경
```