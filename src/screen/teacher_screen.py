import streamlit as st
from src.ui.base_layout import base_layout_dashbord
from src.components.header import header_dashbord
from src.ui.base_layout import base_layout
from src.components.footer import footer_dashbord
from src.database.db import check_teacher_exist,create_teacher,get_teacher_subjects
from src.database.db import teacher_login
from src.components.subjects_cards import subject_card
from src.components.share_subject_dialog import share_subject_dialog
from src.components.create_subject_dialog import create_subject_dialog
from src.components.add_photo_dialog import add_photos_dialog
from src.database.config import supabase
import numpy as np
from src.pipeline.face_pipeline import predict_attendance
from datetime import datetime
import pandas as pd
from src.components.attendance_result_dialog import attendance_result_dialog



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
    base_layout()
    base_layout_dashbord()
    teacher_data=st.session_state.teacher_data;
    name=teacher_data["name"].upper()
    c1,c2=st.columns(2,gap='xxlarge',vertical_alignment='center')
    with c1:
        header_dashbord()
    with c2:
       st.subheader(f'WELCOME,{name}',text_alignment='center')
       if st.button('Logout',shortcut="control+backspace"): 
        st.session_state['is_logged_in']=False
        del st.session_state.teacher_data
        st.rerun() 
         
    st.space()
    # st.space()
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab='take_attendance'
        
    
    tab1,tab2,tab3=st.columns(3)
    with tab1:
      type1="primary" if st.session_state.current_teacher_tab=='take_attendance' else "tertiary"
      if  st.button("Take Attendance",type=type1,width='stretch',icon=":material/ar_on_you:"):
          st.session_state.current_teacher_tab='take_attendance'
          st.rerun()
          
    with tab2:
      type2="primary" if st.session_state.current_teacher_tab=='manage_subjects' else "tertiary"
      if  st.button("Manage Subjects",type=type2,width='stretch',icon=":material/book_ribbon:"):
          st.session_state.current_teacher_tab='manage_subjects'
          st.rerun()
          
    with tab3:
      type3="primary" if st.session_state.current_teacher_tab=='attendance_records' else "tertiary"

      if  st.button("Attendance Records",type=type3,width='stretch',icon=":material/cards_stack:"):
          st.session_state.current_teacher_tab='attendance_records'
          st.rerun()
          
    st.divider()
    if st.session_state.current_teacher_tab=='take_attendance':
        teacher_tab_take_attendace();   
    if st.session_state.current_teacher_tab=='manage_subjects':
        teacher_tab_manage_subjects();   
    if st.session_state.current_teacher_tab=='attendance_records':
        teacher_tab_attendace_records();   
       
    footer_dashbord() 

def teacher_tab_take_attendace():
    teacher_id=st.session_state.teacher_data.get("teacher_id")
    
    st.header("Take AI Attendance")
    
    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []
    subject=get_teacher_subjects(teacher_id)
    
    if not subject:
        st.warning("You have not created any subject yet ! Please create one To begin ")
        return
    subject_options={f"{s['name']}": s['subject_id'] for s in subject}
    
    col1,col2=st.columns([3,1],vertical_alignment='center')
    with col1:
        selected_subject_label=st.selectbox("Select Photos",options=list(subject_options.keys()),label_visibility="collapsed")
        
    with col2:
       if  st.button('Add Photos',icon=":material/image:",width='stretch'):
           add_photos_dialog()
    
    
    selected_subject_id=subject_options[selected_subject_label]
    
    st.divider()   
    
    
    
    if st.session_state.attendance_images:
        st.header("Added Photos")

        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(
                    img,
                    width="stretch",
                    caption=f"Photo {idx + 1}"
                )
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "Clear all photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",disabled=not has_photos
        ):
            st.session_state.attendance_images = []
            st.rerun()
            
    with c2:
        

        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/analytics:",disabled=not has_photos
        ):
            with st.spinner("Deep scanning classroom photos..."):
                all_detected_id = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert("RGB"))

                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_id.setdefault(
                                student_id, []
                            ).append(f"Photo {idx + 1}")

                enrolled_res = supabase.table("subject_student").select("*, student(*)").eq("subject_id",selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course")
                    
                else:

                    results, attendance_to_log = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node["student"]

                        sources = all_detected_id.get(
                            int(student["student_id"]), []
                        )

                        is_present = len(sources) > 0

                        results.append({
                            "Name": student["name"],
                            "ID": student["student_id"],
                            "Source": ", ".join(sources) if is_present else "—",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            "student_id": student["student_id"],
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present)
                        })   
                attendance_result_dialog(pd.DataFrame(results),attendance_to_log)                   
    with c3:
        if st.button(
            "Use Voice Attendance",
            type="primary",
            width="stretch",
            icon=":material/mic:"
        ):
        #  voice_attendance_dialog()     
         pass          
                   
                  
            
            
    
def  teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    col1,col2=st.columns(2)
    with col1:
        st.header("Manage Subjects")
    with col2:
       if st.button("Create Subjects",width='stretch',type='primary'):
           create_subject_dialog(teacher_id)
    
    
    
    # now list all the subject 
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                ("👥","Students",sub['total_students']),
                ("⏰","Classes",sub['total_classes']),
            ]
            def share_btn():
                if st.button(f"Share Code: {sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:",width='stretch'):
                    share_subject_dialog(sub['name'],sub['subject_code'])
                    
            st.space()
            
            
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    
    else:
        st.info("NO SUBJECT FOUND,CREATE ONE ABOVE")
        
        
def   teacher_tab_attendace_records():
    st.header("Attendace Rerords ")
    
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
                st.toast("Welcome back !",icon="❤️")
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
    