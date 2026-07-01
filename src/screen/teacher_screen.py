import time
from zoneinfo import ZoneInfo

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

from src.ui.base_layout import base_layout_dashbord, base_layout
from src.components.header import header_dashbord
from src.components.footer import footer_dashbord
from src.database.db import (
    check_teacher_exist,
    create_teacher,
    get_teacher_subjects,
    teacher_login,
    get_attendance_for_teacher
)
from src.components.subjects_cards import subject_card
from src.components.share_subject_dialog import share_subject_dialog
from src.components.create_subject_dialog import create_subject_dialog
from src.components.edit_subject_dialog import edit_subject_dialog
from src.components.edit_subject_dialog import delete_subject_dialog
from src.components.add_photo_dialog import add_photos_dialog
from src.database.config import supabase
from src.pipeline.face_pipeline import predict_attendance
from src.components.attendance_result_dialog import attendance_result_dialog

from src.components.voice_dialog import voice_attendance_dialog

IST = ZoneInfo("Asia/Kolkata")

# Entry point


def teacher_screen():
    base_layout_dashbord()
    base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    else:
        if "teacher_login_type" not in st.session_state:
            st.session_state.teacher_login_type = "login"

        if st.session_state.teacher_login_type == "login":
            teacher_screen_login()
        else:
            teacher_screen_register()


# Dashboard


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    name = teacher_data["name"].upper()

    c1, c2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with c1:
        header_dashbord()
    with c2:
        st.subheader(f"WELCOME, {name}", text_alignment="center")
        if st.button("Logout", shortcut="control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, width="stretch", icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button("Manage Subjects", type=type2, width="stretch", icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
        if st.button("Attendance Records", type=type3, width="stretch", icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashbord()


# Tab: Take Attendance


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data.get("teacher_id")

    st.header("Take AI Attendance")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("You have not created any subject yet. Please create one to begin.")
        return

    subject_options = {s["name"]: s["subject_id"] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment="center")
    with col1:
        selected_subject_label = st.selectbox(
            "Select Subject",
            options=list(subject_options.keys()),
            label_visibility="collapsed",
        )
    with col2:
        if st.button("Add Photos", icon=":material/image:", width="stretch"):
            st.session_state.show_add_photo_dialog = True

    # Call the dialog unconditionally based on state — NOT only inside the button's
    # own click branch. @st.dialog needs to be invoked on every rerun while it
    # should stay open, otherwise any st.rerun() fired *inside* the dialog
    # (e.g. switching Camera/Upload tabs) will cause Streamlit to close it,
    # since the dialog function call itself was skipped on that rerun.
    if st.session_state.get("show_add_photo_dialog"):
        add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header("Added Photos")
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width="stretch", caption=f"Photo {idx + 1}")

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "Clear All Photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            disabled=not has_photos,
        ):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/analytics:",
            disabled=not has_photos,
        ):
            with st.spinner("Deep scanning classroom photos..."):
                all_detected_id = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert("RGB"))

                    # predict_attendance returns 4 values — discard best_score
                    # with _ since teacher scan doesn't need it
                    detected, _, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_id.setdefault(student_id, []).append(f"Photo {idx + 1}")

                enrolled_res = (
                    supabase.table("subject_student")
                    .select("*, student(*)")
                    .eq("subject_id", selected_subject_id)
                    .execute()
                )
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course.")
                else:
                    results = []
                    attendance_to_log = []
                    current_timestamp = datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%S%z")

                    for node in enrolled_students:
                        student = node["student"]
                        sources = all_detected_id.get(int(student["student_id"]), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student["name"],
                            "ID": student["student_id"],
                            "Source": ", ".join(sources) if is_present else "—",
                            "Status": "✅ Present" if is_present else "❌ Absent",
                        })

                        attendance_to_log.append({
                            "student_id": student["student_id"],
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present),
                        })

                    st.session_state.show_add_photo_dialog = False
                    st.session_state.show_voice_attendance_dialog = False
                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button(
            "Use Voice Attendance",
            type="primary",
            width="stretch",
            icon=":material/mic:",
        ):
            st.session_state.show_add_photo_dialog = False
            st.session_state.show_voice_attendance_dialog = True

    # Same reasoning as the Add Photos dialog above: call unconditionally
    # based on state so it survives the rerun triggered by "Analyze Audio"
    # inside the dialog, instead of only being callable on the exact
    # rerun where this button was clicked.
    if st.session_state.get("show_voice_attendance_dialog"):
        voice_attendance_dialog(selected_subject_id)


