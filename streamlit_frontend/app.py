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
    st.session_state['clicked_item'] = item_ids[index] # idκ°  λ€μ΄μ΄
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
st.button('π ',on_click=home, args=())
st.markdown(f"<p style='text-align: center; font-size: 60px'><strong>What's In Your Closet ?</strong></p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><img src='https://user-images.githubusercontent.com/91870042/172792327-8eb0214e-7c3b-4a12-9d26-19223d5c545e.png' width=70% alt='Logo'></p>", unsafe_allow_html=True)  
survey_container=st.empty()
with survey_container.container():
    with st.container():
        
        (_, c, _) = st.columns([1, 9, 1])
      
        item_mid_class = get_item_mid_class()
        with c:
            st.info("λ¨μ± μ·μ λμμΌλ‘ νκ³  μμ΅λλ€. νκ·Έλ₯Ό λ§μ΄ μλ ₯ν μλ‘ λ§μ κ²°κ³Όκ° λμ€λ μ΅λ 3κ°κΉμ§λ§ μλ ₯ν΄μ£ΌμΈμ.")
            input=st.multiselect(label='κ²μνκ³  μΆμ ν€μλλ₯Ό μλ ₯ν΄μ£ΌμΈμ ex)μΉλ§, λ°λ°μ§ κ°μ μ·μ λΆλ₯λ₯Ό μλ ₯νλ©΄ κ²μμ μ ν  μ μμ΄μ',options = item_mid_class,on_change=input_status_change)
        (_, left2, left, right, _) = st.columns([8,1,1,1,8])
        with left2:
            st.button('πͺ λ¦¬μ',on_click=home, args=())
        with left:
            random_button=st.button('π² λλ€')
        with right:
            input_button = st.button('π κ²μ', on_click= search ,args = ([input]), disabled=st.session_state['input_status'])

        
    if len(st.session_state['result'])!=0 or random_button==True:
        st.markdown("""---""")
        if random_button==True:
            search([str(item_mid_class[random.randint(0,len(item_mid_class))])])
        item_dict=get_item_info(st.session_state['result'])  #['result']μλ ν€μλ #list λ°ν
        
        image_list=list(item_dict['img_url'])
        item_ids=list(item_dict['item_ids'])
        item_name = list(item_dict['item_name'])

        page_limit = len(image_list) // 10
        page_limit = max(1,page_limit) # slider maxκ° minμ΄λ λμΌν κ²½μ° μλ¬ λ°μ
        
        is_disable = False
        if page_limit == 1:
            is_disable=True
        
        with st.container():
            st.markdown("### κ°κ³ μλ μ·κ³Ό κ°μ₯ λΉμ·ν μ¬μ§μ κ³¨λΌμ£ΌμΈμ")

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
            

