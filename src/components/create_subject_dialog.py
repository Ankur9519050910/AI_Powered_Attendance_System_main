import streamlit as st
from src.database.db import create_subject

@st.dialog("Create Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the Details of the Subject")
    name=st.text_input("Subject Name",placeholder='E.g. Introduction to Computer Science')
    code=st.text_input("Subject Code",placeholder="E.g. CS101")
    section=st.text_input("Section",placeholder='E.g. A')
    
    if st.button("Create Subject Now !",type='primary'):
        if name and code and section:
            try:
                create_subject(code, name, section, teacher_id)
                st.toast("Subject Created Successfully !")
                st.rerun()
            except Exception as e:
                st.error(f"Error {str(e)}");
                
        else:
            st.warning("Please fill all the filed !")
    
    
    