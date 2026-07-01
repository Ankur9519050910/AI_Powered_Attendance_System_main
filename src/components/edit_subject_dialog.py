import time
import streamlit as st
from src.database.db import delete_subject, update_subject


@st.dialog("Manage Subject", width="small")
def edit_subject_dialog(subject):
    st.session_state.show_edit_subject_dialog = False

    subject_id     = subject["subject_id"]
    total_students = subject.get("total_students", 0)
    total_classes  = subject.get("total_classes", 0)

    if "edit_subject_tab" not in st.session_state:
        st.session_state.edit_subject_tab = "edit"

    # ── Tab toggle ──────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "✏️ Edit",
            width="stretch",
            type="primary" if st.session_state.edit_subject_tab == "edit" else "tertiary",
        ):
            st.session_state.edit_subject_tab = "edit"
            st.session_state.show_edit_subject_dialog = True
            st.rerun()
    with c2:
        if st.button(
            "🗑️ Delete",
            width="stretch",
            type="primary" if st.session_state.edit_subject_tab == "delete" else "tertiary",
        ):
            st.session_state.edit_subject_tab = "delete"
            st.session_state.show_edit_subject_dialog = True
            st.rerun()

    st.divider()

    # ── Edit tab ─────────────────────────────────────────────────
    if st.session_state.edit_subject_tab == "edit":
        st.write("Update the subject details below.")

        new_name = st.text_input(
            "Subject Name",
            value=subject["name"],
            placeholder="E.g. Introduction to Computer Science",
        )
        new_code = st.text_input(
            "Subject Code",
            value=subject["subject_code"],
            placeholder="E.g. CS101",
        )
        new_section = st.text_input(
            "Section",
            value=subject["section"],
            placeholder="E.g. A",
        )

        if st.button("Save Changes", type="primary", width="stretch"):
            if not new_name or not new_code or not new_section:
                st.warning("All fields are required.")
            else:
                success = update_subject(
                    subject_id,
                    new_name,
                    new_code.strip().upper(),
                    new_section,
                )
                if success:
                    _close_dialog()
                    st.toast("Subject updated successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Update failed. Please try again.")

    # ── Delete tab ───────────────────────────────────────────────
    elif st.session_state.edit_subject_tab == "delete":

        # Show what will be wiped so teacher knows what they're doing
        st.warning(
            f"Permanently delete **{subject['name']} ({subject['subject_code']})**?\n\n"
            f"This will also delete:\n"
            f"- **{total_students}** enrolled student(s)\n"
            f"- **{total_classes}** class session(s) and all attendance records\n\n"
            f"**This cannot be undone.**"
        )

        confirmed = st.checkbox(
            "Yes, delete this subject and all its data",
            key=f"confirm_delete_{subject_id}",
        )

        if confirmed:
            st.session_state.show_edit_subject_dialog = True

        if st.button(
            "Delete Subject",
            type="primary",
            width="stretch",
            disabled=not confirmed,
        ):
            success, reason = delete_subject(subject_id)
            if success:
                _close_dialog()
                st.session_state.pop(f"confirm_delete_{subject_id}", None)
                st.toast("Subject deleted.")
                time.sleep(1)
                st.rerun()
            else:
                st.error(reason)
                st.session_state.show_edit_subject_dialog = True


def _close_dialog():
    st.session_state.show_edit_subject_dialog = False
    st.session_state.edit_subject_target = None
    st.session_state.edit_subject_tab = "edit"