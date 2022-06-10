# Introduction
서비스의 front-end 소스가 담겨있습니다. server의 main.py와 연결되어 있습니다.

# How to Run?
`final-project-level3-recsys-07/streamlit_frontend/` 폴더로 이동해준 후에
```
streamlit run app.py
가 되지 않는다면
streamlit run app.py --server.port <portnumber>
```
- app.py : 요소들을 나열해둔 frontend의 main파일입니다.
- utils.py : app.py에서 데이터 처리 기능을 빼서 한 번에 담아둔 파일입니다.
- rule_based.py : 사이트에서 사용하는 모델이 담긴 파일입니다.

# Install Streamlit
```
pip install streamlit
```