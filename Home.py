import streamlit as st

st.set_page_config(page_title='ReMorroc Calc', page_icon=':crossed_swords:')

st.title('Return to Morroc Calculator')

presentationString = (
    'This is a webapp to calculate a preview damage for your skills in the '\
    'Return to Morroc Ragnarok Server'\
    '\n\n'
    'https://returntomorroc.com/')

st.markdown(presentationString)