# Introduction
수집한 데이터를 전처리하고 룰베이스에 필요한 상호작용 행렬을 생성하는 소스입니다.

## How to Run?
1. 데이터 전처리
    ``` 
    python3 preprocess.py
    ```

2. 상호작용 행렬 생성
    ```
    python3 cluster_item_interaction_matrix.py
    ```

<br>

## 디렉터리 구조
```
    📦Preprocessing
    ┣ 📜preprocess.py
    ┣ 📜cluster_item_interaction_matrix.py
    ┣ 📂utils
    ┃ ┣ 📂codi
    ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┗ 📜codi_preprocess_functions.py
    ┃ ┣ 📂item
    ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┗ 📜item_preprocess_functions.py
    ┃ ┣ 📜utils_codi.py
    ┃ ┣ 📜utils_item.py
    ┃ ┣ 📜utils_item_fit.py
    ┃ ┗ 📜utils_item_four_season.py
    ┣ 📂testing_files
    ┃ ┣ 📜color_extraction_test.ipynb
    ┃ ┗ 📜imgae_loading_tester.ipynb
    ┗ 📜README.md
```

<br>

## Directory Explanation

<p align="center">
<img src="https://user-images.githubusercontent.com/44887886/173222170-ae7ce245-a8ca-4e22-8e7d-65545a0647cf.png" width="800" height="450">
</p>

- 📜 `preprocess.py` : 위의 그림과 같이 정해진 순서대로 전처리를 진행합니다.
- 📜 `Cluster_item_interaction_matrix.py` : 룰베이스에 필요한 상호작용 행렬을 생성합니다.
- 📂 utils : 전처리에 필요한 함수가 모여있습니다.
- 📂 testing_files : 수집한 데이터를 검수합니다.
    - 📜 `color_extraction_test.ipynb` : 아이템 이미지에서 추출한 색상이 올바른지 검수합니다.
    - 📜 `imgae_loading_tester.ipynb` : 아이템 이미지가 로딩되는지 검수합니다.


<br>

## 데이터 전처리 설명

### Item 속성 Table

1. Item Table

    | Feature | 설명        | 결측치 처리                 | 비고 |
    |:-------:|:---------:|:-------------------------:|:---:|
    |id       | 아이템 ID   |X|     |
    |name     | 상품명      |X|     |
    |big_class| 대분류      |X| 유사한 대분류 통일, 악세사리 및 기타 대분류 제거 |
    |mid_class| 중분류      |X| 유사한 중분류 통일     |
    |brand    | 브랜드      |X|      |
    |serial_number| 품번    |X|      |
    |price    | 가격        |X|      |
    |likes    | 좋아요 수    | 0                         |   |
    |R, G, B  | 색상 R, G, B|X| 이미지에서 가장 높은 비율을 차지하는 색상의 R, G, B 값 추출|
    |rating   | 평점        | 모든 아이템 평점의 평균|       |      |
    |gender   | 성별        | '유니섹스'                  |      |
    |season_year | 출시 연도 | NULL                      | season feature에서 추출 |
    |season   | 출시 시즌    | NULL                      | 출시 연도를 제거하고 계절 정보만 추출 |
    |view_count| 조회 수     | NULL                      | str에서 Int로 타입 변환 |
    |cum_sale  | 누적판매 수  | NULL                      | str에서 Int로 타입 변환 |
    |most_bought_age_class|구매 비율이 가장 높은 연령층 클래스|6 | Item_buy_age 테이블 참조 |
    |men_bought_ratio|남성 사용자의 구매 비율|50             | Item_buy_gender 테이블 참조 |
    |color_id| 색상 아이디    |X| R, G, B 값을 활용해 클러스터링 |
    |cluster_id|클러스터 아이디 |X| 중분류와 색상을 활용해 클러스터링 |
    |img_url   |이미지 주소   |X|         |
    |url       |상품 페이지 주소|X|         |
                      

2. Item_fit Table

    | Feature | 설명        | 결측치 처리                 | 비고 |
    |:-------:|:----------:|:------------------------:|:---:|
    | id      | 아이템 ID    |X                        | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    | fit     | 핏         | 아이템 태그에서 핏 정보 활용    | Item_tag table 참조    |
                             

3. Item_tag Table
    
    | Feature | 설명        | 결측치 처리    | 비고 |
    |:-------:|:----------:|:-----------:|:---:|
    | id      | 아이템 ID    |X            | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    | tag     | 태그        |X             |   |
                           

4. Item_four_season Table

    | Feature     | 설명        | 결측치 처리                 | 비고 |
    |:-----------:|:----------:|:------------------------:|:---:|
    | id          | 아이템 ID    | X                  | Item table에서 대분류 필터링을 통해 제거된 아이템 제거 Id (동기화) | 
    | four_season | 사계절 정보   | 아이템의 출시 시즌 정보 활용    | Item table 참조    |
                          

5. Item_rel_codi_url Table

    | Feature     | 설명        | 결측치 처리         | 비고 |
    |:-----------:|:----------:|:----------------:|:---:|
    | id          | 아이템 ID   |X              | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) |
    | rel_codi_url| 아이템이 사용된 코디 페이지 주소 | |     |
                          

6. Item_buy_gender Table

    |   Feature   | 설명      | 결측치 처리   | 비고 |
    |:-----------:|:--------:|:----------:|:---:|
    | id          | 아이템 ID  |  X       | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    | buy_men     | 남성 사용자 구매 비율    |          |   |
    | buy_women   | 여성 사용자 구매 비율    |           |   |
                          

7. Item_buy_age Table

    |   Feature     | 설명                   | 결측치 처리   | 비고 |
    |:-------------:|:---------------------:|:----------:|:---:|
    | id            | 아이템 ID               |  X | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    | buy_age_18    | ~18세 사용자 구매 비율    | X          |     |
    | buy_age_19_23 | 19세~23세 사용자 구매 비율 |X           |     |
    | buy_age_24_28 | 24세~28세 사용자 구매 비율 |X           |     |
    | buy_age_29_33 | 29세~33세 사용자 구매 비율 |X           |     |
    | buy_age_34_39 | 34세~39세 사용자 구매 비율 |X           |     |
    | buy_age_40    | 40세~ 사용자 구매 비율     |X          |     |
                          

8. Item_codi_id Table

    |   Feature   | 설명      | 결측치 처리   | 비고 |
    |:-----------:|:--------:|:----------:|:---:|
    | id          | 아이템 ID  |X          |Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    | codi_id     | 코디 ID   |X          |      |    
                        
                                              


### Codi 속성 Table

1. codi Table

    | Feature | 설명          | 결측치 처리   | 비고 |
    |:-------:|:------------:|:----------:|:---:|
    |id       | 코디 ID       |X          | Item_codi_id table에서 제거된 코디 Id 제거 (동기화) |
    |style    | 코디 스타일     |X          |     |
    |popularity| 조회 수       |sX         |     |
    |img_url  | 코디 이미지 주소 |X          |     |
    |url      | 상품 페이지 주소 |X          |     |


2. codi_tag Table

    | Feature | 설명          | 결측치 처리   | 비고 |
    |:-------:|:------------:|:----------:|:---:|
    |id       | 코디 ID       |X           |codi table에서 제거된 코디 Id 제거 (동기화) |
    |tag      | 코디 태그      |X           |     |