if st.session_state['survey_end']: # λ²νΌμ΄ λλ¦¬λ©΄
    survey_container.empty() # μμ λ΄μ©λ€ μ­μ νκΈ°
    pick_container=st.empty()
    with pick_container.container():
        st.markdown("### κ°μ§κ³  μλ μμ΄ν")
        (_, center, _) = st.columns([1, 1, 1])
        with center:
            st.image(get_image_url(st.session_state['clicked_item']), width=300) # st.session_state['clicked_item'] : id
        
        clicked_cluster_id=cluster_id(st.session_state['clicked_item']) # probλ₯Ό μν λ³μ
        

        codis= get_recommendation(st.session_state['clicked_item'])
        
        clicked_item_info = get_item_info([st.session_state['clicked_item']])
        clicked_big_class = clicked_item_info['big_class'][0]

        st.markdown('### κ΄λ ¨ μ½λλ₯Ό λ³΄κ³ μΆμ μ·μ κ³¨λΌλ³΄μΈμ')
        st.markdown("#### μΆμ² μμ΄ν")
        st.info("β» μ΄λ―Έμ§λ₯Ό ν΄λ¦­νλ©΄ μν νμ΄μ§λ‘, μ²΄ν¬λ°μ€λ₯Ό ν΄λ¦­νλ©΄ μ°κ΄ μ½λ νμ΄μ§λ‘ μ΄λν  μ μμ΅λλ€")
        
        for codi in codis.keys():
            codi_id=codis[codi]

            if clicked_big_class == codi: continue
            if len(codi_id)!=0:
                if codi == 'μμ°ν°': st.markdown(f'#### π§₯ {codi}')
                elif codi == 'μμ': st.markdown(f'#### π {codi}')
                elif codi == 'λ°μ§': st.markdown(f'#### π {codi}')
                elif codi == 'λͺ¨μ': st.markdown(f'#### π§’ {codi}')
                elif codi == 'κ°λ°©': st.markdown(f'#### π {codi}')
                elif codi == 'μ λ°': st.markdown(f'#### π {codi}')
                else: st.markdown(f'#### {codi}')

                codi_dict=get_item_info(codi_id)  

                item_prob= get_prob_info(clicked_cluster_id,item_ids)['item_probs']
                image_list=list(codi_dict['img_url'])
                item_ids=list(codi_dict['item_ids'])
                item_name = list(codi_dict['item_name'])
                item_url = list(codi_dict['item_url'])

                sort_by_prob = list()
                for id, img_url, name, prob, url in zip(item_ids, image_list, item_name, item_prob, item_url):
                    sort_by_prob.append([id, img_url, name, prob, url])
                sort_by_prob.sort(key=lambda x:x[3], reverse=True)

                image_list, item_ids, item_name, item_prob, item_url = [], [], [], [], []
                for id, img_url, name, prob, url in sort_by_prob:
                    image_list.append(img_url)
                    item_ids.append(id)
                    item_name.append(name)
                    item_prob.append(prob)
                    item_url.append(url)
                    

                codi_cnt = len(item_ids)
                idx = 0
                for col_index, col in enumerate(st.columns(5)):
                    if idx >= len(item_ids):
                        break

                    clothes = image_list[idx]

                    with col:
                        st.markdown(f"<p style='text-align: center;'>β€οΈ AI λ§€μΉ­νλ₯  : {int(item_prob[idx]*10000)/100}%</p>", unsafe_allow_html=True)
                        st.markdown(f'[<img src="{image_list[idx]}" width=100%></img>]({item_url[idx]})',
                            unsafe_allow_html=True)

                        checked=st.checkbox(
                            item_name[idx],
                            key = 'clothes-{}'.format(item_ids[idx]), #urlμ΄ keyλ‘ λ€μ΄κ°κ²λ¨
                            on_change = pick_item,
                            args=(idx,item_ids,),
                        )
    
                    idx+=1

if st.session_state['picked_end']:
    pick_container.empty() # μ§κΈκ» μλ λ΄μ©λ€ λͺ¨λ μ­μ 
    with st.container():
        st.markdown('### π μΆμ²μ½λ')
        st.markdown('<p style="color:blue ; font-size: 15px"><strong>β» μ΄λ―Έμ§λ₯Ό ν΄λ¦­νλ©΄ μ½λ νμ΄μ§λ‘ <u>μ΄λ</u>ν  μ μμ΅λλ€</strong></p>',
                     unsafe_allow_html=True)
        
        codi_ids=get_codi(st.session_state['clicked_item'],st.session_state['picked_item'])
        
        codi_dict=get_codi_info(codi_ids)
        
        codi_image_list=list(codi_dict['img_url'])
        result_codi_ids=list(codi_dict['item_ids'])
        codi_style_list = list(codi_dict['item_name'])
        codi_url_list = list(codi_dict['item_url'])
        
        for idx in range(len(codi_image_list)):
            col1, col2, col3 = st.columns(3)
            with col2:
                st.markdown(f'[<img src="{codi_image_list[idx]}" width=100%></img>]({codi_url_list[idx]})',
                            unsafe_allow_html=True)
                st.markdown(f'<p style="text-align: center; font-size: 20px"><strong>{codi_style_list[idx]}</strong></p>',
                            unsafe_allow_html=True)

