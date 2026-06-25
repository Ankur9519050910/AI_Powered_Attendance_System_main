import streamlit as st
from PIL import Image


@st.dialog("Capture Or Upload Photos")
def add_photos_dialog():

    st.write("Add classroom photos to scan for attendance")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(2)

    with t1:
        type_camera = (
            "primary"
            if st.session_state.photo_tab == "camera"
            else "tertiary"
        )
        if st.button("Camera", type=type_camera, width="stretch"):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with t2:
        type_upload = (
            "primary"
            if st.session_state.photo_tab == "upload"
            else "tertiary"
        )
        if st.button("Upload Photos", type=type_upload, width="stretch"):
            st.session_state.photo_tab = "upload"
            st.rerun()

    # CAMERA TAB
    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input("Take Snapshot", key="dialog_cam")

        if cam_photo is not None:
            st.image(cam_photo, width="stretch")

            if st.button("Add Photo", type="primary", width="stretch"):
                st.session_state.attendance_images.append(Image.open(cam_photo))
                st.toast("Photo captured!")
                st.rerun()

    # UPLOAD TAB
    elif st.session_state.photo_tab == "upload":

        upload_files = st.file_uploader(
            "Choose Image Files",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload",
        )

        if upload_files:
            if st.button("Add Uploaded Photos", type="primary", width="stretch"):
                for f in upload_files:
                    st.session_state.attendance_images.append(Image.open(f))
                st.toast(f"{len(upload_files)} photo(s) added!")
                st.rerun()

    st.divider()

    st.write(f"Photos Added: {len(st.session_state.attendance_images)}")

    # This must match the flag checked in teacher_tab_take_attendance(),
    # otherwise closing here won't actually prevent the dialog from
    # being re-invoked on the next rerun.
    if st.button("Done", type="primary", width="stretch"):
        st.session_state.show_add_photo_dialog = False
        st.rerun()