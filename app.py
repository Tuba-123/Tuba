import streamlit as st
st.title("Welcome to Streamlit")
name = st.text_input("TUBA")
if name: st.success(f"Hello {TUBA}")
age = st.slider("Select your age", 1, 100)
st.write("Age:", age)
if st.button("Celebrate"): st.balloons()
