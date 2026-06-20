import streamlit as st
from src.ui.base_layout import base_layout_dashbord
from src.components.header import header_dashbord
from src.ui.base_layout import base_layout
from src.components.footer import footer_dashbord
from src.database.db import check_teacher_exist,create_teacher
from src.database.db import teacher_login

def student_screen():
     base_layout_dashbord()
     base_layout()
     teacher_scree_login()
     
def teacher_scree_login():
    
    c1,c2=st.columns(2,gap='xxlarge',vertical_alignment='center')
    with c1:
        header_dashbord()
    with c2:
       if st.button('Go Back To Home',shortcut="control+backspace"): 
        st.session_state['login_type']=None;
        st.rerun() 
    
    st.header("Login using FaceID",text_alignment='center')
    st.space()
    st.camera_input("Position your face in the Center")
    footer_dashbord()