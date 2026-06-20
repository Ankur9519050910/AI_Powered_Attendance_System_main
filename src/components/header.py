import streamlit as st
from src.ui.base_layout import base_layout
def header():
    base_layout()
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <div style="
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            margin-top:30px;
            margin-buttom:10px;
        ">
            <img src="{logo_url}" style="height:100px;">
            <h1 style="text-align:center;color:#E0E3FF">SNAP<br>CLASS</h1>
        </div>
    """, unsafe_allow_html=True)
    
    
def header_dashbord():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            margin-buttom:10px;
            gap:30px;
        ">
            <img src="{logo_url}" style="height:85px;">
            <h2 style="text-align:left;color:#5865F2">SNAP<br>CLASS</h2>
        </div>
    """, unsafe_allow_html=True)