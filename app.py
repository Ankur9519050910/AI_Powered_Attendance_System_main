import streamlit as st

from src.screen.home_screen import home_screen
from src.screen.student_screen import student_screen
from src.screen.teacher_screen import teacher_screen
from src.components.enroll_auto_dialog import auto_enroll_dialog
from src.components.session_manager import restore_session, refresh_session


def main():

    st.set_page_config(
        page_title="SnapClass - Making Attendance faster using AI",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )

    # MUST be called first — before any routing logic.
    # Reads localStorage and restores teacher_data / student_data
    # if the saved session is within the 5-minute TTL window.
    restore_session()

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            # Refresh TTL on every active page render so the
            # 5-min clock resets as long as the teacher is using the app
            refresh_session()
            teacher_screen()

        case 'student':
            refresh_session()
            student_screen()

        case None:
            home_screen()

    join_code = st.query_params.get("join-code")
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)


main()