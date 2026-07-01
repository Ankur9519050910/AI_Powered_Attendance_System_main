import streamlit as st
from src.database.db import create_attendance


@st.dialog("Attendance Report")
def show_attendance_result(df, logs):
    st.write("Please review attendance before confirming.")
    st.dataframe(df, hide_index=True, width="stretch")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Discard", width="stretch"):
            _reset_attendance_state()
            st.rerun()

    with col2:
        if st.button(
            "Confirm & Save",
            width="stretch",
            type="primary"
        ):
            try:
                create_attendance(logs)

                st.toast("Attendance taken")
                _reset_attendance_state()

                st.rerun()

            except Exception as e:
                st.error(f"Sync failed! {e}")


def _reset_attendance_state():
    st.session_state.voice_attendance_record = None
    st.session_state.attendance_images = []
    st.session_state.show_add_photo_dialog = False
    st.session_state.show_voice_attendance_dialog = False


def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)