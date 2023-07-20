import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import requests

key_number = -1

def main():
    st.write("# 무구 비카 by 길드-레오니스")
    st.write("")

    sql = "select class_alias from class_list"
    selected_job_class1 = ""
    selected_job_class2 = ""
    selected_job_class3 = ""

    selected_job_class1 = get_job_class_name()
    if selected_job_class1:
        selected_job_class2 = get_job_class_name()
        if selected_job_class2:
            selected_job_class3 = get_job_class_name()

    if selected_job_class1:
        columns = st.columns(3)
        columns[0].write(f"무구1: {selected_job_class1}")
        if selected_job_class2:
            columns[1].write(f"무구2: {selected_job_class2}")
            if selected_job_class3:
                columns[2].write(f"무구3: {selected_job_class3}")
    else:
        pass
    selected_job_classes = [j for j in [selected_job_class1, selected_job_class2, selected_job_class3] if j != ""]
    if selected_job_classes:
        vcs = fetch_vcs_for_job_in_brief(selected_job_classes)
        show_vcs_in_brief(vcs)
    else:
        st.write("### 무구를 선택해 주세요.")
    st.write("# 무구 비전카드 목록 - 자세히(언젠가는...)")

def fetch_vcs_for_job_in_brief(job_classes:list):
    # 비카이름, 이미지링크, 링크
    # select * from vc_for_job_list where 검1 = 0 and 검2 = 0 and 검3 = 1 and 총 = 1;
    sql = "select vc_name, vc_img_src, g8_link from vc_for_job_list where {}".format(' = 1 and '.join(job_classes)) + " = 1"
    fetched_vcs = fetch_data_from_db(sql)
    print(fetched_vcs)
    return fetched_vcs
def show_vcs_in_brief(vcs:list, col_num:int=4, width=100):
    columns = st.columns(col_num)
    cnt = 0
    print(len(vcs))
    while cnt < len(vcs):
        for c in range(col_num):
            display_image_with_link(*vcs[cnt],width, columns[c])
            cnt+=1
            if not cnt < len(vcs):
                break
def get_job_class_name():
    upper_columns = st.columns(3)
    input_char = upper_columns[0].text_input("캐릭이름:", key=get_key())
    if input_char:
        possible_chars = fetch_possible_chars(input_char)
        selected_char = upper_columns[1].selectbox("캐릭선택", [possible_chars], key=get_key())
    else:
        selected_char = upper_columns[1].selectbox("캐릭선택", [""], key=get_key())

    sql = "select class_alias from class_list"
    class_list = [""] + [d[0] for d in fetch_data_from_db(sql)]
    if selected_char:
        fetched_class = fetch_class(selected_char)
        index = get_index_by_job(fetched_class)
        selected_job_class = upper_columns[2].selectbox("무구직업", class_list, index=index, key=get_key())
    else:
        selected_job_class = upper_columns[2].selectbox("무구직업", class_list, index=0, key=get_key())
    return selected_job_class
def get_key():
    global key_number
    key_number += 1
    return key_number
def fetch_possible_chars(char_name):
    return [char_name]
def fetch_class(char_name):
    return "검1"
def get_index_by_job(job):
    return 1
def display_image_with_link(caption_text=None, image_url=None, hyperlink_url=None, image_width=100, canvas=None):
    if canvas == None:
        canvas = st
        print("Canvas is st")

    centered_image_with_caption = f'''
        <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
            <a href="{hyperlink_url}" target="_blank" rel="noopener noreferrer">
                <img src="{image_url}" alt="Image" width="{image_width}">
            </a>
            <p style="text-align: center;">{caption_text}</p>
        </div>
    '''
    canvas.markdown(centered_image_with_caption, unsafe_allow_html=True)
    # # Display the image with a clickable link
    # canvas.markdown(f'<div style="text-align: center;"><a href="{link_url}" target="_blank"><img src="{image_path} width=50 alt="{caption}" style="max-width:100%;"></a></div>', unsafe_allow_html=True)
    # # Display the caption
    # canvas.write(caption)

def connect_db():
    # Connect to the MySQL database
    db_connection = mysql.connector.connect(
        host='146.56.43.43',
        user='ffbemaster',
        password='aksaksgo1!',
        database='ffbe')
    return db_connection
def fetch_data_from_db(sql):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    res = [list(d) for d in cursor.fetchall()]
    return res
# Run the Streamlit app
if __name__ == "__main__":
    main()