import pandas as pd
import numpy as np
import os
import re
from util.utils import TextUtils
utils = TextUtils()
curr_dir = os.path.dirname(__file__)
dfPredict = pd.read_csv(os.path.join(curr_dir, '../Datasets/predictedData.csv'))
# Define disaster patterns with word boundaries
disaster_patterns = {
    "flood": r'\b(?:banjir|rendam)\b',
    "earthquake": r'\b(?:gempa|getar|guncang)\b',
    "fire": r'\b(?:bakar|hangus|bara)\b',
    "landslide": r'\b(?:longsor)\b',
    "clash": r'\b(?:tawuran|tikai|tawur|rusuh|bentrok)\b',
    "fallen tree": r'\b(?:pohon tumbang|tumbang)\b',
    "protest": r'\b(?:demo|demonstrasi|ricuh|unjuk|unjuk rasa)\b',
    "accident": r'\b(?:kecelakaan|celaka|laka lantas|tabrak|senggol|timpa|tumpah oli|tumpah minyak|guling|jeblos|patah as)\b'
}
# Compile the disaster patterns
compiled_disaster_patterns = {category: re.compile(pattern, flags=re.IGNORECASE) for category, pattern in disaster_patterns.items()}
dfCategory = dfPredict.copy() # Load the new data CSV
# Add an untokenized column by joining the tokens back into a single string
dfCategory['untokenized'] = dfCategory['textToken'].apply(utils.removeSymbols).apply(utils.removeSpaces)
# Function to apply disaster patterns and assign categories
def assign_category(row):
    combined_text = row['untokenized'] + ' ' + row['textClean']
    for category, pattern in compiled_disaster_patterns.items():
        if pattern.search(combined_text):
            return category
    return 'unidentified'
# Apply the function to assign categories based on both columns
dfCategory['category'] = dfCategory.apply(assign_category, axis=1)
dfCategory = dfCategory.drop(columns=['untokenized', 'textToken']) #<-- Don't need this two to reduce the file size
dfCategory.to_csv(os.path.join(curr_dir, '../Datasets/categorizedData.csv'), index=False)
dfCategory.to_excel(os.path.join(curr_dir, '../Datasets/categorizedData.xlsx'), index=False)