from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

from src.database.config import supabase
from src.pipeline.voice_pipeline import process_bulk_audio
from src.components.attendance_result_dialog import show_attendance_result


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):

    # Initialize session state
    if "voice_attendance_record" not in st.session_state:
        st.session_state.voice_attendance_record = None

    st.write(
        "Record audio of students saying 'I am present'. "
        "The AI will analyze the voices and mark attendance."
    )

    audio_data = st.audio_input("Record classroom audio")

    if st.button(
        "Analyze Audio",
        width="stretch",
        type="primary"
    ):

        if audio_data is None:
            st.warning("Please record audio first.")
            return

        with st.spinner("Processing Audio Data..."):

            enrolled_res = (
                supabase.table("subject_student")
                .select("*, student(*)")
                .eq("subject_id", selected_subject_id)
                .execute()
            )

            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students enrolled in this course.")
                return

            candidates_dict = {
                s["student"]["student_id"]: s["student"]["voice_embedding"]
                for s in enrolled_students
                if s["student"].get("voice_embedding")
            }

            if not candidates_dict:
                st.error(
                    "No enrolled students have registered voice profiles."
                )
                return

            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(
                audio_bytes,
                candidates_dict
            )

            results = []
            attendance_to_log = []

            # Explicit UTC, consistent with the face-attendance write path
            # and with how Supabase's timestamptz column stores values.
            current_timestamp = datetime.now(ZoneInfo("UTC")).strftime(
                "%Y-%m-%dT%H:%M:%S%z"
            )

            for node in enrolled_students:

                student = node["student"]

                score = detected_scores.get(
                    student["student_id"],
                    0.0
                )

                is_present = score > 0

                results.append(
                    {
                        "Name": student["name"],
                        "ID": student["student_id"],
                        "Source": round(score, 4)
                        if is_present
                        else "-",
                        "Status": (
                            "✅ Present"
                            if is_present
                            else "❌ Absent"
                        ),
                    }
                )

                attendance_to_log.append(
                    {
                        "student_id": student["student_id"],
                        "subject_id": selected_subject_id,
                        "timestamp": current_timestamp,
                        "is_present": bool(is_present),
                    }
                )

            st.session_state.voice_attendance_record = (
                pd.DataFrame(results),
                attendance_to_log,
            )

            # IMPORTANT: @st.dialog only allows one dialog open at a time.
            # show_attendance_result() below is ALSO an @st.dialog. Calling
            # it while this voice_attendance_dialog is still considered
            # "open" causes:
            #   StreamlitAPIException: Only one dialog is allowed to be
            #   opened at the same time.
            # We close this dialog's own trigger flag here, right before
            # st.rerun(), so that on the next script run only
            # show_attendance_result() requests to open — not both.
            st.session_state.show_voice_attendance_dialog = False
            st.rerun()

    # Show attendance result after analysis.
    # This branch only matters on the rerun right after the flag above
    # was cleared — at that point voice_attendance_dialog() itself is no
    # longer invoked from teacher_screen.py, so this dialog body never
    # runs again, and show_attendance_result() opens cleanly on its own.
    if st.session_state.get("voice_attendance_record") is not None:
        df_result, logs = st.session_state.voice_attendance_record
        show_attendance_result(df_result, logs)