from ctypes import alignment
from faulthandler import disable
from math import floor
import streamlit as st
from utils import *
import random

def search(mid_class_list):
    if mid_class_list != []:
        st.session_state['result'] = get_mid_class_id(mid_class_list)


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

# (_, l,r, _) = st.columns([1, 4,9, 1])
# with l:
# st.title("What's In Your Closet?") 
st.button('🏠',on_click=home, args=())
st.markdown(f"<p style='text-align: center; font-size: 70px'><strong>What's In Your Closet ?</strong></p>", unsafe_allow_html=True)
# with r:

st.markdown(f"<p style='text-align: center;'><img src='https://user-images.githubusercontent.com/91870042/172782203-665dfca6-31de-48e6-a317-1c3816b23427.png' width=70% alt='Logo'></p>", unsafe_allow_html=True)  

    
#
#  st.markdown(f"<p style='text-align: center;'>❤️ 가진 옷과 매칭확률 : {int(item_prob[idx]*10000)/100}%</p>", unsafe_allow_html=True)

survey_container=st.empty()
with survey_container.container():
    with st.container():
        
        (_, c, _) = st.columns([1, 9, 1])
      
        item_mid_class = get_item_mid_class()
        with c:
            st.info("남성 옷을 대상으로 하고 있습니다. 태그를 많이 입력할수록 많은 결과가 나오니 최대 3개까지만 입력해주세요.")
            input=st.multiselect(label='검색하고 싶은 키워드를 입력해주세요 ex)치마, 반바지 같은 옷의 분류를 입력하면 검색을 잘 할 수 있어요',options = item_mid_class,on_change=input_status_change)
        (_, left2, left, right, _) = st.columns([8,1,1,1,8])
        with left2:
            st.button('🪄 리셋',on_click=home, args=())
        with left:
            random_button=st.button('🎲 랜덤')
        with right:
            input_button = st.button('🔍 검색', on_click= search ,args = ([input]), disabled=st.session_state['input_status'])

        
    if len(st.session_state['result'])!=0 or random_button==True:
        st.markdown("""---""")
        if random_button==True:
            search([str(item_mid_class[random.randint(0,len(item_mid_class))])])
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
                            key = 'search-{}'.format(item_ids[idx]),
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
        
        clicked_cluster_id=cluster_id(st.session_state['clicked_item']) # prob를 위한 변수
        

        codis= get_recommendation(st.session_state['clicked_item'])
        
        clicked_item_info = get_item_info([st.session_state['clicked_item']])
        clicked_big_class = clicked_item_info['big_class'][0]

        st.markdown('### 관련 코디를 보고싶은 옷을 골라보세요')
        for codi in codis.keys():
            codi_id=codis[codi]

            if clicked_big_class == codi: continue
            if len(codi_id)!=0:
                if codi == '아우터': st.markdown(f'#### 🧥 {codi}')
                elif codi == '상의': st.markdown(f'#### 👕 {codi}')
                elif codi == '바지': st.markdown(f'#### 👖 {codi}')
                elif codi == '모자': st.markdown(f'#### 🧢 {codi}')
                elif codi == '가방': st.markdown(f'#### 🎒 {codi}')
                elif codi == '신발': st.markdown(f'#### 👟 {codi}')
                else: st.markdown(f'#### {codi}')

                codi_dict=get_item_info(codi_id)  

                item_prob= get_prob_info(clicked_cluster_id,item_ids)['item_probs']
                image_list=list(codi_dict['img_url'])
                item_ids=list(codi_dict['item_ids'])
                item_name = list(codi_dict['item_name'])

                sort_by_prob = list()
                for id, url, name, prob in zip(item_ids, image_list, item_name, item_prob):
                    sort_by_prob.append([id, url, name, prob])
                sort_by_prob.sort(key=lambda x:x[3], reverse=True)

                image_list, item_ids, item_name, item_prob = [], [], [], []
                for id, url, name, prob in sort_by_prob:
                    image_list.append(url)
                    item_ids.append(id)
                    item_name.append(name)
                    item_prob.append(prob)
                    

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
                        st.markdown(f"<p style='text-align: center;'>❤️ 가진 옷과 매칭확률 : {int(item_prob[idx]*10000)/100}%</p>", unsafe_allow_html=True)
                    idx+=1

if st.session_state['picked_end']:
    pick_container.empty() # 지금껏 있던 내용들 모두 삭제
    with st.container():
        st.markdown('### 🌟 추천코디')
        
        codi_ids=get_codi(st.session_state['clicked_item'],st.session_state['picked_item'])
        
        codi_dict=get_codi_info(codi_ids)
        
        codi_image_list=list(codi_dict['img_url'])
        result_codi_ids=list(codi_dict['item_ids'])
        codi_style_list = list(codi_dict['item_name'])

        st.image(codi_image_list, caption = codi_style_list, use_column_width=False,width=300)
