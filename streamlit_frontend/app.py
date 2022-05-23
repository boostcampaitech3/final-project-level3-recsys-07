from faulthandler import disable
import imp
from logging import PlaceHolder
import streamlit as st
from utils import paginator, get_images_url
from st_clickable_images import clickable_images
import pandas as pd
from rule_based import get_item_recommendation


st.image('https://www.noiremag.com/wp-content/uploads/2020/08/2020-fashion-trends-feature-696x392-1.jpg')
st.title('YUSINSA')

df=pd.read_excel('/opt/ml/input/data/raw_codishop/item_tag.xlsx',engine='openpyxl')
tags=pd.unique(df['tag'])
STATE_KEYS_VALS = [
    ("result", []),
    ("input_status", True),
    ("my_cloth",None),
    ("end_survey",False),
    ('clicked_item',-1)
]
for k, v in STATE_KEYS_VALS:
    if k not in st.session_state:
        st.session_state[k] = v

def search(tag):
    if tag != []:
        temp=df[df['tag']==tag[0]]
        st.session_state['result'] = temp.iloc[:,0].tolist() # 일단 id 하나만

def input_status_change():
    st.session_state['input_status']=False

with st.container():
    # TODO : 검색 리스트 생성
    # TODO : 검색 이벤트 연결 -> on.click
    c1_col1,c1_col2 = st.columns(2)

    with c1_col1:
        input=st.multiselect(label='👕👖 갖고있는 옷을 검색하세요',options = tags,on_change=input_status_change)
        
    with c1_col2:
        st.write("")
        st.write("")
        input_button = st.button('🔍', on_click=search,args =(input,), disabled=st.session_state['input_status'])       
    

if len(st.session_state['result'])!=0:
    st.markdown("""---""")
    image_dict=get_images_url([st.session_state['result']]) #list 반환
    image_list=list(image_dict.values())
    item_ids=list(image_dict.keys())

    with st.container():
        st.markdown("### 갖고있는 옷과 가장 비슷한 사진을 골라주세요")
        image_iterator = paginator('',image_list,items_per_page=5,on_sidebar=False)
        indices_on_page, images_on_page = map(list, zip(*image_iterator))
        st.session_state['my_cloth']= clickable_images(images_on_page,titles=[f"Image #{str(i)}" for i in range(5)],
                                    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                    img_style={"margin": "5px", "height": "200px", "width" : "125px"},key='mySelect'
                                )
        st.session_state['clicked_item']=item_ids[indices_on_page[st.session_state['my_cloth']]] # id가  들어옴

        st.button('선택', disabled=st.session_state['clicked_item'] == -1)
        st.write(st.session_state['clicked_item'])
        st.write(get_item_recommendation(st.session_state['clicked_item']))


if st.session_state["clicked_item"]!=-1:
    st.markdown("""---""")
    with st.container():
        top_list=['https://image.msscdn.net/images/goods_img/20211224/2282033/2282033_2_500.jpg?t=20220503165501' for i in range(5)]
        pants_list=['https://image.msscdn.net/images/goods_img/20220307/2403053/2403053_1_220.jpg' for i in range(5)]
        shoes_list=['https://image.msscdn.net/images/goods_img/20210730/2044904/2044904_4_220.jpg' for i in range(5)]
        acc_list=['https://image.msscdn.net/images/goods_img/20220224/2382342/2382342_1_220.jpg' for i in range(5)]
        st.markdown('### 관련 코디를 보고싶은 옷을 골라보세요')
        st.markdown('#### 상의')
        top_click= clickable_images(top_list,titles=[f"Image #{str(i)}" for i in range(5)],
                                            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                            img_style={"margin": "5px", "height": "200px", "width" : "125px"},key='topSelect'
                                        )
        st.markdown(f"Image #{top_click} clicked" if top_click > -1 else "No image clicked")
        
        if st.session_state.topSelect!= None:
            st.write(st.session_state)
            st.write(st.session_state.topSelect)
        st.markdown('#### 바지')
        pants_click= clickable_images(pants_list,titles=[f"Image #{str(i)}" for i in range(5)],
                                            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                            img_style={"margin": "5px", "height": "200px", "width" : "125px"},key='pantsSelect'
                                        )
        # st.markdown(f"Image #{pants_click} clicked" if pants_click > -1 else "No image clicked")

        st.markdown('#### 신발')
        shoes_click= clickable_images(shoes_list,titles=[f"Image #{str(i)}" for i in range(5)],
                                            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                            img_style={"margin": "5px", "height": "200px", "width" : "125px"},key='shoesSelect'
                                        )
        # st.markdown(f"Image #{shoes_click} clicked" if shoes_click > -1 else "No image clicked")
        
        st.markdown('#### 악세사리')
        acc_click= clickable_images(acc_list,titles=[f"Image #{str(i)}" for i in range(5)],
                                            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                            img_style={"margin": "5px", "height": "200px", "width" : "125px"},key='accSelect'
                                        )
        # st.markdown(f"Image #{acc_click} clicked" if acc_click > -1 else "No image clicked")


    st.markdown("""---""")

    with st.container():
        st.markdown('### 추천코디')
        fit_list=['https://image.msscdn.net/images/style/list/l_3_2022051912523500000002502.jpg' for i in range(5)]
        notfit_list=['https://image.msscdn.net/images/style/list/l_2_2022020309572400000037350.jpg' for i in range(5)]

        st.image(fit_list, use_column_width=False, caption=["some generic text"] * len(fit_list),width=125)
        st.markdown('#### 가진 옷과는 어울리지 않아요')
        st.image(notfit_list, use_column_width=False, caption=["some generic text"] * len(notfit_list),width=125)