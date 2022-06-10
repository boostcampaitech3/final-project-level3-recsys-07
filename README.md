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