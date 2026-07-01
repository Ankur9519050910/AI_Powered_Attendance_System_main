import time

import streamlit as st
import numpy as np
from PIL import Image

from src.ui.base_layout import base_layout_dashbord, base_layout
from src.components.header import header_dashbord
from src.components.footer import footer_dashbord
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subject,
    get_student_attendance,
    unroll_student_to_subject,
)
from src.pipeline.face_pipeline import predict_attendance, get_face_embedding, train_classifier
from src.pipeline.voice_pipeline import get_voice_embedding
from src.components.enroll_dialog import enroll_dialog
from src.components.subjects_cards import subject_card
from src.components.session_manager import save_session,clear_session
from src.components.unenroll_dialog import unenroll_dialog
  
# Dashboard (shown after login)
  

def student_dashboard():
    base_layout()
    base_layout_dashbord()

    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    name = student_data["name"].upper()

    c1, c2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with c1:
        header_dashbord()
    with c2:
        st.subheader(f"WELCOME, {name}", text_alignment="center")
        if st.button("Logout", shortcut="control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            clear_session() 
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll in Subject", type="primary", width="stretch"):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading your Subjects..."):
        subjects = get_student_subject(student_id)
        logs = get_student_attendance(student_id)

    # Build attendance stats per subject
    stats_map = {}
    for log in logs:
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sid = sub["subject_id"]
        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def make_unenroll_btn(subject_id, subject_name, subject_code):
            def enroll_btn():
                if st.button(
                    "Unenroll from this Program",
                    type="tertiary",
                    icon=":material/delete_forever:",
                    width="stretch",
                    key=f"unenroll_{subject_id}",
                ):
                    st.session_state.show_unenroll_dialog = True
                    st.session_state.unenroll_target = {
                        "subject_id": subject_id,
                        "subject_name": subject_name,
                        "subject_code": subject_code,
                    }
            return enroll_btn

        with cols[i % 2]:
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    ("📅", "Total", stats["total"]),
                    ("✅", "Attended", stats["attended"]),
                ],
                footer_callback=make_unenroll_btn(sid, sub["name"], sub["subject_code"]),
            )
    if st.session_state.get("show_unenroll_dialog"):
        target = st.session_state.get("unenroll_target", {})
        unenroll_dialog(
            student_id=student_id,
            subject_id=target["subject_id"],
            subject_name=target["subject_name"],
            subject_code=target["subject_code"],
        )
    footer_dashbord()


  
# Login screen
  

def student_login_screen():
    base_layout_dashbord()
    base_layout()

    c1, c2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with c1:
        header_dashbord()
    with c2:
        if st.button("Go Back To Home", shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using Face ID", text_alignment="center")
    st.space()

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):
            detect, all_ids, num_faces, best_score = predict_attendance(img)

        if num_faces == 0:
            st.warning("No face found. Please try again.")
            st.session_state.show_registration = False

        elif num_faces > 1:
            st.warning("Multiple faces detected. Please ensure only one face is visible.")
            st.session_state.show_registration = False

        else:
            if detect:
                # Use a tighter threshold for login than for general detection.
                # This prevents a borderline match from logging in the wrong person.
                if best_score > 0.45:
                    st.warning(
                        "Face detected but confidence is low. "
                        "Please try better lighting or move closer."
                    )
                    st.session_state.show_registration = False

                else:
                    # High confidence match — log the student in
                    student_id = list(detect.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if int(s["student_id"]) == student_id),
                        None
                    )

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.session_state.show_registration = False
                        st.toast(f"Welcome back, {student['name']}!")
                        time.sleep(1)
                        save_session()
                        st.rerun()
                    else:
                        st.error("Student record not found. Please contact support.")

            elif best_score <= 0.5:
                # Score is low meaning face is close to someone we know
                # but just missed the threshold — bad lighting or angle.
                # Block registration to prevent duplicate accounts.
                st.warning(
                    "Your face looks familiar but couldn't be confirmed. "
                    "Try better lighting or move closer to the camera."
                )
                st.session_state.show_registration = False

            else:
                # Score is high meaning face looks nothing like anyone we know.
                # This is genuinely a new student.
                st.info("Face not recognized. You might be a new student — please register below.")
                st.session_state.show_registration = True

      
    # Registration form
      

    if st.session_state.show_registration:
        with st.container(border=True):
            st.header("Register New Profile")

            new_name = st.text_input("Enter your name", placeholder="E.g. Ankur Bharti")

            st.subheader("Optional: Voice Enrollment")
            st.info("Enroll for Voice Attendance")

            audio_data = None
            try:
                audio_data = st.audio_input(
                    "Record a short phrase like 'I am present' or 'My name is ...'"
                )
            except Exception:
                st.error("Audio input failed. Continuing without voice enrollment.")

            if st.button("Create Account", type="primary"):
                if not new_name:
                    st.error("Please enter your name!")
                else:
                    with st.spinner("Creating account..."):
                        img = np.array(Image.open(photo_source))
                        embedding = get_face_embedding(img)

                        if embedding:
                            face_emb = list(embedding[0])
                            voice_emb = get_voice_embedding(audio_data) if audio_data else None

                            response = create_student(new_name, face_emb, voice_emb)

                            if response:
                                # Train the classifier with the new student included
                                train_classifier()

                                # IMPORTANT: use response[0] directly from the DB
                                new_student = response[0]

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = new_student
                                st.session_state.show_registration = False
                                st.toast(f"Profile created! Hi, {new_name}!")
                                save_session()
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Account creation failed. Please try again.")
                        else:
                            st.error(
                                "Couldn't capture your face for registration. "
                                "Please retake the photo."
                            )

    footer_dashbord()


  
# Entry point
  

def student_screen():
    if st.session_state.get("student_data"):
        student_dashboard()
    else:
        student_login_screen()