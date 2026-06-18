import streamlit as st
def main():
    st.header("Hellow Ankur")
    name=st.text_input("Enter Your Nmae")
    st.button("display my name",type='primary',key='btn1',width='stretch')
    if st.button("display my name",type='primary',width='content'):
        print(f'Hello : {name}')

main()