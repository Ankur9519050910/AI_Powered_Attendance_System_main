import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject

@st.dialog("Enroll In Subject")
def enroll_dialog():

    st.write("Enter the Subject code provided by your Teacher to enroll")

    join_code = st.text_input(
        "Enter code",
        placeholder="Eg. CS101"
    )

    if st.button("Enroll Now", width='stretch', type='primary'):

        if not join_code:
            st.warning("Please enter a valid subject code!")
            return

        join_code = join_code.strip().upper()

        try:
            # Find subject
            res = (
                supabase.table("subjects")
                .select("subject_id,name,subject_code")
                .eq("subject_code", join_code)
                .execute()
            )

            if not res.data:
                st.error("Subject not found!")
                return

            subject = res.data[0]
            student_id = st.session_state.student_data["student_id"]

            # Check if already enrolled
            check = (
                supabase.table("subject_student")
                .select("*")
                .eq("student_id", student_id)
                .eq("subject_id", subject["subject_id"])
                .execute()
            )

            if len(check.data) > 0:
                st.warning(
                    f"You are already enrolled in {subject['name']}"
                )
                return

            # Enroll student
            enroll_student_to_subject(
                student_id,
                subject["subject_id"]
            )
            import time 

            st.success(
                f"Successfully enrolled in {subject['name']} 🎉"
            )
            time.sleep(2)

            st.rerun()

        except Exception as e:
            st.error(f"Error: {str(e)}")