from faulthandler import disable
from logging import PlaceHolder
import streamlit as st
from utils import *

import pandas as pd
from rule_based import get_item_recommendation

from PIL import Image

def search(tag_list):
    if tag_list != []:
        st.session_state['result'] = get_tag_id(tag_list)

def input_status_change():
    st.session_state['input_status']=False

def set_value(key):
    st.session_state[key] = st.session_state["key_" + key]


def select_item(index: int):
    st.session_state['clicked_item'] = item_ids[index] # id가  들어옴
    st.session_state['survey_end'] = True

def pick_item(idx:int,item_ids):
    st.session_state['picked_item']=item_ids[idx]
    st.session_state['picked_end']=True

def home():
    for key in st.session_state.keys():
        del st.session_state[key]
    set_state_key(STATE_KEYS_VALS)
    input_status_change()
    if survey_container:
        survey_container.empty()
    try:
        if pick_container:
            pick_container.empty()
    except:
        pass
    
def set_state_key(STATE_KEYS_VALS):
    for k, v in STATE_KEYS_VALS:
        if k not in st.session_state:
            st.session_state[k] = v

STATE_KEYS_VALS = [
    ("result", []),
    ("input_status", True),
    ("my_cloth",None),
    ("end_survey",False),
    ('clicked_item',-1),
    ('my_cloth_button',False), 
    ('survey_end',False),
    ('codi_click', None),
    ('picked_item',None),
    ('picked_end',False)
]
set_state_key(STATE_KEYS_VALS)

st.set_page_config(layout='wide')

(_, l,r, _) = st.columns([1, 4,9, 1])
with l:
    st.title("What's In Your Closet?") 
    st.button('🏠',on_click=home, args=())
with r:
    st.image('./main_image-removebg-preview.png')
    

survey_container=st.empty()
with survey_container.container():
    with st.container():
        # TODO : 검색 리스트 생성
        # TODO : 검색 이벤트 연결 -> on.click
        
        (_, c, _) = st.columns([1, 9, 1])

        item_tags = get_item_tags()

        with c:
            input=st.multiselect(label=' ', options = item_tags , on_change=input_status_change)
        (_, left,right, _) = st.columns([8,1,1,8])
        with left:
            input_button = st.button('🔍', on_click= search ,args = ([input]), disabled=st.session_state['input_status'])
        with right:
            random_button=st.button('🎲')   
        
    if len(st.session_state['result'])!=0:
        st.markdown("""---""")

        item_dict=get_item_info(st.session_state['result'])  #['result']에는 키워드 #list 반환
        
        image_list=list(item_dict['img_url'])
        item_ids=list(item_dict['item_ids'])
        item_name = list(item_dict['item_name'])

        page_limit = len(image_list) // 10
        page_limit = max(1,page_limit) # slider max가 min이랑 동일한 경우 에러 발생
        
        is_disable = False
        if page_limit == 1:
            is_disable=True
        
        with st.container():
            st.markdown("### 갖고있는 옷과 가장 비슷한 사진을 골라주세요")

            page = st.slider('Select pages', 0, page_limit, 0, disabled=is_disable)

            idx = 0 + (page * 10)

            for row in range(2):
                for col_index, col in enumerate(st.columns(5)):
                    if idx >= len(image_list):
                        break

                    clothes = image_list[idx]

                    with col:
                        st.image(get_image(clothes))
                        st.checkbox(
                            item_name[idx],
                            key = 'clothes-{}'.format(item_ids[idx]),
                            on_change = select_item,
                            args=(idx,),
                        )
                    idx+=1
            

if st.session_state['survey_end']: # 버튼이 눌리면
    survey_container.empty() # 위의 내용들 삭제하기
    pick_container=st.empty()
    with pick_container.container():
        st.write("선택한 아이템 : ")
        (_, center, _) = st.columns([1, 1, 1])
        with center:
            st.image(get_image_url(st.session_state['clicked_item']), width=500) # st.session_state['clicked_item'] : id
      
        codis=get_item_recommendation(st.session_state['clicked_item'])

        st.markdown('### 관련 코디를 보고싶은 옷을 골라보세요')
        for codi in codis.keys():
            codi_id=codis[codi]
            
            if len(codi_id)!=0:
                st.markdown(f'#### {codi}')

                codi_dict=get_item_info(codi_id)

                image_list=list(codi_dict['img_url'])
                item_ids=list(codi_dict['item_ids'])
                item_name = list(codi_dict['item_name'])

                codi_cnt = len(item_ids)
                idx = 0
                for col_index, col in enumerate(st.columns(5)):
                    if idx >= len(item_ids):
                        break

                    clothes = image_list[idx]

                    with col:
                        st.image(get_image(clothes))
                        checked=st.checkbox(
                            item_name[idx],
                            key = 'clothes-{}'.format(item_ids[idx]), #url이 key로 들어가게됨
                            on_change = pick_item,
                            args=(idx,item_ids,),
                        )

                    idx+=1

if st.session_state['picked_end']:
    pick_container.empty() # 지금껏 있던 내용들 모두 삭제
    with st.container():
        st.markdown('### 추천코디')
        # st.write(st.session_state['picked_item'])
        # st.write("코디리스트")
        codi_ids=get_codi(st.session_state['clicked_item'],st.session_state['picked_item'])
        
        codi_dict=get_codi_info(codi_ids)
        print(codi_dict)
        codi_image_list=list(codi_dict['img_url'])
        result_codi_ids=list(codi_dict['item_ids'])
        codi_style_list = list(codi_dict['item_name'])

        st.image(codi_image_list, caption = codi_style_list, use_column_width=False,width=300)
