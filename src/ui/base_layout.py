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
                
               
              /* #MainMenu,header,footer{
                     visibility:hidden;
                }*/
                
                
                .block-container{
                     padding-top:1.5rem !important;
                }
                
                h1{
                    font-family:'Climate Crisis', sans-serif !important;
                    font-size:2.5rem !important;
                    line-height:0.9 !important;
                    margin-bottom:0rem !important;
                   
                }
                
                h2{
                    font-family:'Climate Crisis', sans-serif !important;
                    font-size:2rem !important;
                    line-height:0.9 !important;
                    margin-bottom:0rem !important;
                     color:black !important;
                }
                
                h4{
                     font-family:'Outfit',sans-serif !important;
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
                      background:#EB459E !important;
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
                
                </style>
                
    """,unsafe_allow_html=True)