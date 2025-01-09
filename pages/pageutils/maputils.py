import pandas as pd
import json
import requests
import time
import streamlit as st
import folium
from streamlit_folium import folium_static, st_folium
from folium.plugins import TagFilterButton
from geopy.distance import geodesic
import mysql.connector
from mysql.connector import Error, pooling
import re
import numpy as np
import os
curr_dir = os.path.dirname(os.path.dirname(__file__))
if not os.path.exists(os.path.join(curr_dir, "../cache")):
    os.makedirs(os.path.join(curr_dir, "../cache"))
@st.cache_data
# Save the updated results to a local JSON file
def save_overpassResults(overpass_results):
    with open(os.path.join(curr_dir, "../cache/overpass_results.json"), 'w') as f:
        json.dump(overpass_results, f)
def load_overpassResults():
    try:
        with open(os.path.join(curr_dir, "../cache/overpass_results.json")) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@st.cache_data(ttl=86400)
def overpass_search(location):
    if not location:
        return None
    if "jalan" in location.lower():
        overpass_query = f"""
            [out:json][timeout:2500];
            area["name"="Jakarta Selatan"]->.searchArea;
            (
            way["highway"!~"living_street|residential|tertiary|steps"]["name"~"{location}", i](area.searchArea);
            way["highway"!~"living_street|residential|tertiary|steps"]["alt_name"~"{location}", i](area.searchArea);
            );
            out body geom;
        """
    else:
        overpass_query = f"""
            [out:json][timeout:2500];
            area["name"="Jakarta Selatan"]->.searchArea;
            (
            way["name"~"{location}", i]["railway"!~"rail|construction"]["landuse"!~"railway"]["highway"!~"."]["building"!~"yes"]["amenity"!~"."]["power"!~"."](area.searchArea);
            way["alt_name"~"{location}", i]["railway"!~"rail|construction"]["landuse"!~"railway"]["highway"!~"."]["building"!~"yes"]["amenity"!~"."]["power"!~"."](area.searchArea);
            
            node["name"~"{location}", i]["railway"!~"rail|construction"]["landuse"!~"railway"]["highway"!~"."]["building"!~"yes"]["amenity"!~"."]["power"!~"."](area.searchArea);
            node["alt_name"~"{location}", i]["railway"!~"rail|construction"]["landuse"!~"railway"]["highway"!~"."]["building"!~"yes"]["amenity"!~"."]["power"!~"."](area.searchArea);
            
            way["amenity"~"bus_station|marketplace"]["name"~"{location}", i](area.searchArea);
            way["amenity"~"bus_station|marketplace"]["alt_name"~"{location}", i](area.searchArea);

            node["amenity"~"bus_station|marketplace"]["name"~"{location}", i](area.searchArea);
            node["amenity"~"bus_station|marketplace"]["alt_name"~"{location}", i](area.searchArea);

            way["shop"~"mall"]["name"~"{location}", i](area.searchArea);
            way["shop"~"mall"]["alt_name"~"{location}", i](area.searchArea);
            
            node["shop"~"mall"]["name"~"{location}", i](area.searchArea);
            node["shop"~"mall"]["alt_name"~"{location}", i](area.searchArea);
            );
            out body geom;
        """
    retries = 3
    delay = 5
    for attempt in range(retries):
        try:
            response = requests.get(f"https://overpass-api.de/api/interpreter?data={requests.utils.quote(overpass_query)}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                st.warning(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                st.error(f"HTTP error occurred: {e}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from Overpass API: {e}")
            return None
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON response: {e}")
            st.write("Response content:", response.content)
            return None
    st.error("Exceeded maximum retries.") #<-- Still experimenting on this one :)
    return None

class MapUtils:
    def __init__(self):
        self.map_center = [-6.2771059771128295, 106.80883650021909] # Move map to South Jakarta
        self.map_maxLat, self.map_minLat = -6.177980, -6.394432
        self.map_maxLon, self.map_minLon = 106.877121, 106.732214
        self.data = None
        self.location_text_count = {}
        self.location_year_text_count = {}
        self.location_categories = {}
        try:
            self.dbPool=mysql.connector.pooling.MySQLConnectionPool(
                pool_name="strlitPool",
                pool_size=10,
                host="localhost",
                user="root",
                password="",
                database="db_strlit"
            )
        except Error as e:
            st.error("Failed to create connection pool. Check if xampp is started correctly by pressing the start button on the Apache and MySQL options.\n\n"
                     f"Details: {e}")
    def db_connection(self):
        try:
            return self.dbPool.get_connection()
        except Error as e:
            raise RuntimeError(f'Something went wrong, unable to get a connection from the pool. Details: {e}')
    def load_data_from_db(self):
        conn = None
        cursor = None
        try:
            conn = self.db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM finaldatanew")
            data = cursor.fetchall()
            return data
        except Error as e:
            st.error(f"Oops! an error occured. Unable to find the database.\n\n"
                     f"You might wanna visit the Get New Data menu.\n\n"
                     f"Details: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    def get_data(self):
        if self.data is None:
            self.data = self.load_data_from_db()
        return self.data
    def extract_valid_location(self, entry):
        if entry['location'] and entry['location'] != '-':
            return entry['location']
        return None
    # Map Graph Calculation
    def calculate_centroid(self, latlngs):
        lat_sum = sum(point[0] for point in latlngs)
        lon_sum = sum(point[1] for point in latlngs)
        return [lat_sum / len(latlngs), lon_sum / len(latlngs)]
    def closest_point_on_line(self, latlngs, point):
        closest_point = latlngs[0]
        min_distance = geodesic(point, closest_point).meters
        for latlng in latlngs:
            distance = geodesic(point, latlng).meters
            if distance < min_distance:
                min_distance = distance
                closest_point = latlng
        return closest_point
    def create_map(self):
        if 'map' not in st.session_state:
            m = folium.Map(max_bounds=True,
                           location=self.map_center,
                           max_lat=self.map_maxLat,
                           min_lat=self.map_minLat,
                           max_lon=self.map_maxLon,
                           min_lon=self.map_minLon,
                           max_zoom=19,
                           min_zoom=12,
                           zoom_start=12)
            st.session_state.map = m  # Save the map in the session state
        return st.session_state.map
    def show_map(self):
        try:
            m = self.create_map()  # Create the map
            overpass_results = load_overpassResults()  # Load cached results
            years = set()
            location_categories_set = set()
            for entry in self.get_data():
                location = self.extract_valid_location(entry)
                year = entry['datetime'].year
                category = entry['category']

                if location:
                    # Update text count
                    if location not in self.location_text_count:
                        self.location_text_count[location] = 0
                    self.location_text_count[location] += 1

                    # Update year text count
                    if location not in self.location_year_text_count:
                        self.location_year_text_count[location] = {}
                    if year not in self.location_year_text_count[location]:
                        self.location_year_text_count[location][year] = 0
                    self.location_year_text_count[location][year] += 1

                    # Update categories
                    if location not in self.location_categories:
                        self.location_categories[location] = set()
                    self.location_categories[location].add(category)

                    # Add to years and categories sets
                    years.add(str(year))
                    location_categories_set.update(self.location_categories[location])

                    # Check if the location exists in the cache
                    if location in overpass_results:
                        search_result = overpass_results[location]
                        print("Searching location in cache...")
                    else:
                        # Perform online search and update the cache
                        search_result = overpass_search(location)
                        if search_result:
                            overpass_results[location] = search_result
                            save_overpassResults({location: search_result})

                    # Proceed to process the search result
                    if search_result and search_result.get('elements'):
                        all_latlngs = []
                        is_highway_or_railway = False

                        for element in search_result['elements']:
                            if 'geometry' in element:
                                latlngs = [[point['lat'], point['lon']] for point in element['geometry']]
                                all_latlngs.extend(latlngs)

                                if element['type'] == 'way' and ('highway' in element['tags'] or 'railway' in element['tags']):
                                    folium.PolyLine(latlngs, color='blue').add_to(m)
                                    is_highway_or_railway = True

                        if all_latlngs:
                            centroid = self.calculate_centroid(all_latlngs)
                            marker_position = self.closest_point_on_line(all_latlngs, centroid) if is_highway_or_railway else centroid

                            # Calculate total text count for a location
                            total_text_count = self.location_text_count.get(location, 0)

                            # Get list of categories for a location
                            location_category_list = ", ".join(self.location_categories.get(location, set()))

                            # Update popup to show location name, total text count, year, and categories
                            popup_content = (f'<b>{location}</b><br>Total Emergencies: {total_text_count}<br>'
                                            f'Year: {year}<br>Type: {location_category_list}')
                            popup = folium.Popup(popup_content, max_width=300)
                            marker = folium.Marker(marker_position, popup=popup, tags=[str(year)] + list(self.location_categories.get(location, set())))
                            marker.add_to(m)

                            if not is_highway_or_railway:
                                folium.Circle(marker_position, radius=500, color='blue', fill_opacity=0.2).add_to(m)
                            # Borders
                            # folium.CircleMarker([self.map_maxLat, self.map_minLon], tooltip="Upper Left Corner").add_to(m)
                            # folium.CircleMarker([self.map_minLat, self.map_minLon], tooltip="Lower Left Corner").add_to(m)
                            # folium.CircleMarker([self.map_minLat, self.map_maxLon], tooltip="Lower Right Corner").add_to(m)
                            # folium.CircleMarker([self.map_maxLat, self.map_maxLon], tooltip="Upper Right Corner").add_to(m)
                            folium.Rectangle(bounds=[[self.map_minLat, self.map_minLon],[self.map_maxLat, self.map_maxLon]],
                                            fill=False,
                                            popup="Rough boundaries of current region",
                                            weight=2).add_to(m)
            # Sort categories for TagFilterButton
            sorted_years = sorted(years, key=lambda x: int(x))
            sorted_location_categories = sorted(location_categories_set)

            # Add TagFilterButton only once
            if 'tag_filter_button_added' not in st.session_state:
                TagFilterButton(sorted_years).add_to(m)
                st.session_state['tag_filter_button_added'] = True
            
            if 'category_tag_filter_button_added' not in st.session_state:
                TagFilterButton(sorted_location_categories).add_to(m)
                st.session_state['category_tag_filter_button_added'] = True

            # Save the map to an HTML file
            m.save(os.path.join(curr_dir, "../cache/map.html"))
            # Read the HTML file
            with open(os.path.join(curr_dir, "../cache/map.html")) as inf:
                txt = inf.read()

            # Find all the marker names given by folium
            markers = re.findall(r'\bmarker_\w+', txt)

            # Add hover behavior to each marker
            for marker in markers:
                txt = txt.replace(
                    f'{marker}.bindPopup',
                    f"""
                    {marker}.on('mouseover', function (e) {{
                        this.openPopup();
                    }});
                    {marker}.on('mouseout', function (e) {{
                        this.closePopup();
                    }});
                    {marker}.bindPopup
                    """
                )

            # Save the modified HTML to a new file
            with open(os.path.join(curr_dir, "../cache/map.html"), "w") as outf:
                outf.write(txt)
            # Read the modified HTML
            with open(os.path.join(curr_dir, "../cache/map.html"), "r") as f:
                html = f.read()

            # Display the map with full width
            st.components.v1.html(f"""
            <div style="width: 100%; height: 500px;">
                {html}
            </div>
            """, height=500)
        except Exception as e:
            st.error("Oops! an unexpected error occured. You might wanna do this steps: \n\n"
                    "1. Make sure the data is available. You can get or process some data on the Get New Data Menu\n"
                    "2. Check if xampp is started correctly by pressing the start button on the Apache and MySQL options\n"
                    "3. Check your network connection, make sure it's stable\n"
                    "4. Reload the page or restart the app\n\n"
                    "Sorry for the inconvenience (˶ᵕ︵ᵕ˶)\n\n"
                    f"Details: {e}")
    def filter_data_by_location(self, location):
        try:
            filtered_loc = [entry for entry in self.get_data() if entry['location'] == location]
            return filtered_loc
        except Exception as e:
            st.error("An error occured, sorry for the inconvenience :(\n\n"
                    f"Details: {e}")
    def filter_data_by_category(self, category):
        try:
            filtered_cat = [entry for entry in self.get_data() if entry['category'] == category]
            return filtered_cat
        except Exception as e:
            st.error("An error occured, sorry for the inconvenience :(\n\n"
                    f"Details: {e}")