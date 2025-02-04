# Insta-EmergenMap
Shows map of recent emergency situations in South Jakarta from Instagram with Instaloader
[![Map](https://raw.githubusercontent.com/mfzulfikarr/Insta-EmergenMap/refs/heads/main/img/map.png)]
## Notice
THIS PROJECT IS INTENDED SOLELY FOR PERSONAL OR NON-COMMERCIAL USE.

Any activities involving commercial use are strictly prohibited.

This project may only be used for educational purposes only WITH THE AGREEMENT BETWEEN USER AND THE ACCOUNT OWNER.
## Table of Contents
- [Notice](#notice) | [Features](#features) | [Requirements](#requirements) | [Installation](#installation)
- [Getting Started](#getting-started) | [Run the Project](#run-the-project)
- [Known Bugs](#known-bugs) | [Upcoming Features and WIP BugFix](#upcoming-features-and-wip-bugfix)
- [LICENSE](#license)
## Features
1. Auto Data Collection and Processing.
2. Shows an estimate location by highlighting the streets or circling the closest building or point of interest from the exact emergency location.
3. Data filtering by year and/or by emergency types.
4. Graph to show the types of emergencies that occur most frequently and which locations experience emergencies most frequently.
5. Tabel of original text data to help with each emergency types or locations context.
## Requirements
To run this project, ensure to have the following installed:
### 1. Python and libraries
- **Python**: Version 3.9 or higher.
- **XAMPP**: Version 3.3.0 or higher.
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

## Installation
### 1. Clone this repository
```bash
git clone https://github.com/mfzulfikarr/Insta-EmergenMap.git
```

### 2. Use pip to automatically install the libraries:
```bash
pip install -r requirements.txt
```

## Getting Started
The captions or text data should be in a form of .txt with its date and time including timezone as the filename with the format of yyyy-mm-dd_hh-mm-ss_UTC (For Example: 2024-06-17_01-01-05_UTC.txt).

The map could only be used if the text data is already processed or stored in the database (at least one processed data is in the database). Use the Get New Data menu in order to collect or process the data.
### Run the project
Run XAMPP, start Apache and SQL

Run the start.py with streamlit to start the project
```shell
streamlit run start.py
```
If no data are available yet, head to the Get New Data menu to collect or process the data.

Further guides available in the project start pages.

## Known Bugs
1. Buttons inside the streamlit dialog for data confirmation are able to be clicked multiple times which causing the project to spitting bars in a form of error logs.
2. Same for the get new data button it can be clicked multiple times and makes the project spitting some error logs.
3. The progress bar is stuck to the top of the page.
4. The tag filter button overlaps when clicking for the first filter.
5. The graph can be really big or really small randomly.

## Upcoming Features and WIP BugFix
1. Clickable marker (still trying to find a workaround for streamlit-folium map).
2. Safer way to show confirmation dialog.
3. More stronger and accurate models.
4. Reinforcement Learning from Human Feedback (RLHF).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
