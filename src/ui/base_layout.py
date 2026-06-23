import streamlit as st

def base_layout_home():
    st.markdown("""
                <style>
                
                /*this will change the backgrouond of the home screen */
                 .stApp{
                     background:#5865F2!important;
                     height: 100vh;
                     overflow: hidden;

                 }
                 
                /*this will change the clolumn size */
                
                 .stApp div[data-testid="stColumn"]{
                       background-color:#E0E3FF !important;
                       padding:2.5rem !important;
                       border-radius:5rem !important;
                 }
                 
     
   
                 
                </style>
    """,unsafe_allow_html=True)
    
    
def base_layout_dashbord():
    st.markdown("""
                <style>
                 .stApp{
                     background:#E0E3FF!important;
                 }
                </style>
    """,unsafe_allow_html=True)
    



def base_layout():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

    /* Main Container */
    .block-container{
        padding-top:1.5rem !important;
        max-width:700px !important;
    }

    /* H1 */
    h1{
        font-family:'Climate Crisis', sans-serif !important;
        font-size:2.5rem !important;
        line-height:0.9 !important;
        margin-bottom:0rem !important;
        color:#E84393 !important;
    }

    /* H2 */
    h2{
        font-family:'Outfit', sans-serif !important;
        font-size:1.8rem !important;
        font-weight:800 !important;
        line-height:1.1 !important;
        color:#5865F2 !important;
    }

    /* H3 */
    h3{
        font-family:'Outfit', sans-serif !important;
        color:#444444 !important;
        font-weight:700 !important;
    }

    /* Paragraph */
    p{
        font-family:'Outfit', sans-serif !important;
    }

    /* Text Input */
    .stTextInput input{
        background:#F5F5F5 !important;
        color:#444 !important;
        border:none !important;
        border-radius:12px !important;
        padding:14px !important;
        font-size:16px !important;
        font-family:'Outfit', sans-serif !important;
    }

    /* Input Container */
    [data-baseweb="input"]{
        border-radius:12px !important;
        overflow:hidden !important;
    }

    /* Labels */
    label{
        font-family:'Outfit', sans-serif !important;
        color:#444 !important;
        font-size:15px !important;
        font-weight:600 !important;
    }

    /* Divider */
    hr{
        border:none !important;
        height:2px !important;
        background:#5865F2 !important;
        margin-top:2rem !important;
        margin-bottom:2rem !important;
    }

    /* Buttons */
    .stButton > button{
        border-radius:25px !important;
        border:none !important;
        background:#E84393 !important;
        color:white !important;
        height:55px !important;
        padding:10px 20px !important;
        font-weight:700 !important;
        font-family:'Outfit', sans-serif !important;
        transition:all 0.25s ease-in-out !important;
    }

    .stButton > button:hover{
        transform:scale(1.03) !important;
    }

    /* Primary Button */
    button[kind="primary"]{
        background:#E84393 !important;
        color:white !important;
    }

    /* Secondary Button */
    button[kind="secondary"]{
        background:#5865F2 !important;
        color:white !important;
    }

    /* Tertiary Button */
    button[kind="tertiary"]{
        background:#222222 !important;
        color:white !important;
    }

    /* Select Box */
    .stSelectbox div[data-baseweb="select"]{
    min-height:55px !important;
    border-radius:12px !important;
    font-family:'Outfit', sans-serif !important;
}

    .stSelectbox div[data-baseweb="select"] > div{
        height:55px !important;
        display:flex !important;
        align-items:center !important;
        border-radius:12px !important;
        background:#F5F5F5 !important;
    }

        .stSelectbox span{
            font-family:'Outfit', sans-serif !important;
            font-size:16px !important;
        }

        .stSelectbox{
            margin-top:0px !important;
        }

    /* Text Area */
    .stTextArea textarea{
        border-radius:12px !important;
        background:#F5F5F5 !important;
        font-family:'Outfit', sans-serif !important;
    }

    /* Number Input */
    .stNumberInput input{
        border-radius:12px !important;
        background:#F5F5F5 !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"]{
        border-radius:16px !important;
    }

    /* Camera Input */
    [data-testid="stCameraInput"]{
        border-radius:16px !important;
    }

    /* Containers */
    [data-testid="stVerticalBlockBorderWrapper"]{
        border-radius:20px !important;
    }

    /* Toast */
    [data-testid="stToast"]{
        border-radius:15px !important;
        font-family:'Outfit', sans-serif !important;
    }

    </style>
    """, unsafe_allow_html=True)