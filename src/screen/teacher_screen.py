import streamlit as st
from src.ui.base_layout import base_layout_dashbord
from src.components.header import header_dashbord
from src.ui.base_layout import base_layout
from src.components.footer import footer_dashbord
from src.database.db import check_teacher_exist,create_teacher
from src.database.db import teacher_login

def teacher_screen():
    base_layout_dashbord()
    base_layout()
    
    if "teacher_data" in st.session_state:
     teacher_dashbord()
    
    else:
        if 'teacher_login_type' not in st.session_state:
            st.session_state.teacher_login_type = 'login'

        if st.session_state.teacher_login_type == 'login':
            teacher_scree_login()
        else:
            teacher_screen_regi()
        
        
def teacher_dashbord():
    teacher_data=st.session_state.teacher_data;
    st.header(f"""Welcome , {teacher_data["name"]}""")
         
         
         
def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):

      if not teacher_name or not teacher_username or not teacher_pass:
          return False,"All Fields required"

      if teacher_pass != teacher_pass_confirm:
          return False,"Password doesn't match"

      if check_teacher_exist(teacher_username):
          return False,"Username already taken!"

      try:
          create_teacher(
              teacher_username,
              teacher_pass,
              teacher_name
          )

          return True, "Teacher registered successfully"

      except Exception as e:
          print(e)
          return False, f"Unexpected Error: {e}"
      
      
def login_teacher(username,password):
    if not username or not password:
        return False;
    teacher=teacher_login(username,password);
    if teacher:
        st.session_state.teacher_data=teacher
        st.session_state.user_role="teacher"
        st.session_state.is_logged_in=True
        return True;
    else :
        return False;
      
      
               
def teacher_scree_login():
    
    c1,c2=st.columns(2,gap='xxlarge',vertical_alignment='center')
    with c1:
        header_dashbord()
    with c2:
       if st.button('Go Back To Home',shortcut="control+backspace"): 
        st.session_state['login_type']=None;
        st.rerun() 
    
    st.header("Login with passwrod",text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Entet username",placeholder="Enter your username")
    teacher_pass=st.text_input("Enter Password",type='password',placeholder="Enter your passwrod")
    st.divider()
    c1,c2=st.columns(2)
    with c1:
        if st.button('Login',type="primary",width='stretch',icon=":material/passkey:"):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("Welcome back !",icon="🙏")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username/password Combo !")
    with c2:
      if  st.button('Register',type='secondary',width='stretch',icon=":material/passkey:"):
          st.session_state.teacher_login_type='register'
          st.rerun()
          
    footer_dashbord()
    
    
def teacher_screen_regi():
    c1,c2=st.columns(2,gap='xxlarge',vertical_alignment='center')
    with c1:
        header_dashbord()
    with c2:
       if st.button('Go Back To Home',shortcut="control+backspace"): 
        st.session_state['login_type']=None
        st.rerun() 
    
    st.header("Register Your Teacher Profile",text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Entet username",placeholder="Enter your username")
    teacher_name=st.text_input("Enter teacher name",placeholder="Enter teacher name")
    teacher_pass=st.text_input("Enter Password",type='password',placeholder="Enter your password")
    teacher_pass_confirm=st.text_input("Confirm password",type='password',placeholder="Confirm your password")
    st.divider()
    c1,c2=st.columns(2)
    with c1:
       if st.button('Register Now',type="primary",width='stretch',icon=":material/passkey:"):
           success,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
           if success:
               st.success(message)
               import time 
               time.sleep(2)
               st.session_state.teacher_login_type="login";
               st.rerun()
           else:
               st.error(message)
    with c2:
       if st.button('Login Instead',type='secondary',width='stretch',icon=":material/passkey:"):
           st.session_state.teacher_login_type='login'
           st.rerun()
    footer_dashbord()
    