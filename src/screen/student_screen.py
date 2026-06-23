import streamlit as st
from src.ui.base_layout import base_layout_dashbord
from src.components.header import header_dashbord
from src.ui.base_layout import base_layout
from src.components.footer import footer_dashbord
from src.database.db import check_teacher_exist,create_teacher
from src.database.db import teacher_login
import numpy as np
from PIL import Image
from src.pipeline.face_pipeline import predict_attendance,get_face_embedding,train_classifier
from src.database.db import get_all_students,create_student,get_student_subject,get_student_attendance,unroll_student_to_subject
from src.pipeline.voice_pipeline import get_voice_embedding
from src.components.enroll_dialog import enroll_dialog
from src.components.subjects_cards import subject_card



def student_dashbord():
    base_layout()
    base_layout_dashbord()
    student_data=st.session_state.student_data;
    student_id=student_data['student_id']
    name=student_data["name"].upper()
    c1,c2=st.columns(2,gap='xxlarge',vertical_alignment='center')
    with c1:
        header_dashbord()
    with c2:
       st.subheader(f'WELCOME,{name}',text_alignment='center')
       if st.button('Logout',shortcut="control+backspace"): 
        st.session_state['is_logged_in']=False
        del st.session_state.student_data
        st.rerun() 
         
    st.space()
    c1,c2=st.columns(2)
    with c1:
        st.header("Your Enroll Subjects")
    with c2:
       if st.button("Enroll in subject",type='primary',width='stretch'):
           enroll_dialog()

    st.divider()
    
    with st.spinner("Loading your Subjects...."):
        subjects=get_student_subject(student_id)
        logs=get_student_attendance(student_id)
    
    
    stats_map = {}

    for log in logs:
        
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(
        sid,
        {"total": 0, "attended": 0}
        )
        def enroll_btn():
            if st.button("Unenroll from this Program ",type='tertiary',icon=':material/delete_forever:',width='stretch', key=f"unenroll_{sid}",):
                import time
                
                unroll_student_to_subject(student_id,sid)
                
                st.toast(f"Unenroll form {sub['name']} Successfully !")
                time.sleep(1)
                st.rerun()
                
        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                ("📅", "Total", stats['total']),
                ("✅", "Attended", stats['attended']),
                ],
                footer_callback=enroll_btn
        )
    footer_dashbord()
    
def student_screen():
     base_layout_dashbord()
     base_layout()

     if st.session_state.get("student_data"):
         student_dashbord()
     else:
         teacher_screen_login()
     
def teacher_screen_login():
    
    c1,c2=st.columns(2,gap='xxlarge',vertical_alignment='center')
    with c1:
        header_dashbord()
    with c2:
       if st.button('Go Back To Home',shortcut="control+backspace"): 
        st.session_state['login_type']=None;
        st.rerun() 
    
    st.header("Login using FaceID",text_alignment='center')
    st.space()
    
    show_registration=False
    photo_source=st.camera_input("Position your face in the Center")
    if photo_source:
        img=np.array(Image.open(photo_source))
        with st.spinner("AI is scanning..."):
            detect,all_ids,num_faces=predict_attendance(img)
            if num_faces==0:
                st.warning("Face Not Found !")
            if num_faces>1:
                st.warning("Multiple Faces Found !")
            else:
                if detect:
                    student_id=list(detect.keys())[0]
                    all_student=get_all_students()
                    student=None
                    for s in all_student:
                        if s["student_id"]==student_id:
                            student=s
                            break
                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role="student"
                        st.session_state.student_data=student
                        st.toast(f"Welcome Back {student['name']}")
                        import time 
                        time.sleep(1)
                        st.rerun()
                        
                else:
                    st.info("Fcae Not Recognized ! You might be a new student !")
                    show_registration=True;
                    
    if show_registration:
        with st.container(border=True):
          st.header("Register new profile")
          
          new_name=st.text_input("Enter you name", placeholder="E.g. Ankur Bharti")    
          
          st.subheader("Optionl : Voice Enrollment")
          st.info("Enroll for Voice Attendace")
          
        #   now take the audio data 
          audio_data=None;
          try:
              audio_data=st.audio_input("Record a short Phrase like I am present,My name is Dario")
          except Exception:
              st.error("Audio data Failed !")
              
          if st.button("Create Account",type='primary'):
              if new_name:
                  with st.spinner("Creating Account..."):
                      img=np.array(Image.open(photo_source));
                      embedding=get_face_embedding(img)
                      if embedding:
                          face_emb = list(embedding[0])
                          
                          voice_emb = None
                          if audio_data:
                            voice_emb=get_voice_embedding(audio_data)
                          responce=create_student(new_name,face_emb,voice_emb)
                          if responce:
                                train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role="student"
                                st.session_state.student_data=responce[0]
                                st.toast(f"Profile Creatted,Hi {new_name}")
                                import time 
                                time.sleep(1)
                                st.rerun()
                      else:
                          st.error("Couldno't capture your facial for Registration")        
              else:
                  st.error("Please enter your name !")
          
    footer_dashbord()