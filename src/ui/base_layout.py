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
                
               
               #MainMenu,header,footer{
                     visibility:hidden;
                }
                
                
                .block-container{
                     padding-top:1.5rem !important;
                }
                
                h1{
                    font-family:'Climate Crisis', sans-serif !important;
                    font-size:2.5rem !important;
                    line-height:0.9 !important;
                    margin-bottom:0rem !important;
                    color:#E0E3FF !important;
                   
                }
                
                h2{
                    font-family:'Climate Crisis', sans-serif !important;
                    font-size:1.8rem !important;
                    line-height:0.9 !important;
                    margin-bottom:0rem !important;
                    color:#5865F2!important;
                }
                
                
                
                button{
                      border-radius:1.5rem !important;
                      background:#EB459E !important;
                      padding:10px 20px !important;
                      color:white !important;
                      borde:none important;
                      transition:all 0.25s ease-in-out !important;
                }
                
                button[kind='secondary']{
                      border-radius:1.5rem !important;
                      background:blue !important;
                      padding:10px 20px !important;
                      color:white !important;
                      borde:none important;
                      transition:all 0.25s ease-in-out !important;
                }
                
                button[kind='tertiary']{
                      border-radius:1.5rem !important;
                      background:black !important;
                      padding:10px 20px !important;
                      color:white !important;
                      borde:none important;
                      transition:all 0.25s ease-in-out !important;
                }
                
                button:hover{
                     transform:scale(1.05) !important;
                }
                

/* Input Box */
.stTextInput input{
    background:#F5F5F5 !important;
    color:#444 !important;
    border:none !important;
    border-radius:12px !important;
    padding:14px !important;
    font-size:16px !important;
    box-shadow:none !important;
    
}

/* Input Container */
[data-baseweb="input"]{
    border-radius:12px !important;
    overflow:hidden !important;
}

/* Labels */
.stTextInput label{
    color:#444 !important;
    font-size:15px !important;
    font-weight:500 !important;
}

/* Divider */
hr{
    margin-top:2rem !important;
    margin-bottom:2rem !important;
}

/* Primary Button */
button[kind="primary"]{
    background:#E63E9E !important;
    color:white !important;
    border:none !important;
    border-radius:25px !important;
    height:55px !important;
    font-weight:600 !important;
}

/* Secondary Button */
button[kind="secondary"]{
    background:#5865F2 !important;
    color:white !important;
    border:none !important;
    border-radius:25px !important;
    height:55px !important;
    font-weight:600 !important;
}

/* Hover */
button:hover{
    transform:scale(1.02);
}

/* Form Width */
.block-container{
    max-width:700px !important;
}
                </style>
                
    """,unsafe_allow_html=True)