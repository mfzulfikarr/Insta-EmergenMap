import streamlit as st
st.set_page_config(layout="wide", page_title="Welcome!")
st.title("Hello and Welcome!")
st.write("This is a streamlit project that uses Instaloader and folium map.")
st.write("This project able to locate projectroximate location for any historical emergency event in South Jakarta.")
st.markdown("<h1 style='text-align: center; color: white;'>DISCLAIMER NOTICE</h1>", unsafe_allow_html=True)
st.write("THIS PROJECT IS INTENDED SOLELY FOR PERSONAL OR NON-COMMERCIAL USE.\n\n"
         "Any activities involving commercial use are strictly prohibited, including but not limited to:\n\n"
         "- Research conducted for commercial purposes.\n"
         "- Use by any group, organization, or entity with commercial intentions (e.g., real estate planning).\n"
         "- Any other activities with a commercial focus or purpose.\n\n"
         "PERMITTED USES\n\n"
         "This project may only be used for purposes such as:\n\n"
         "- Studying emergency situation patterns in a specific area with educational purposes only.\n"
         "- Building portfolio with educational purposes.\n\n"
         "WITH THE AGREEMENT BETWEEN USER AND THE ACCOUNT OWNER.\n\n"
         "By using this project, you agree to obtain prior consent from the account owner of any Instagram account whose data you intend to collect. Failure to comply with this requirement may violate the rights of the account owner and could result in legal consequences.")
st.markdown("<h1 style='text-align: center; color: white;'>USE AT YOUR OWN RISK</h1>", unsafe_allow_html=True)
st.write("### How to use")
st.write("1. Select MAP menu from the sidebar to view the map\n"
         "2. Select the GET NEW DATA menu from the sidebar if you don't have any data yet\n"
         "3. If you already have some data in a form of .txt and don't want to do data collection then you can check the \"I already have the data\" checkbox\n"
         "4. If the data processing is done, you may go back to the MAP menu again\n"
         "5. You can check some graphs and see the data that you've processed before\n"
         "6. Done, those are things you can do in this project for now.\n\n")
st.write("### How to skip the collection process?")
st.write("1. Make sure you have the data in a format of .txt and with its date and time as the filename.\n\n"
         "For Example: 2024-06-17_01-01-05_UTC\n\n"
         "2. Make sure all the filenames are unique (you could add or substitute a second for the filename if there's a file that coincidentally has same date and time)\n"
         "3. Store all the .txt files to the \"collection\" folder\n"
         "4. In the GET NEW DATA MENU you may check the \"I already have the data\" checkbox and start the process.")
st.write("I'm sorry for the inconvenience if it's generating a lot of unidentified data or maybe a lot of bugs. I will try my best to improve the experience.\n")
st.write("### Thank you!!! :)")