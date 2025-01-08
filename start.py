import streamlit as st
st.set_page_config(layout="wide", page_title="Welcome!")
st.title("Hello and Welcome!")
st.write("This is a streamlit app that uses Instaloader Scraper and folium map.")
st.write("This app able to locate approximate location for any historical emergency event in South Jakarta.")
st.write("What is this app for? Well, it can be use for:\n\n"
         "- Researchers on researching the characteristics of emergency situations in South Jakarta.\n"
         "- Checking on how many emergency activities around the area before deciding on where your new home will be.\n"
         "- Builders or city planners to decide what kinds of emergency situation their project will be facing frequently.\n"
         "- Studying the emergency situation's patterns in South Jakarta.\n"
         "- Your portfolio if you need some.\n\n")
st.write("### How to use")
st.write("1. Select MAP menu from the sidebar to view the map\n"
         "2. Select the GET NEW DATA menu from the sidebar if you don't have any data yet\n"
         "3. If you already have some data in a form of .txt and don't want to do another scrape then you can check the \"I already have the data\" checkbox\n"
         "4. If the data processing is done, you may go back to the MAP menu again\n"
         "5. You can check some graphs and see the data that you've processed before\n"
         "6. Done, those are things you can do in this app for now.\n\n")
st.write("### How to skip the scraping process?")
st.write("1. Make sure you have the data in a format of .txt and with its date and time as the filename.\n\n"
         "For Example: 2024-06-17_01-01-05_UTC\n\n"
         "2. Make sure all the filenames are unique (you could add or substitute a second for the filename if there's a file that coincidentally has same date and time)\n"
         "3. Store all the .txt files to the scrape-results folder\n"
         "4. In the GET NEW DATA MENU you may check the \"I already have the data\" checkbox and start the process.")
st.write("I'm sorry for the inconvenience if it's generating a lot of unidentified data or maybe a lot of bugs. I will try my best to improve the experience.\n")
st.write("### Thank you!!! :)")