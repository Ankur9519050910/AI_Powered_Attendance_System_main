import time
import streamlit as st
from src.database.db import unroll_student_to_subject


@st.dialog("Unenroll from Subject")
def unenroll_dialog(student_id, subject_id, subject_name, subject_code):
    # Clear flag at top — same pattern as edit_subject_dialog
    # so X-button close works correctly
    st.session_state.show_unenroll_dialog = False

    st.warning(
        f"You are about to unenroll from **{subject_name} ({subject_code})**.\n\n"
        f"You will lose access to this subject and your attendance history "
        f"for it will no longer be visible."
    )

    confirmed = st.checkbox(
        "Yes, I want to unenroll from this subject",
        key=f"confirm_unenroll_{subject_id}",
    )

    if confirmed:
        st.session_state.show_unenroll_dialog = True

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", width="stretch", type="tertiary"):
            _close_dialog(subject_id)
            st.rerun()

    with col2:
        if st.button(
            "Unenroll",
            width="stretch",
            type="primary",
            disabled=not confirmed,
        ):
            unroll_student_to_subject(student_id, subject_id)
            _close_dialog(subject_id)
            st.toast(f"Unenrolled from {subject_name} successfully!")
            time.sleep(1)
            st.rerun()


def _close_dialog(subject_id=None):
    st.session_state.show_unenroll_dialog = False
    st.session_state.unenroll_target = None
    if subject_id:
        st.session_state.pop(f"confirm_unenroll_{subject_id}", None)