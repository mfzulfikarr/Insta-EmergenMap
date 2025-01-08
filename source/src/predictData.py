import pandas as pd
import numpy as np
import pickle
import os
import sys
from util.utils import TextUtils
utils = TextUtils()
curr_dir = os.path.dirname(__file__)
dfProc = pd.read_csv(os.path.join(curr_dir, '../Datasets/cleanData.csv'))
duplicates = dfProc[dfProc.duplicated(subset='content', keep=False)]
if not duplicates.empty:
    dfProc = dfProc.drop_duplicates(subset='content', keep='first')
dfProc['textToken'] = dfProc['textToken'].apply(utils.removeSymbols)
dfProc['textToken'] = dfProc['textToken'].apply(utils.removeSpaces)
dfPredict = dfProc.copy()
# Reminder that the texttoken (tokenized text) column is required ;)
if 'textToken' not in dfPredict.columns:
    raise ValueError("The input CSV file must contain a 'textToken' column.")
with open(os.path.join(curr_dir, 'util/models/nb_model_fix.pkl'), 'rb') as tempfile:
    NBModel = pickle.load(tempfile)
with open(os.path.join(curr_dir, 'util/models/tfidf_model.pkl'), 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)
new_data_tfidf = vectorizer.transform(dfPredict['textToken'])
predictions = NBModel.predict(new_data_tfidf)
dfPredict['isinfo'] = predictions # Add the predictions to the DataFrame
dfPredict['isinfo'] = dfPredict['isinfo'].map({1: 'informative', 0: 'not informative'})
dfPredict.to_csv(os.path.join(curr_dir, '../Datasets/predictedData.csv'), index=False)
dfPredict.to_excel(os.path.join(curr_dir, '../Datasets/predictedData.csv').replace('.csv', '.xlsx'), index=False)