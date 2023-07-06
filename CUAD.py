
from app import init, hello_page, main
import streamlit as st


CUAD_DESC = "In the following task you will be presented a single file from CUAD " \
            "dataset, consists of legal contracts from various types, " \
            "such as outsourcing, manufacturing, affiliate agreements contracts, " \
            "and more.  \n"


def generate_rep_map_to_column():
    CUAD_header = ["username", "filename", "file_length", "Marketing And Sales",
                   "Disclaimer Of Warranties", "Payments And Fees", "Indemnification",
                   "Confidentiality"	"Waiver And Amendment"	"Proprietary Rights"	
                   "Company:  Immunotolerance, Inc",
                   "Representations, Warranties And Covenants",	"Upon Termination"]

    map_to_columns = {}
    for i, header in enumerate(CUAD_header):
        if header in {"username", "filename", "file_length"}:
            continue
        letter = string.ascii_uppercase[i]
        map_to_columns[header] = letter

    return map_to_columns


if __name__ == '__main__':
    init("CUAD", CUAD_DESC)

    if 'column_map' not in st.session_state:
        representative_map_to_column = generate_rep_map_to_column()
        st.session_state['column_map'] = representative_map_to_column

    if st.session_state.cur_page == 0:
        hello_page()
    else:
        main("CUAD.csv")
