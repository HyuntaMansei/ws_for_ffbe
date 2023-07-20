import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import requests

def display_image_link(canvas, image_path=None, caption=None, link_url=None):
    # Display the image with a clickable link
    canvas.markdown(f'<div style="text-align: center;"><a href="{link_url}" target="_blank"><img src="{image_path}" alt="{caption}" style="max-width:100%;"></a></div>', unsafe_allow_html=True)
    # Display the caption
    canvas.write(caption)
def show_image(image_urls:list):
    # # Replace these with the image URLs you want to display
    # image_urls = [
    #     "https://img.game8.jp/8378156/07abc8beb1a9891f0d2289099cf00632.png/show",
    #     "https://img.game8.jp/8229107/bf83dde4914987f13acfc218e5174903.png/show",
    #     "https://img.game8.jp/8172868/ca520efa4bb343774f08884499ea31c0.png/show",
    #     # Add more image URLs as needed
    # ]

    # Replace this with the desired width and height of each image
    image_width = 100
    image_height = 150

    # Create a horizontal layout with multiple columns
    columns = st.columns(len(image_urls))

    # Display each image in a separate column
    for i, column in enumerate(columns):
        column.image(image_urls[i], caption=f"Image {i+1}", width=image_width)
def connect_db():
    # Connect to the MySQL database
    db_connection = mysql.connector.connect(
        host='146.56.43.43',
        user='ffbemaster',
        password='aksaksgo1!',
        database='ffbe')

    return db_connection
def main():
    # Replace these with the image URLs you want to display
    image_urls = [
        "https://img.game8.jp/8378156/07abc8beb1a9891f0d2289099cf00632.png/show",
        "https://img.game8.jp/8229107/bf83dde4914987f13acfc218e5174903.png/show",
        "https://img.game8.jp/8172868/ca520efa4bb343774f08884499ea31c0.png/show",
        "https://img.game8.jp/8378156/07abc8beb1a9891f0d2289099cf00632.png/show",
        "https://img.game8.jp/8229107/bf83dde4914987f13acfc218e5174903.png/show",
        "https://img.game8.jp/8172868/ca520efa4bb343774f08884499ea31c0.png/show",
        "https://img.game8.jp/8229107/bf83dde4914987f13acfc218e5174903.png/show",
        "https://img.game8.jp/8172868/ca520efa4bb343774f08884499ea31c0.png/show",
        # Add more image URLs as needed
    ]

    # Replace this with the desired width and height of each image
    image_width = 100
    image_height = 150

    show_image(image_urls)
    show_image(image_urls)

    columns = st.columns(8)
    columns[0].write("I am 1")
    columns[0].write("I am 1")
    st.write(888)
    columns[0].write("I am 1")
    columns[0].write("I am 1")
    columns[1].write(2)
    columns[7].image("https://img.game8.jp/8378156/07abc8beb1a9891f0d2289099cf00632.png/show")


    char_name = st.text_input("Character Name:")
    st.write(char_name)

    db_conn = connect_db()
    cursor = db_conn.cursor()

    sql = "SELECT char_name, char_img_src, char_main_job FROM char_list"
    cursor.execute(sql)
    res = cursor.fetchall()
    # for r in res:
    res_data = pd.DataFrame(res, columns=[col[0] for col in cursor.description])
    st.dataframe(res_data)
    char_data = res_data.iloc[0]


    res_data.items()

    cursor.close()
    db_conn.close()

    # Image file path
    image_path = char_data[1]

    # Caption for the image
    caption = char_data[0]

    # Link URL
    link_url = "https://www.naver.com"
    (display_image_link(columns[0], image_path, caption, link_url))
    (display_image_link(columns[2], image_path, caption, link_url))
    (display_image_link(columns[4], image_path, caption, link_url))

    # Sample data for the ComboBox options
    options_map = {
        'Fruit': ['Apple', 'Banana', 'Orange'],
        'Vegetable': ['Carrot', 'Broccoli', 'Tomato'],
        'Animal': ['Dog', 'Cat', 'Elephant'],
    }

    # Create a ComboBox to select the category
    category = st.selectbox('Select a category:', ['']+list(options_map.keys()))

    # Check if a category is selected
    if category:
        # Get the selected category's options
        selected_options = options_map.get(category, [])

        # Create a ComboBox to select an option based on the selected category
        selected_option = st.selectbox('Select an option:', selected_options)

        # Display the selected option
        if selected_option:
            st.write(f'You selected: {selected_option}')
    else:
        selected_option = st.selectbox('Select an option:', np.random.rand(5))
        if selected_option:
            st.write(f'You selected: {selected_option}')
# Run the Streamlit app
if __name__ == "__main__":
    main()