import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import requests

key_number = -1
def main():
    divide_screen(4)
    Title_msg = convert_to_center_msg("무구 비카 by 길드-레오니스 v0.2")
    Centered_msg = f"""<p style = "font-size: 2em; text-align: center;" >{Title_msg}</p>"""
    st.write(Centered_msg, unsafe_allow_html=True)

    sql = "select class_alias from class_list"

    columns = st.columns(2)
    selected_job_class1 = get_job_class_name_simple(columns[0])
    selected_job_class2 = get_job_class_name_simple(columns[1])

    if selected_job_class1:
        columns = st.columns(3)
        columns[0].write(f"무구1: {selected_job_class1}")
        if selected_job_class2:
            columns[1].write(f"무구2: {selected_job_class2}")

    selected_job_classes = [j for j in [selected_job_class1, selected_job_class2] if j != ""]
    chars = fetch_chars_in_brief()
    if selected_job_classes:
        st.markdown(f"### 해당 비전카드")
        vcs = fetch_vcs_for_job_in_brief(selected_job_classes)
        show_vcs_in_brief(vcs,4)

        divide_screen(8)
        st.markdown(f"### 해당 무구 캐릭터:{selected_job_classes}")
        show_chars_in_brief(chars, selected_job_classes)
        if selected_job_class1:
            st.markdown(f"### 무구1 캐릭터:{selected_job_class1}")
            show_chars_in_brief(chars, selected_job_class1)
        if selected_job_class2:
            st.markdown(f"### 무구2 캐릭터:{selected_job_class2}")
            show_chars_in_brief(chars, selected_job_class2)
    else:
        st.write("### 무구를 선택해 주세요.")
    st.write("To add later")
def divide_screen(col_num:float):
    r = (1/col_num)*100
    st.write(f'''<style>
    [data-testid="column"] {{
        width: calc({r}% - 1rem) !important;
        flex: 1 1 calc({r}% - 1rem) !important;
        min-width: calc({r}% - 1rem) !important;
    }}
    </style>''', unsafe_allow_html=True)
def fetch_vcs_for_job_in_brief(job_classes:list):
    # 비카이름, 이미지링크, 링크
    # select * from vc_for_job_list where 검1 = 0 and 검2 = 0 and 검3 = 1 and 총 = 1;
    sql = "select vc_name, vc_trsl_name, vc_jp_name, vc_g8_link, vc_img_src from vc_for_job_list where {}".format(' = 1 and '.join(job_classes)) + " = 1"
    fetched_vcs = fetch_data_from_db(sql)
    # print(fetched_vcs)
    return fetched_vcs
def fetch_chars_in_brief():
    #캐릭터이름, 이미지링크, 겜8링크
    sql_query = """SELECT * from char_list"""
    fetched_chars, col_names = fetch_data_from_db_with_col_names(sql_query)
    df = pd.DataFrame(fetched_chars, columns=col_names)
    return df
def show_vcs_in_brief(vcs:list, col_num:int=4, width=100):
    cnt = 0
    while cnt < len(vcs):
        columns = st.columns(col_num)
        for c in range(col_num):
            # vc: vc_name, vc_trsl_name, vc_jp_name, vc_g8_link, vc_img_src
            # caption, image, hyperlink
            vc = vcs[cnt]
            if vc[0]:
                vc_name = vc[0]
            elif vc[1]:
                vc_name = vc[1]
            else:
                vc_name = vc[2]
            g8_link = vc[3]
            image_src = vc[4]
            display_image_with_link(vc_name, g8_link, image_src, width, columns[c])
            cnt+=1
            if not cnt < len(vcs):
                break
def show_chars_in_brief(chars:pd.DataFrame, selected_chars, width=70):
    # chars = Dataframe
    if type(selected_chars) != list:
        selected_chars = [selected_chars,]
    col_num = 8
    cnt = 0
    element_list = ['화', '빙', '풍', '토', '뇌', '수', '명', '암']
    chars_on_element = {}
    # 속성별로 해당하는 클라스 캐릭터를 나누어 담는다.
    for e in element_list:
        chars_on_element[e] = chars[(chars['char_element']==e)
                                    & (chars['char_main_job_class_alias'].isin(selected_chars))]
    for e in element_list:
        if len(chars_on_element[e]):
            print(f"for {e}", "-"*50)
            print(chars_on_element[e]['char_trsl_name'])

    #캐릭터를 속성별로 출력
    columns = st.columns(col_num)
    for i, e in enumerate(element_list):
        print(chars_on_element[e])
        write_in_center(e, columns[(i % col_num)])
        for _, character in chars_on_element[e].iterrows():
            char_name = get_char_name(character)
            g8_link = character['char_g8_link']
            image_src = character['char_img_src']
            display_image_with_link(char_name, g8_link, image_src, width, columns[i])
            # display_image_with_link(char_name, g8_link, image_src, width, columns[(i%col_num)])
def get_char_name(character):
    print(type(character))
    if character['char_name']:
        return character['char_name']
    if character['char_trsl_name']:
        return character['char_trsl_name']
    if character['char_jp_name']:
        return character['char_jp_name']
    else:
        return "NoName"
def get_job_class_name_simple(canvas=None):
    if not canvas:
        canvas = st
    sql = "select class_alias from class_list"
    class_list = [""] + [d[0] for d in fetch_data_from_db(sql)]
    selected_job_class = canvas.selectbox("무구직업", class_list, key=get_key())
    return selected_job_class
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
def write_in_center(msg, canvas=None):
    if not canvas:
        canvas:st
    canvas.write(f"<div style='text-align: center'>{msg}</div>", unsafe_allow_html=True)
def display_image_with_link(caption_text=None, hyperlink_url=None, image_url=None, image_width=50, canvas=None):
    if canvas == None:
        canvas = st
    centered_image_with_caption = f'''
        <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
            <a href="{hyperlink_url}" target="_blank" rel="noopener noreferrer">
                <img src="{image_url}" alt="Image" width="{image_width}">
            </a>
            <div style="display: flex; justify-content: center;">
                <p style="font-size: 0.5em;">{caption_text}</p>
            </div>
        </div>
    '''
    canvas.markdown(centered_image_with_caption, unsafe_allow_html=True)
def convert_to_center_msg(msg:str):
    return f'''
        <div style="display: flex; justify-content: center;">
            <h3>{msg}</h3>
        </div>'''
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
    cursor.close()
    conn.close()
    return res
def fetch_data_from_db_with_col_names(sql):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    res = [list(d) for d in cursor.fetchall()]
    col_names = cursor.column_names
    cursor.close()
    conn.close()
    return res, col_names
# Run the Streamlit app
if __name__ == "__main__":
    main()