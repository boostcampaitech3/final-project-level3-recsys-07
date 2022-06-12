# Introduction
수집한 데이터를 전처리하는 소스입니다.

## How to Run?

1. 데이터 전처리
    ``` 
    python3 preprocess.py
    ```

2. 상호작용 행렬 생성
    ```
    python3 cluster_item_interaction_matrix.py
    ```

## 디렉터리 구조
```
📦Preprocessing
|-- 📜preprocess.py
|-- 📜cluster_item_interaction_matrix.py
|-- 📂testing_files
|   |-- 📜color_extraction_test.ipynb
|   `-- 📜imgae_loading_tester.ipynb
|-- 📂utils
|   |-- 📂codi
|   |   |-- 📜__init__.py
|   |   `-- 📜codi_preprocess_functions.py
|   |-- 📂item
|   |   |-- 📜__init__.py
|   |   `-- 📜item_preprocess_functions.py
|   |-- 📜utils_codi.py
|   |-- 📜utils_item.py
|   |-- 📜utils_item_fit.py
|   `-- 📜utils_item_four_season.py
`-- 📜README.md
```