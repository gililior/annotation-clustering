
import numpy as np
import streamlit as st
import pandas as pd
import random
import gspread
import string

credentials = {
  "type": "service_account",
  "project_id": "cluster-segments",
  "private_key_id": "8d9cb8b9eba0856375220b5f26f67917d19b7d70",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCNN/rUlJTEUral\nNWh+d+Bk6ssjXCktwtuI77glU24gzMFfFwtHpCilYrljPP7/Ufzyrf1YxOGf3MkR\np4zikrJ5NOuS72j+dvVunAgJiRabIhVnKDAvq3/A/Kkx9UMPgJFN8lyUhkLuq887\n0bMXT+FcqiFUvmW4XBEFT9ZFPnnlms9iifMpebgNr1E+KCNCQ+9a5mh5vaQuJn+l\nNvIdIBo0C06a23fozpKl7Vbk3PQ8sWI/D7M3VEN3o0LKV+tbwme5YO7RePrzBKuN\nZ4yLUH3pYolRpbIwHxT8BbWIgGLs3MhIuFnI7cWzXciQXfIN2VhyLll4Jz2Kvhtz\n/VkZd1r3AgMBAAECggEAEv8kztPt7zrxNugoVlrp5KlxCiCrqWw8+/7DVsISXncs\nzA3dhpWeoiDVr3PVGaN902d0XSye7VJV+foACbqSJ5vm1K1AAnseKPL0YdP/Jn8/\nQdE2KjN3zA4w9Hd5vewdn86qhZBKELEr/3AGF2y3dC+urCewp0w7Peuvd0EgRLKL\nY4LujH6TilR+buYruUzKwZ5vcXXjuubFhPxHK/CvtwyD18rMHH4pnMoXGDYFBTz3\n88/j/L9SdxgvX3bAM7LepsfHKpA3fLpiIv5Pkdvo9DhLYRPVVfuWV6Yx+Nux8s2x\nJgGWwe9a0laDTRQdgi5kStPyOZyWvqJ+S1iRYiymAQKBgQDE8LnvMXbCf4D60Joj\nYoHp0masjw47JwjLZ2JF/jhQVJjkpGHHIWDfRO1KD2tcaWUjd2L6AItYNdmmjbEF\nHHr3H684zz3adCP6B9iNE6uuIEwNkrMS4RmFM+ChoM5QCl0gOpuWAbOYvxzQP/Qd\nJ/fwWderD98SCTG1tPAwVxrncQKBgQC3kXRtc65mMmtpYOBkPsFwcIl1w4DMbmtI\nHFOfVm4v3MTMVcKFW84piVBQmZfFfq5cBxk3OIwT9NFSJFB93wQA0FTZQEY30Jg/\nTcrbr/4q2GI59rlKAALhdYt6JY5zGkMkdpHwvjjgPo13g04cuspz6D6bbeREu9It\nl1w8497E5wKBgAaN0FJCfiZI4fz21jpZO+ORKfOSKzISwXsrbJzRsgQSXKg3RD3B\nQZ0MiS0OyE7h/wioH3YccIa1/BFL49k8smbo+gbU9sT/WncmrbE8N1lrH7zP5f+5\n2ASTzmTymgsV3TWGXcknM1fg/E994VzbCKhKBSBfPdg20B2w8NFbBL0xAoGAbCSr\n04NQHfLcJpOk/kmeSjByOsd3THhMiYnulbMkbNwBsGNhmpEQLpYvk5w4tmfALoUc\nDNUqaONUobC1HsJQqG4TXn2oIF+qIbkhpjTTZshdbcp1NCw3hj1qcwZHGnZBUezs\nY0idVzZivyLC1NgSRyBuKcEetoNz+dnuxAx2g8cCgYBlNmFu8CeXsc2HZ/jf6Ri8\nLztzp3bEXZmjUA/VYaU33t73oZssERW1yGkw6MDHuKJoeHjtql7rBIXLRHzLqaRf\no1ErRtmTf4X0KIpzHzkFIdeQ+ymPrDCAF6XG0aqFFP4G2iT5NdytbCRAkOR1RkMV\nobjqSZeHeh/NidRzkQEbig==\n-----END PRIVATE KEY-----\n",
  "client_email": "cluster-segments-annotation@cluster-segments.iam.gserviceaccount.com",
  "client_id": "111788008470838013578",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cluster-segments-annotation%40cluster-segments.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

if "ws" not in st.session_state:
    gc = gspread.service_account_from_dict(credentials)
    # 2. Load the sheet
    sh = gc.open("cluster-annotation")
    while not st.button("10k") and not st.button("CUAD"):
        pass
    option = st.selectbox('Choose dataset', ('CUAD', '10k'))
    st.session_state.df_path = f"{option}.csv"
    # 3. Open the specific worksheet
    st.session_state.ws = sh.worksheet(option)
    st.session_state.first_row_index = len(st.session_state.ws.col_values(1)) + 1
    # 2. Update the sheet
    st.session_state.ws.update('A' + str(st.session_state.first_row_index), 'username')
    st.session_state.ws.update('B' + str(st.session_state.first_row_index), 'filename')
    st.session_state.i = 0


def generate_random_colors(length):
    colors = []
    for _ in range(length):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        colors.append(f"rgb({red}, {green}, {blue})")
    return colors


def generate_colors_map(df):
    representatives = df[df["best_cluster"] == True].representative.unique()
    colors = generate_random_colors(len(representatives))
    color_map = {}
    for i, rep in enumerate(representatives):
        color_map[rep] = colors[i]
    return color_map


def generate_sidebar_linking(color_map, line_numbers, total):
    sorted_keys = sorted(line_numbers, key=lambda k: line_numbers[k][0])
    for representative in sorted_keys:
        id_rep = get_id_rep(representative)
        start, end = line_numbers[representative]
        st.sidebar.markdown(
            f"<a style='border: 3px solid {color_map[representative]}; padding: 5px; font-size: 16px; color: black;' href='#{id_rep}'>{representative}</a>",
            unsafe_allow_html=True)
        st.sidebar.select_slider(label='select range', label_visibility='hidden',
                                 key=representative,
                                 options=list(np.arange(1, total)), value=[start, end])



@st.cache
def load_csv(file_path):
    return pd.read_csv(file_path)


def generate_rep_map_to_column(df):
    representatives = df[df["best_cluster"] == True].representative.unique()
    rep_to_column = {}
    for i, rep in enumerate(representatives):
        index_letter = i+2
        letter = string.ascii_uppercase[index_letter]
        st.session_state.ws.update(letter + str(st.session_state.first_row_index), rep)
        rep_to_column[rep] = letter
    return rep_to_column


def main():
    # Page title and description
    st.title("Conceptual ToC Viewer")

    # File selection
    # Load CSV data
    if "df" not in st.session_state:
        st.session_state["df"] = pd.read_csv(st.session_state.df_path)
    df = st.session_state["df"]

    # Set a variable once after a new CSV file is loaded
    if 'color_map' not in st.session_state:
        color_map = generate_colors_map(df)
        st.session_state['color_map'] = color_map
        representative_map_to_column = generate_rep_map_to_column(df)
        st.session_state['column_map'] = representative_map_to_column
    color_map = st.session_state['color_map']
    representative_map_to_column = st.session_state['column_map']

    st.sidebar.markdown("<h3 style='font-size: 24px;'>ToC (color mapping)</h3>",
                        unsafe_allow_html=True)

    group_by_filename = df.groupby("filename").groups

    all_files = list(group_by_filename.keys())
    if st.button('submit'):
        st.session_state.i += 1
        # write session state slider
        # Update the google sheet
        # 1. Find in which row we need to put the new annotations
        next_row_ind = len(st.session_state.ws.col_values(1)) + 1
        # 2. Update the sheet
        st.session_state.ws.update('A' + str(next_row_ind), 'tbd')
        st.session_state.ws.update('B' + str(next_row_ind), all_files[st.session_state.i - 1])
        for representative in representative_map_to_column:
            if representative in st.session_state:
                letter = representative_map_to_column[representative]
                st.session_state.ws.update(letter + str(next_row_ind), str(st.session_state[representative]))
                st.session_state.pop(representative)
    selected_file = all_files[st.session_state.i]
    st.write(selected_file)
    # Filter dataframe based on selected file
    filtered_df = df.loc[group_by_filename[selected_file]]
    filtered_df = filtered_df.sort_values(by=['title_index']).reset_index()

    if not filtered_df.empty:
        display_single_file(color_map, filtered_df)
    else:
        st.write("Selected file not found in the CSV.")


def display_single_file(color_map, filtered_df):

    st.header("Text Content:")

    all_paragraphs, labels_start_end = get_paragraphs(filtered_df)

    line_numbers = {}
    is_open = (False, None)
    for i, paragraph in enumerate(all_paragraphs):
        prev_label, current_label = labels_start_end[i]
        if prev_label is not None:
            line_numbers[prev_label] = (line_numbers[prev_label], i)
            color = color_map[prev_label]
            st.markdown(f"""<hr style="height:10px;border:none;color:{color};background-color:{color};" /> """, unsafe_allow_html=True)
            is_open = (False, None)
        if current_label is not None:
            id_rep = get_id_rep(current_label)
            st.markdown(f"<h3 id='{id_rep}'>{current_label}</h3>", unsafe_allow_html=True)
            color = color_map[current_label]
            st.markdown(f"""<hr style="height:10px;border:none;color:{color};background-color:{color};" /> """,
                        unsafe_allow_html=True)
            is_open = (True, current_label)
            line_numbers[current_label] = i+1
        html_text = f""" <table><tr><th> {i+1} </th><th> {paragraph} </th></tr></table>"""
        st.markdown(html_text, unsafe_allow_html=True)

    if is_open[0]:
        label = is_open[1]
        color = color_map[label]
        st.markdown(
            f"""<hr style="height:10px;border:none;color:{color};background-color:{color};" /> """,
            unsafe_allow_html=True)
        line_numbers[label] = (line_numbers[label], len(all_paragraphs))

    generate_sidebar_linking(color_map, line_numbers, len(all_paragraphs)+1)


def get_id_rep(representative):
    return representative.lower().replace('.', '').replace(' ', '-')


def get_paragraphs(filtered_df):
    all_paragraphs = []
    all_labels = []
    labels_start_end = []
    for i, row in filtered_df.iterrows():
        paragraph = f"{row['title_text']}\n\n{row['section_text']}\n\n"
        if i + 1 < len(filtered_df):
            if row['section_text'] == filtered_df.loc[i + 1]['title_text']:
                paragraph += f"{filtered_df.loc[i + 1]['section_text']}\n\n"
        label = row["representative"] if row["best_cluster"] else None
        prev = current = None
        if i == 0 and label is not None:
            current = label
        if i > 0 and all_labels[-1] != label:
            if i > 0 and all_labels[-1] is not None:
                prev = all_labels[-1]
            if label is not None:
                current = label
        labels_start_end.append((prev, current))
        all_paragraphs.append(paragraph)
        all_labels.append(label)

    return all_paragraphs, labels_start_end


if __name__ == '__main__':
    main()
