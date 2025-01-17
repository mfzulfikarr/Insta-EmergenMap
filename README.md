# Insta-EmergenMap
Shows map of recent emergency situations in South Jakarta from Instagram with Instaloader

## Notice
THIS PROJECT IS INTENDED SOLELY FOR PERSONAL OR NON-COMMERCIAL USE.

Any activities involving commercial use are strictly prohibited.

This project may only be used for educational purposes only WITH THE AGREEMENT BETWEEN USER AND THE ACCOUNT OWNER.

## Requirements
To run this project, ensure to have the following installed:
### 1. Python and libraries
- **Python**: Version 3.9 or higher.
- **Python Libraries** (automatically installed via `requirements.txt`):
  - `streamlit 1.40.1 or higher`
  - `pandas`
  - `seaborn`
  - `numpy`
  - `mysql-connector-python`
  - `folium`
  - `geopy`
  - `nltk`
  - `Sastrawi`
  - `instaloader`
  - `sklearn`
  - `dill`

Use pip to automatically install the libraries:
```bash
pip install -r requirements.txt
```

## Getting Started
The captions or text data should be in a form of .txt with its date and time including timezone as the filename with the format of yyyy-mm-dd_hh-mm-ss_UTC (For Example: 2024-06-17_01-01-05_UTC.txt)
## How to use
run the streamlit from the shell to start it
```shell
streamlit run start.py
```
The map could only be used if the text data is already processed or stored in the database.

Use the Get New Data menu in order to collect or process the data.

The map will be able to be used if there's at least one processed data in the database.

A graph and details of the data is provided below the map.
