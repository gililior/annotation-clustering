
from app import init, hello_page, main
import streamlit as st


CUAD_DESC = "In the following task you will be presented a single file from CUAD " \
            "dataset, consists of legal contracts from various types, " \
            "such as outsourcing, manufacturing, affiliate agreements contracts, " \
            "and more.  \n"


if __name__ == '__main__':
    init("CUAD", CUAD_DESC)
    if st.session_state.cur_page == 0:
        hello_page()
    else:
        main("CUAD.csv")
