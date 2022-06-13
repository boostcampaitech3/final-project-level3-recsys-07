![logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

# 서비스 구조

|As-Is|To-Be|
|:-----:|:-----:|
|![image](https://user-images.githubusercontent.com/10546369/173264689-52f2e4db-872e-428b-9a81-cda88a57275e.png)|![image](https://user-images.githubusercontent.com/10546369/173264655-39000089-05d3-43fd-9276-905355c17699.png)|

# 디렉토리 구조
```
.
|-- 📜 README.md
|-- 📜 __init__.py
|-- 📜 __main__.py
|-- 📜 config.yaml
|-- 📜 main.py
`-- 📂services
    |-- 📜 __init__.py
    |-- 📜 crud.py
    `-- 📜 recomendation.py
```

# 서버 실행 방법
0. 사전 설정
    ```shell
    > apt-get update
    > apt install curl
    ```

1. Poetry 설치하기
    ```shell
    > curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    ```

2. 환경변수 설정
    ```shell
    > source $HOME/.poetry/env 
    ```

3. poetry install
    ```shell
    > poetry install
    ```
4. poetry 가상환경 실행
    ```shell
    > poetry shell
    ```

5. 서버 실행

    ```shell
    > cd final-project-level3-recsys-07
    > python -m server 
    ```
    or
    ```shell
    > bash server_run.sh
    ```

6. config.yaml

    DB 연결을 위해 다음과 같은 형식의 config.yaml이 /server 디렉토리에 있어야함
    ```
    mysql:
        user : <id>
        password : <password>
        host : <database_address>
        db : <schema_name>
    ```

# API Docs

<details>
<summary>Toggle</summary>
<div markdown="1">

## FastAPI
#### Version: 0.1.0

### /item/image/{item_id}

#### GET
##### Summary:

item_id 로 부터 image의 uri를 받아오는 API

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| item_id | path |  | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /items/info/

#### POST
##### Summary:

Item에 대한 정보를 return 하는 api
Read Item Info

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /rule_base/recommendation/{item_id}

#### GET
##### Summary:

Rule base로 만들어진 추천 결과를 return 하는 api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| item_id | path |  | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /lightGCN/recommendation/{item_id}

#### GET
##### Summary:

lightgcn으로 부터 추론된 추천 결과를 return 하는 api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| item_id | path |  | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /MultiVAE/recommendation/{item_id}

#### GET
##### Summary:

**(TODO)**MultiVAE로부터 추론뢴 추천 결과를 return 하는 api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| item_id | path |  | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /items/names

#### POST
##### Summary:

item의 이름을 return 하는 api

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /codi

#### GET
##### Summary:

Read Codi

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| select_item | query |  | Yes | integer |
| pick_item | query |  | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /codis/info

#### POST
##### Summary:

코디에 대한정보를 return 하는 api

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /items

#### POST
##### Summary:

Read Item From Mid Class

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /mid_class

#### GET
##### Summary:

Read Item Mid Class

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /tags

#### GET
##### Summary:

item의 tag 키워드를 return 하는 api

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

### /item/cluster/{item_id}

#### GET
##### Summary:

item의 cluster id를 return 하는 api

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| item_id | path |  | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

### /items/prob/

#### POST
##### Summary:

추천 확률을 return 하는 api

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

</div>
</details>