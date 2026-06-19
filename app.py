import streamlit as st
def main():
    
    st.header("Hellow Ankur")
    name=st.text_input("Enter Your Nmae")
    col1,col2=st.columns(2,gap='small')
    with col1:
       st.button("display my name",type='primary',key='btn1',width='stretch')
    with col2:
        if st.button("display my name",type='primary',width='stretch'):
            print(f'Hello : {name}')

main() 


