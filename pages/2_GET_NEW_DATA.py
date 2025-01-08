import streamlit as st
import time
from datetime import datetime, timedelta
import os
import subprocess
import pandas as pd
import mysql.connector
from mysql.connector import Error
curr_dir = os.path.dirname(__file__)
st.set_page_config(layout="wide", page_title="Collect New Data")
if "disabled" not in st.session_state:
    st.session_state.disabled = False
def btn_status():
    st.session_state.disabled = True
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False
# Dialog Function
@st.dialog("Notice")
def confirmed(src_id, since_str, until_str, date_diff):
    st.write(f"Confirmation: \n\n"
            f"Search from: **{src_id}**\n\n"
            f"Search since: **{since_str}**\n\n"
            f"Search Until: **{until_str} ({date_diff} days)**\n\n"
            "If it's correct you may press Confirm to start")
    if st.button("Confirm"):
        st.session_state.confirmed = True
        st.rerun()
        st.write("Getting new data, please wait")
    if st.button("Cancel"):
        st.session_state.disabled = False
        st.session_state.confirmed = False
        st.rerun()
@st.dialog("Notice")
def confirmedSkip():
    st.write(f"Confirmation: \n\n"
            "No data collecting will be performed, only data processing\n\n"
            "You may press Confirm to start when you ready")
    if st.button("Confirm"):
        st.session_state.confirmed = True
        st.rerun()
        st.write("Processing data, please wait")
    if st.button("Cancel"):
        st.session_state.button_status = False
        st.session_state.confirmed = False
        st.rerun()
# Script Running Function
def run_script(script_name, *args):
    try:
        result = subprocess.run(["python", script_name] + list(args), check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        st.error("Oops! an unexpected error occured. You might wanna do this steps: \n\n"
                 "1. Make sure the Instagram ID is available (not banned) and not private\n"
                 "2. Check your network connection, make sure it's stable\n"
                 "3. If there are a lot of posts (over 1000), reduce the date range\n"
                 "4. Wait for a moment before continuing again\n\n"
                 "Sorry for the inconvenience (˶ᵕ︵ᵕ˶)\n\n"
                 f"Error in {script_name}. Details: {e.stderr}") #<-- The error handling isn't working well yet, so I have to improvise lol :p
def load_predicted_data():
    try:
        df = pd.read_csv(os.path.join(curr_dir, '../source/Datasets/extractedData.csv'))
        return df
    except FileNotFoundError:
        st.error("Data Not Found")
        return None
# Processing Function

def scrapingData(src_id, since_str, until_str_adj):
    progressBar.progress(17, text ="Reading the newspaper...")
    run_script(os.path.join(curr_dir, "../source/src/runscraper.py"), since_str, until_str_adj, src_id)
def processingData():
    progressBar.progress(34, text ="Reading the newspaper...")
    run_script(os.path.join(curr_dir, "../source/src/convertData.py"))
    progressBar.progress(51, text ="Cleaning the dishes...")
    run_script(os.path.join(curr_dir, "../source/src/cleaningData.py"))
    progressBar.progress(68, text ="Watching the forecasts...")
    run_script(os.path.join(curr_dir, "../source/src/predictData.py"))
    progressBar.progress(85, text ="Taking some notes...")
    run_script(os.path.join(curr_dir, "../source/src/extractCategory.py"))
    progressBar.progress(97, text ="Taking some notes...")
    run_script(os.path.join(curr_dir, "../source/src/extractLocation.py"))
    progressBar.progress(100, text ="Launching the notes to the clouds...")
# Database Config and Functions
try:
    dbPool=mysql.connector.pooling.MySQLConnectionPool(
        pool_name="strlitPool",
        pool_size=10,
        host="localhost",
        user="root",
        password="",
        database="db_strlit"
    )
except Error as e:
    st.error(f"Failed to create connection pool. Detail: {e}")
def get_db_connection():
    if dbPool is None:
        st.error("Connection to pool is not initialized")
        return None
    try:
        return dbPool.get_connection()
    except Error as e:
        st.error(f'Something went wrong, unable to get a connection from the pool. Detail: {e}')
        return None
def upload_data_to_db(df):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None:
            st.error("Database connection failed")
            return
        cursor = conn.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS finalDatanew (
                id INT AUTO_INCREMENT PRIMARY KEY,
                datetime DATETIME,
                content VARCHAR(255),
                textClean VARCHAR(255),
                isinfo VARCHAR(255),
                category VARCHAR(255),
                location VARCHAR(255),
                UNIQUE KEY unique_record (datetime, content)
            )
        """
        cursor.execute(create_table_query)
        # Insert dataframe into the table
        cols = "`, `".join([str(i) for i in df.columns])
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO `finalDatanew` (`{cols}`) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE content=content"
        for i, row in df.iterrows():
            cursor.execute(sql, tuple(row))
        conn.commit()
        st.write("The launch was a success!")
    except Error as e:
        st.error(f"Something went wrong: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
# Main Functions
def main():
    st.title("Get New Data")
    skipScrape = st.checkbox("I already have the data, just need it to be processed to the map")
    if skipScrape:
        try:
            src_id = st.text_input("Instagram ID without @", placeholder="Example: jakarta.terkini", disabled=True).lstrip('@')
            since_date = st.date_input("Search Since", datetime.now().date() - timedelta(days=10), max_value = datetime.now(), disabled=True)
            until_date = st.date_input("Search Until", datetime.now().date(), min_value = since_date, max_value = datetime.now(), disabled=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        src_id = st.text_input("Instagram ID without @", placeholder="Example: jakarta.terkini", disabled=st.session_state.disabled).lstrip('@')
        try:
            since_date = st.date_input("Search Since", datetime.now().date() - timedelta(days=10), max_value = datetime.now(), disabled=st.session_state.disabled)
        except:
            st.error("Whoa! You almost travel to the future there (￣ᴗ￣ᵕ)\n\n"
                    "The Since Date could not be higher than Today's Date.")
        until_date = st.date_input("Search Until", datetime.now().date(), min_value = since_date, max_value = datetime.now(), disabled=st.session_state.disabled)
        until_date_adj = until_date + timedelta(days=1)
        date_diff = (until_date - since_date).days
        since_str = since_date.strftime("%Y-%m-%d")
        until_str = until_date.strftime("%Y-%m-%d")
        until_str_adj = until_date_adj.strftime("%Y-%m-%d")
    startBtn = st.button("Start Processing", on_click=btn_status)
    if startBtn:
        try:
            if skipScrape:
                confirmedSkip()
            else:
                if not src_id.strip():
                    st.error("Oops! The Instagram ID is still empty (￣ᴗ￣ᵕ)")
                elif until_date > datetime.now().date():
                    st.error("Oops! I guess there is a mix up (￣ᴗ￣ᵕ)\n\n"
                            "The Until Date could not be higher than Today's Date.")
                elif until_date < since_date:
                    st.error("Oops! I guess there is a mix up (￣ᴗ￣ᵕ)\n\n"
                            "The Since Date should not be higher than the Until Date.")
                else:
                    confirmed(src_id, since_str, until_str, date_diff)
        except Exception as e:
            st.error(f"An error occured: {e}")
    if st.session_state.confirmed:
        if not skipScrape:
            scrapingData(src_id, since_str, until_str_adj)
        processingData()
        df = load_predicted_data()
        if df is not None:
            upload_data_to_db(df)
        if "confirmed" in st.session_state:
            st.session_state.confirmed = False
            st.session_state.disabled = False
        st.success('Finished!')
progressBar = st.progress(0)
progressBar.empty()

if __name__ == "__main__":
    main()