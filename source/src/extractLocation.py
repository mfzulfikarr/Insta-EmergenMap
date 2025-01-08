import pandas as pd
import numpy as np
import os
import re
from util.utils import TextUtils
utils = TextUtils()
curr_dir = os.path.dirname(__file__)
# Read all kinds of places and road names in South Jakarta (Collected with Overpass Turbo)
text_data = pd.read_csv(os.path.join(curr_dir, '../Datasets/categorizedData.csv'))
building_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselbuildingname2.xlsx'))
bus_station_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselbusstationname2.xlsx'))
train_station_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakseltrainstationname2.xlsx'))
cemetery_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselcemeteryname2.xlsx'))
hospital_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselhospitalname2.xlsx'))
mall_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselmallname2.xlsx'))
office_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselofficename2.xlsx'))
residential_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselresidentialname2.xlsx'))
kelurahan_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselkelurahanname2.xlsx'))
street_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselstreetname2.xlsx'))
highway_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakselhighwayname2.xlsx'))
overunder_data = pd.read_excel(os.path.join(curr_dir, '../placenames/alljakseloverundername2.xlsx'))
text_data = text_data[text_data['isinfo'] != 'not informative']
# Function to sort data by length of 'name' and 'alt_name' in descending order
def sort_by_length(data):
    data['name'] = data['name'].fillna('')
    data['alt_name'] = data['alt_name'].fillna('')
    data['name_length'] = data['name'].apply(len)
    data['alt_name_length'] = data['alt_name'].apply(len)
    data = data.sort_values(by=['name_length', 'alt_name_length'], ascending=False)
    return data
# Sort all data by length of names
building_data = sort_by_length(building_data)
bus_station_data = sort_by_length(bus_station_data)
train_station_data = sort_by_length(train_station_data)
cemetery_data = sort_by_length(cemetery_data)
hospital_data = sort_by_length(hospital_data)
mall_data = sort_by_length(mall_data)
office_data = sort_by_length(office_data)
residential_data = sort_by_length(residential_data)
kelurahan_data = sort_by_length(kelurahan_data)
street_data = sort_by_length(street_data)
highway_data = sort_by_length(highway_data)
overunder_data = sort_by_length(overunder_data)
# Function to find the location
def find_location(text):
    # Define the priority order (A building location is more accurate than just the street names)
    data_files = [
        building_data, office_data, residential_data, overunder_data, highway_data, mall_data,
        bus_station_data, train_station_data, hospital_data, cemetery_data, street_data, kelurahan_data]
    text = text.lower() # Convert text to lowercase for case-insensitive matching
    # Check for each category in order of priority
    for data in data_files:
        for _, row in data.iterrows():
            name = row['name'].lower()
            alt_name = row['alt_name'].lower() if pd.notna(row['alt_name']) else None
            if re.search(rf'\b{name}\b', text):
                return row['name']
            elif alt_name and re.search(rf'\b{alt_name}\b', text):
                return row['alt_name']
    # Check for streets if no other location name was found and no words that resemble an object location for failsafe
    notstreetwords = ['kawasan', 'daerah', 'dekat', 'depan', 'belakang', 'sebelah']
    if not any(word in text for word in notstreetwords):
        for data in [street_data, highway_data, overunder_data]:
            for _, row in data.iterrows():
                name = row['name'].lower()
                alt_name = row['alt_name'].lower() if pd.notna(row['alt_name']) else None
                
                if re.search(rf'\b{name}\b', text) or (alt_name and re.search(rf'\b{alt_name}\b', text)):
                    return row['name']
    return None
text_data['location'] = text_data['textClean'].apply(find_location)
subset = ['category', 'location']
text_data.loc[:, subset] = text_data.loc[:, subset].fillna('unidentified')
text_data.to_excel(os.path.join(curr_dir, '../Datasets/extractedData.xlsx'), index=False)
text_data.to_csv(os.path.join(curr_dir, '../Datasets/extractedData.csv'), index=False)