# Tab: Manage Subjects


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects")
    with col2:
        if st.button("Create Subject", width="stretch", type="primary"):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub["total_students"]),
                ("⏰", "Classes", sub["total_classes"]),
            ]

            def make_footer_btns(subject):
                def footer_btns():
                    col_share, col_edit = st.columns(2)

                    with col_share:
                        if st.button(
                            f"Share Code: {subject['name']}",
                            key=f"share_{subject['subject_code']}",
                            icon=":material/share:",
                            width="stretch",
                        ):
                            share_subject_dialog(subject["name"], subject["subject_code"])

                    with col_edit:
                        if st.button(
                            "Edit / Manage",
                            key=f"edit_{subject['subject_code']}",
                            icon=":material/edit:",
                            width="stretch",
                            type="secondary",
                        ):
                            # Store the full subject dict so the dialog
                            # has everything it needs (id, name, code,
                            # section, total_students for safe-delete check)
                            st.session_state.show_edit_subject_dialog = True
                            st.session_state.edit_subject_target = subject

                return footer_btns

            st.space()
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=make_footer_btns(sub),
            )

        # State-based dialog call — same pattern as all other dialogs in this app
        if st.session_state.get("show_edit_subject_dialog"):
            target = st.session_state.get("edit_subject_target", {})
            edit_subject_dialog(target)

    else:
        st.info("No subjects found. Create one above.")


# Tab: Attendance Records


def teacher_tab_attendance_records():
    st.header("Attendance Records")

    teacher_id = st.session_state.teacher_data['teacher_id']
    record = get_attendance_for_teacher(teacher_id)
    # st.write(record)  # DEBUG
    if not record:
        return
    data = []

    for r in record:
        ts = r.get('timestamp')

        display_time = "N/A"
        if ts:
            try:
                parsed = datetime.fromisoformat(ts)
                # Legacy rows written before this fix may lack tz info.
                # Treat those as UTC (matches old behavior) before converting.
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=ZoneInfo("UTC"))
                display_time = parsed.astimezone(IST).strftime("%Y-%m-%d %I:%M %p")
            except ValueError:
                display_time = "N/A"

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": display_time,
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        )
        .reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + "/" +
        summary['Total_Count'].astype(str) + " Students"
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
            [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
    )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


# Auth helpers


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_name or not teacher_username or not teacher_pass:
        return False, "All fields are required."

    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords don't match."

    if check_teacher_exist(teacher_username):
        return False, "Username already taken!"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Teacher registered successfully."
    except Exception as e:
        print(e)
        return False, f"Unexpected error: {e}"


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.teacher_data = teacher
        st.session_state.user_role = "teacher"
        st.session_state.is_logged_in = True
        return True

    return False


# Login screen


def teacher_screen_login():
    c1, c2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with c1:
        header_dashbord()
    with c2:
        if st.button("Go Back To Home", shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login with Password", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder="Enter your username")
    teacher_pass = st.text_input("Enter Password", type="password", placeholder="Enter your password")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login", type="primary", width="stretch", icon=":material/passkey:"):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="❤️")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with c2:
        if st.button("Register", type="secondary", width="stretch", icon=":material/passkey:"):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashbord()


# Registration screen


def teacher_screen_register():
    c1, c2 = st.columns(2, gap="xxlarge", vertical_alignment="center")
    with c1:
        header_dashbord()
    with c2:
        if st.button("Go Back To Home", shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Register Your Teacher Profile", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder="Enter your username")
    teacher_name = st.text_input("Enter teacher name", placeholder="Enter teacher name")
    teacher_pass = st.text_input("Enter Password", type="password", placeholder="Enter your password")
    teacher_pass_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Register Now", type="primary", width="stretch", icon=":material/passkey:"):
            success, message = register_teacher(
                teacher_username, teacher_name, teacher_pass, teacher_pass_confirm
            )
            if success:
                st.success(message)
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with c2:
        if st.button("Login Instead", type="secondary", width="stretch", icon=":material/passkey:"):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashbord()