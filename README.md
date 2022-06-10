## Members

<table align="center">
    <tr>
        <td align="center">백승주</td>
        <td align="center">서현덕</td>
        <td align="center">이채원</td>
        <td align="center">유종문</td>
        <td align="center">김소미</td>
    </tr>
    <tr height="160px">
        <td align="center">
            <img height="120px" weight="120px" src="https://avatars.githubusercontent.com/u/10546369?v=4"/>
        </td>
        <td align="center">
            <img height="120px" weight="120px" src="https://avatars.githubusercontent.com/u/96756092?v=4"/>
        </td>
        <td align="center">
            <img height="120px" weight="120px" src="https://avatars.githubusercontent.com/u/41178045?v=4"/>
        </td>
        <td align="center">
            <img height="120px" weight="120px" src="https://avatars.githubusercontent.com/u/91870042?v=4"/>
        </td>
        <td align="center">
            <img height="120px" weight="120px" src="https://avatars.githubusercontent.com/u/44887886?v=4"/>
        </td>
    </tr>
    <tr>
    </tr>
    <tr>
        <td align="center">
            <code>ML engineer</code>
        </td>
        <td align="center"><code></code></td>
        <td align="center"><code></code></td>
        <td align="center"><code></code></td>
        <td align="center"><code></code></td>
    </tr>
    <tr>
        <td align="center"><a href="https://github.com/halucinor">Github</a></td>
        <td align="center"><a href="">Github</a></td>
        <td align="center"><a href="">Github</a></td>
        <td align="center"><a href="https://github.com/killerWhale0917">Github</a></td>
        <td align="center"><a href="">Github</a></td>
    </tr>
    <tr>
        <td align="center">
          <code>백엔드</code> <code>프론트엔드</code>
        </td>
        <td align="center">
          <code>?</code> <code>?</code> <br> <code>?</code>
        </td>
        <td align="center">
          <code>?</code>
        </td>
        <td align="center">
          <code>데이터 크롤링</code><br><code>데이터 전처리</code>
        </td>
        <td align="center">
          <code>?</code> <code>?</code> <br> <code>?</code>
        </td>
    </tr>
</table>

## 목차

## 프로젝트 소개

- 사용자가 가진 옷들을 기반으로 여러 코디에 최대한 활용할 수 있는 옷을 추천해주는 서비스

- Rule Base, LightGCN 모델을 활용해서 사용자가 가지고 있는 옷과 어울리는 옷을 추천하고 두 옷을 조합한 코디를 추천

<div align= "center">
<img src="https://user-images.githubusercontent.com/10546369/173015652-adce2a8b-188b-4dba-b48b-c6331790dcdf.png"/>
</div>

### 추천 프로세스

사용자가 가진 옷 검색 → 비슷한 옷 선택 → 옷 추천 → 추천 결과 중 마음에 드는 옷 선택→ 관련 코디를 추천

## 서비스 시연

[**서비스 링크**](https://bit.ly/3NAqJQd)

*### TODO : 영상 or 서비스 gif 업로드*
`김소미`

## 디렉토리 구조

<details>
<summary>Toggle</summary>
<div markdown="1">

```
    .
    |-- EDA
    |   |-- EDA_codimap.ipynb
    |   |-- IIM_maker.ipynb
    |   `-- make_item_matrix_codimap.ipynb
    |-- README.md
    |-- crawler
    |   `-- codishop
    |-- models
    |   |-- LightGCN
    |   |-- Mult-VAE
    |   |-- Rule based
    |   |-- Rule_based
    |   |-- __init__.py
    |-- poetry.lock
    |-- preprocessing
    |   |-- cluster_item_interaction_matrix.py
    |   |-- preprocess.py
    |   |-- testing_files
    |   `-- utils
    |-- pyproject.toml
    |-- requirements.txt
    |-- resource
    |   |-- CCIM.csv
    |   |-- cluster_item_prob.csv
    |   `-- item.csv
    |-- server
    |   |-- README.md
    |   |-- __init__.py
    |   |-- __main__.py
    |   |-- __pycache__
    |   |-- config.yaml
    |   |-- main.py
    |   `-- services
    |-- server_run.sh
    `-- streamlit_frontend
        |-- app.py
        |-- config.yaml
        |-- main-image.png
        |-- readme.md
        |-- requirements.txt
        |-- streamlit_run.sh
        |-- test.ipynb
        `-- utils.py
```
</div>
</details>

## 상세 설명

### 1. 데이터 크롤링/전처리

*### TODO : README Link*
`유종문` `김소미`

### 2. 모델

*### TODO : README Link*
`서현덕`

### 3. 프론트엔드 서버

*### TODO : README Link*
`이채원`
### 4. 백엔드 서버

*### TODO : README Link*
`백승주`
