import sys, os, re, time
from streamlit import cli as stcli
import streamlit as st
from main_page import mainpage
from infopage import info

def gillajabi_app():
    #st.set_page_config(layout="wide")
    st.markdown("""
        <style>
        .big-font {
            font-size:24px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.title("길라잡이! - Gillajab-i!")
    st.sidebar.title("길라잡이! - Gillajab-i!")
    app_mode = st.sidebar.radio(
        "Go to", ("Gillajab-i!", "Gillajab-i Info")
    )

    st.sidebar.info(
        "Gillajab-i! was developed for aspiring learners of the Korean Language."
        "We trained an ASR Model that detects the phonemes of the Korean Language,"
        "and developed an algorithm to compare the based phonemes to yours!"

    )

    if app_mode == "Gillajab-i!":
        mainpage()
    elif app_mode == "Gillajab-i Info":
        info()

if __name__ == "__main__":
    if st._is_running_with_streamlit:
        gillajabi_app()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0], "--server.port", "7001"]
        sys.exit(stcli.main())
