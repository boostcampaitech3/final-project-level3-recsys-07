from logging import PlaceHolder
import streamlit as st
from utils import paginator
from st_clickable_images import clickable_images

st.image('https://www.noiremag.com/wp-content/uploads/2020/08/2020-fashion-trends-feature-696x392-1.jpg')
st.title('YUSINSA')

with st.container():
    c1_col1,c1_col2 = st.columns(2)

    with c1_col1:
        input=st.text_input(label='👕👖',placeholder='갖고있는 옷을 검색하세요')
    with c1_col2:
        st.write("")
        st.write("")
        input_button=st.button('🔍')

st.markdown("""---""")
image_list=['https://image.msscdn.net/images/style/detail/26833/detail_26833_2_500.jpg' for i in range(8)]
print(image_list)
with st.container():
    st.markdown("### 갖고있는 옷과 가장 비슷한 사진을 골라주세요")
    image_iterator = paginator('',image_list,items_per_page=5,on_sidebar=False)
    indices_on_page, images_on_page = map(list, zip(*image_iterator))
    my_cloth= clickable_images(images_on_page,titles=[f"Image #{str(i)}" for i in range(5)],
                                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                img_style={"margin": "5px", "height": "200px", "width" : "125px"},key='mySelect'
                            )
    st.write(my_cloth) # 아무것도 선택하지 않았을 때 : -1
    st.write(indices_on_page[my_cloth])

    st.button('선택')

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
            


