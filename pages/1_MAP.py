import pandas as pd
# import json
# import requests
# import time
import streamlit as st
# import folium
# from streamlit_folium import folium_static, st_folium
# from folium.plugins import TagFilterButton
# from geopy.distance import geodesic
# import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
import numpy as np
from pages.pageutils.maputils import MapUtils
st.set_page_config(layout="wide", page_title="South Jakarta Emergency Map")
maps = MapUtils()
data = maps.get_data()
# Streamlit UI
st.title('South Jakarta Emergency Map')
# Show the map
maps.show_map()
# Process data to get counts
location_counts = pd.DataFrame(data)['location'].value_counts().reset_index()
category_counts = pd.DataFrame(data)['category'].value_counts().reset_index()

# Rename columns
location_counts.columns = ['Location', 'Count']
category_counts.columns = ['Category', 'Count']

# Exclude empty locations and categories
st.write("### Frequencies Graph")
st.write("Graph to show the frequencies of emergencies")
exclUnidentified = st.checkbox("Exclude Unidentified Results")
if exclUnidentified:
    location_counts = location_counts[location_counts['Location'] != 'unidentified']
    category_counts = category_counts[category_counts['Category'] != 'unidentified']
def wrap_labels(labels, width=20):
    return ['\n'.join(textwrap.wrap(l, width)) for l in labels]
# Get top 10 locations
topLoc_counts = location_counts.head(10)
topCat_counts = category_counts.head(5)
topLoc_counts['Location'] = wrap_labels(topLoc_counts['Location'], width=20)
topCat_counts['Category'] = wrap_labels(topCat_counts['Category'], width=20)
# Plot for top locations
plt.style.use('dark_background')
numofLoc = len(topLoc_counts)
figWidth = max(10, 15)
figHeight = max(4, numofLoc*0.8)
plt.figure(figsize=(figWidth, figHeight))
sns.set_context("talk")
ax1 = sns.barplot(topLoc_counts, y='Location', x='Count', palette='viridis')
for index, value in enumerate(topLoc_counts['Count']):
    ax1.text(value+0.02, index, f'{int(value)}', ha='left', va='center')
plt.title('Emergency frequencies by locations')
plt.xlabel('Frequency')
plt.ylabel('Location')
plt.xticks(np.arange(0, topLoc_counts['Count'].max() + 2, 1))
plt.yticks()
plt.tight_layout()

# Display plot for locations in Streamlit column 1
# col1, col2 = st.columns(2)
# with col1:
#     st.pyplot(fig)
with st.expander("View frequencies by locations graph"):
    st.pyplot(plt)
# Plot for top categories
plt.figure(figsize=(10, 10))
sns.set_context("talk")
numofCat = len(topCat_counts)
figHeight = max(4, numofCat*0.8)
plt.figure(figsize=(figWidth, figHeight))
ax2 = sns.barplot(topCat_counts, x='Count', y='Category', palette='viridis')
for index, value in enumerate(topCat_counts['Count']):
    ax2.text(value+0.02, index, f'{int(value)}', ha='left', va='center')
plt.title('Emergency frequencies by type')
plt.xlabel('Frequency')
plt.ylabel('Type')
plt.xticks(np.arange(0, topCat_counts['Count'].max() + 2, 1))
plt.yticks()
plt.tight_layout()

# with col2:
#     st.pyplot(plt)
with st.expander("View frequencies by types graph"):
    st.pyplot(plt)
unique_locations = sorted(list(set(entry['location'] for entry in data if entry['location'])))
unique_category = sorted(list(set(entry['category'] for entry in data if entry['category'])))
unique_years = sorted(list(set(entry['datetime'].year for entry in data)))

unique_locations.insert(0, "Show data by available location")
unique_category.insert(0, "Show data by available emergency type") 
st.write("### Data details")
# For location selection
selected_location = st.selectbox('Show data by location', unique_locations, key="location_select")
# Display filtered data table for location
if selected_location and selected_location != 'Select Location':
    filtered_data = maps.filter_data_by_location(selected_location)
    if filtered_data:
        # Convert filtered data to a DataFrame
        df = pd.DataFrame(filtered_data)
        st.write(f"### Showing Data for {selected_location}")
        # Create a multi-select for year selection with unique key
        selected_years = st.multiselect('Select Year', unique_years, default=unique_years, key="year_select_location")

        # Filter data by selected years
        filtered_data_by_year = [entry for entry in filtered_data if entry['datetime'].year in selected_years]
        df_by_year = pd.DataFrame(filtered_data_by_year)
        
        # Display the updated DataFrame based on year selection
        if df_by_year.empty:
            st.write('There\'s no data available (˶╹o╹˶)')
        else:
            st.dataframe(df_by_year, use_container_width=True, hide_index=True, column_config={"id":None})
    else:
        st.write('')

# For category selection
selected_category = st.selectbox('Show data by type', unique_category, key="category_select")
# Display filtered data table for category
if selected_category and selected_category != 'Select Type':
    filtered_data = maps.filter_data_by_category(selected_category)
    if filtered_data:
        # Convert filtered data to a DataFrame
        df = pd.DataFrame(filtered_data)
        st.write(f"### Showing Data for {selected_category}")
        # Create a multi-select for year selection with unique key
        selected_years = st.multiselect('Select Year', unique_years, default=unique_years, key="year_select_category")

        # Filter data by selected years
        filtered_data_by_year = [entry for entry in filtered_data if entry['datetime'].year in selected_years]
        df_by_year = pd.DataFrame(filtered_data_by_year)
        
        # Display the updated DataFrame based on year selection
        if df_by_year.empty:
            st.write('There\'s no data available (˶╹o╹˶)')
        else:
            st.dataframe(df_by_year, use_container_width=True, hide_index=True, column_config={"id":None})
    else:
        st.write('')