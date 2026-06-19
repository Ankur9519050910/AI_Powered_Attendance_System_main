import streamlit as st

def footer_home():
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"

    st.markdown(f"""
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            gap:8px;
            margin-top:1rem;
        ">
            <span>Created by ❤️</span>
            <img src="{logo_url}" style="height:30px;">
        </div>
    """, unsafe_allow_html=True)