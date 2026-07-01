import time
import streamlit as st
from src.database.db import delete_subject, update_subject


@st.dialog("Manage Subject", width="small")
def edit_subject_dialog(subject):
    """
    Dialog for editing or deleting a subject.
    - Edit: lets teacher fix subject name, code, or section
    - Delete: only allowed if zero students are enrolled (safe mode)

    The show_edit_subject_dialog flag is cleared on every explicit
    close action (Save, Delete, or the built-in X button pattern)
    so the dialog doesn't re-open itself on the next rerun.
    """
    subject_id     = subject["subject_id"]
    total_students = subject.get("total_students", 0)

    # Reset tab to "edit" whenever dialog freshly opens
    # (i.e. the flag was just set to True this rerun)
    if st.session_state.get("_edit_dialog_just_opened"):
        st.session_state.edit_subject_tab = "edit"
        st.session_state._edit_dialog_just_opened = False

    if "edit_subject_tab" not in st.session_state:
        st.session_state.edit_subject_tab = "edit"

    # ── Tab toggle 
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "✏️ Edit",
            width="stretch",
            type="primary" if st.session_state.edit_subject_tab == "edit" else "tertiary",
        ):
            st.session_state.edit_subject_tab = "edit"
            st.rerun()
    with c2:
        if st.button(
            "🗑️ Delete",
            width="stretch",
            type="primary" if st.session_state.edit_subject_tab == "delete" else "tertiary",
        ):
            st.session_state.edit_subject_tab = "delete"
            st.rerun()

    st.divider()

    # ── Edit tab 
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

        if total_students > 0:
            st.error(
                f"**Cannot delete this subject.**\n\n"
                f"{total_students} student(s) are currently enrolled. "
                f"All students must unenroll before this subject can be deleted."
            )
        else:
            st.warning(
                f"You are about to permanently delete "
                f"**{subject['name']} ({subject['subject_code']})**.\n\n"
                f"This cannot be undone."
            )

            confirmed = st.checkbox("Yes, I want to permanently delete this subject")

            if st.button(
                "Delete Subject",
                type="primary",
                width="stretch",
                disabled=not confirmed,
            ):
                success, reason = delete_subject(subject_id)
                if success:
                    _close_dialog()
                    st.toast("Subject deleted.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(reason)


def _close_dialog():
    """Reset all dialog-related state so it doesn't re-open on next rerun."""
    st.session_state.show_edit_subject_dialog = False
    st.session_state.edit_subject_target = None
    st.session_state.edit_subject_tab = "edit"
    st.session_state._edit_dialog_just_opened = False