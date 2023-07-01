
from app import init, hello_page, main
import streamlit as st


DESC_10K = "In the following task you will be presented a single file from the 10k " \
           "dataset, consists of financial company annual reports.  \n"

if __name__ == '__main__':
    init("10k", DESC_10K)
    if st.session_state.cur_page == 0:
        hello_page()
    else:
        main("10k-ver2.csv")
