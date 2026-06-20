import streamlit as st

def footer_home():
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"

    st.markdown(f"""
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            gap:8px;
            font-weight:900;
            margin-top:2rem;
        ">
            <span>Created by ❤️ and ....</span>
            
        </div>
    """, unsafe_allow_html=True)
    
def footer_dashbord():
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"

    st.markdown(f"""
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            gap:8px;
            margin-top:1rem;
            font-weight:900;
        ">
            <span style="color:black;font-weight:bold;">Created by ❤️ and ....</span>
            
        </div>
    """, unsafe_allow_html=True)