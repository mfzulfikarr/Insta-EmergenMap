import re
import os
import pandas as pd
# This code is only to helps with the labeling, thats all
# Function to read text files and return a set of lines stripped of whitespace
def read_txt(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return set(line.strip() for line in file)
# Function to clean text by removing symbols
def removeSymbols(text):
    clnString = re.sub(r'\n+', ' ', text)  # Remove newlines (\n)
    clnString = re.sub(r"[$%#@*']", "", clnString)
    clnString = re.sub(r"[^ a-zA-Z0-9=-]", " ", clnString)  # Remove symbols (.,<>\/, etc.)
    clnString = re.sub(r'-', ' ', clnString)
    return clnString
# Function to remove extra spaces
def removeSpaces(text):
    removeSpc = re.sub(r"\s+", " ", text).strip()
    return removeSpc
# Function for tokenization
def tokenization(text):
    tokens = text.split()
    return tokens
# Read the CSV file into a DataFrame
df = pd.read_excel('./Datasets/customizedDatanew.xlsx')
# Clean and tokenize text data
df['textToken'] = df['textToken'].apply(removeSymbols)
df['textToken'] = df['textToken'].apply(removeSpaces)
df['textToken'] = df['textToken'].apply(tokenization)
# Define dictionaries of disaster-related patterns and unknown patterns
disaster_patterns = {
    "banjir": r'\b(?:banjir|rendam)\b',
    "gempa": r'\b(?:gempa|getar|guncang)\b',
    "kebakaran": r'\b(?:bakar|hangus|bara)\b',
    "longsor": r'\b(?:longsor)\b',
    "bentrok": r'\b(?:tawuran|tikai|tawur|rusuh|bentrok)\b',
    "pohon tumbang": r'\b(?:pohon tumbang|tumbang)\b',
    "demonstrasi": r'\b(?:demo|demonstrasi|ricuh|unjuk|unjuk rasa)\b',
    "kecelakaan": r'\b(?:kecelakaan|celaka|laka lantas|tabrak|senggol|timpa|tumpah oli|tumpah minyak|guling|jeblos|patah as)\b'
}

unknown_patterns = {
    "not target": r'\b(?:tidak ada korban|simulasi|pasca|tilang|cekcok|kelahi|pembunuhan|bunuh|potong tubuh|mutilasi|cititex|jual|coba|gusur|curi|curanmor|jambret|begal|maling|rampok|jalur tol|tangan|viralkan|tindak|viral|tugas|tangkap|gagal|ungkap|tinju)\b'
}

impact_patterns = {
    "korban_jiwa": r'\b(?:korban|jiwa|tewas|meninggal|mati|luka|cedera|luka|tinggal)\b',
    "kerusakan_lingkungan": r'\b(?:lingkungan|rusak|hancur|porak|poranda|lumpur|kikis|gundul)\b',
    "kerugian_harta": r'\b(?:harta|parah|rugi|hilang|ekonomi)\b',
    "dampak_psikologis": r'\b(?:trauma|kejut|takut|stress|tekan|panik|shock)\b'
}

# Additional patterns to indicate single losses
single_loss_patterns = r'\b(?:sebuah|seorang|tunggal)\b'

# Compile regex patterns for disaster, unknown, impact, and single loss words
disaster_pattern = re.compile('|'.join(disaster_patterns.values()), flags=re.IGNORECASE)
unknown_pattern = re.compile('|'.join(unknown_patterns.values()), flags=re.IGNORECASE)
impact_pattern = re.compile('|'.join(impact_patterns.values()), flags=re.IGNORECASE)
single_loss_pattern = re.compile(single_loss_patterns, flags=re.IGNORECASE)

# Function to check for impact-related words
def has_impact(text):
    return any(re.search(impact_pattern, word) for word in text)

# Function to categorize text with additional filters
def categorize_text(row):
    text_str = ' '.join(row['textToken']) + ' ' + row['textClean']
                    
    # Check for unknown patterns
    if re.search(unknown_pattern, text_str):
        return 'not informative'
    
    # Check for single loss patterns (only for specific disaster types)
    if re.search(single_loss_pattern, text_str):
        for disaster in ["kebakaran", "longsor", "gempa"]:
            if re.search(disaster_patterns[disaster], text_str):
                break
        else:
            return 'not informative'
    
    for disaster, pattern in disaster_patterns.items():
        if re.search(pattern, text_str):
            if disaster in ["banjir", "bentrok", "demonstrasi", "pohon tumbang"]:
                return 'informative'
            elif disaster in ["kebakaran", "longsor", "gempa", "kecelakaan"]:
                if re.search(r'\b(?:korban jiwa|meninggal dunia|meninggal|tewas|md|korban|jenazah)\b', text_str):
                    return 'informative'
                else:
                    return 'not informative'
            else:
                if has_impact(text_str):
                    return 'informative'
                else:
                    return 'not informative'
    
    return 'not informative'

# Iterate through each row of the DataFrame
# for index, row in df.iterrows():
#     text_str = ' '.join(row['textToken']) + ' ' + row['textClean']
#     print(f"Text before categorization:\n{text_str}\n")

# Apply categorization function
df['isinfo'] = df.apply(categorize_text, axis=1)

# Save results to a single CSV file
df.to_csv('./Datasets/customizedDatanew.csv', index=False)
df.to_excel('./Datasets/customizedDatanew.xlsx', index=False)