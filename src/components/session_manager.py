# i want to login the student and teacher for 5 mins after login 
# which remove the login login logic for 5 mins 
"""
session_manager.py
Persists login state across page reloads using browser localStorage.

How it works:
- On every page load, call restore_session() FIRST (before routing logic).
  It injects a tiny JS snippet that reads localStorage and sends the saved
  login data back to Streamlit via st.query_params.
- On every successful login, call save_session() to write the current
  session state into localStorage with a 5-minute expiry timestamp.
- On logout, call clear_session() to wipe localStorage.

TTL: 5 minutes (300,000 ms). After that the data is ignored and the user
must log in again — this matches your requirement exactly.
"""

import json
import streamlit as st
import streamlit.components.v1 as components

SESSION_KEY = "snapclass_session"
TTL_MS = 5 * 60 * 1000  # 5 minutes in milliseconds


def save_session():
    """
    Call this right after a successful login (teacher or student).
    Writes login_type + role-specific data into localStorage with a
    5-minute expiry timestamp.
    """
    login_type = st.session_state.get("login_type")

    if login_type == "teacher":
        payload = {
            "login_type": "teacher",
            "teacher_data": st.session_state.get("teacher_data"),
            "user_role": "teacher",
            "is_logged_in": True,
            "expires_at": None,  # filled by JS using Date.now() + TTL
        }
    elif login_type == "student":
        payload = {
            "login_type": "student",
            "student_data": st.session_state.get("student_data"),
            "user_role": "student",
            "is_logged_in": True,
            "expires_at": None,
        }
    else:
        return

    payload_json = json.dumps(payload)

    components.html(
        f"""
        <script>
        (function() {{
            var payload = {payload_json};
            payload.expires_at = Date.now() + {TTL_MS};
            localStorage.setItem('{SESSION_KEY}', JSON.stringify(payload));
        }})();
        </script>
        """,
        height=0,
    )


def restore_session():
    """
    Call this at the very top of app.py, before any routing logic.
    Reads localStorage and restores session state if the saved data
    is still within the 5-minute TTL window.

    Uses query_params as a one-way bridge: JS writes the saved data
    into the URL as a query param, Streamlit reads it, restores state,
    then immediately clears the param to keep the URL clean.
    """
    # Step 2: if JS already sent us the saved session via query_params, consume it
    raw = st.query_params.get("_session_restore")
    if raw:
        try:
            payload = json.loads(raw)
            expires_at = payload.get("expires_at", 0)

            # Check TTL — only restore if not expired
            # We compare against a JS timestamp (ms since epoch).
            # Python time.time() * 1000 gives the same unit.
            import time
            now_ms = time.time() * 1000

            if now_ms < expires_at:
                login_type = payload.get("login_type")
                st.session_state["login_type"] = login_type
                st.session_state["is_logged_in"] = True
                st.session_state["user_role"] = payload.get("user_role")

                if login_type == "teacher" and payload.get("teacher_data"):
                    st.session_state["teacher_data"] = payload["teacher_data"]

                elif login_type == "student" and payload.get("student_data"):
                    st.session_state["student_data"] = payload["student_data"]

        except (json.JSONDecodeError, KeyError):
            pass  # corrupted data — just ignore and let user log in normally

        # Always clear the query param regardless of success/failure
        st.query_params.pop("_session_restore", None)
        return  # session restored, no need to inject JS

    # Step 1: inject JS to read localStorage and redirect back with the data
    # Only do this if we're not already logged in
    if not st.session_state.get("is_logged_in"):
        components.html(
            f"""
            <script>
            (function() {{
                var raw = localStorage.getItem('{SESSION_KEY}');
                if (!raw) return;

                var payload;
                try {{ payload = JSON.parse(raw); }} catch(e) {{ return; }}

                // Check TTL client-side too (belt-and-suspenders)
                if (!payload.expires_at || Date.now() > payload.expires_at) {{
                    localStorage.removeItem('{SESSION_KEY}');
                    return;
                }}

                // Send the payload back to Streamlit via query param
                var encoded = encodeURIComponent(JSON.stringify(payload));
                var url = window.location.pathname + '?_session_restore=' + encoded;
                window.location.replace(url);
            }})();
            </script>
            """,
            height=0,
        )


def clear_session():
    """Call this on logout to wipe the saved session from localStorage."""
    components.html(
        f"""
        <script>
        localStorage.removeItem('{SESSION_KEY}');
        </script>
        """,
        height=0,
    )


def refresh_session():
    """
    Call this periodically (e.g. on any button click while logged in)
    to reset the 5-minute TTL so active users don't get logged out
    while they're actually using the app.
    """
    save_session()