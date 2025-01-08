from splittingData import train_test_split
from tfidfCalc import SimpleTfidfVectorizer
from trainNB import SimpleMultinomialNB
from textAugment import TextAugment
from accuracyScore import accuracy_score, classification_report
from sklearn.utils import resample
import pandas as pd
import numpy as np
import re
import pickle
import streamlit as st
def removeSymbols(text):
    # new_string =  re.sub(r"[^\w\s]", "", text)
    cln_string = re.sub(r'\n+', ' ', text) #remove newlines (\n)
    cln_string = re.sub(r"[$%#@*']", "", cln_string)
    cln_string = re.sub(r"[^ a-zA-Z0-9=-]", " ", cln_string) #remove symbols(.,<>\/,etc.)
    cln_string = re.sub(r'-', ' ', cln_string)
    return cln_string
def removeSpaces(text):
    # new_string =  re.sub(r"[^\w\s]", "", text)
    spc_remove = re.sub(r"\s+", " ", text).strip()
    return spc_remove
def calculate_confusion_matrix(y_true, y_pred):
    labels = ['not informative', 'informative']
    conv_label = {0: 'not informative', 1: 'informative'}
    matrix = np.zeros((len(labels), len(labels)), dtype=int)
    for true_label, pred_label in zip(y_true, y_pred):
        true_index = labels.index(conv_label[true_label])
        pred_index = labels.index(conv_label[pred_label])
        matrix[true_index, pred_index] += 1
    matrix_df = pd.DataFrame(matrix, index=labels, columns=labels)
    return matrix_df

dfRaw = pd.read_excel('./Datasets/customizedDatanew.xlsx')
df = dfRaw.copy()
duplicates = df[df.duplicated(subset='content', keep=False)]
if not duplicates.empty:
    df = df.drop_duplicates(subset='content', keep='first')
df['textToken'] = df['textToken'].apply(removeSymbols)
df['textToken'] = df['textToken'].apply(removeSpaces)
df['isinfo'] = df['isinfo'].map({'informative': 1, 'not informative': 0})
class_counts = df['isinfo'].value_counts()
majority_class = class_counts.idxmax()
minority_class = class_counts.idxmin()
dfFix = df.copy()
X = dfFix['textToken']
y = dfFix['isinfo']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

train_df = pd.DataFrame({'textToken': X_train, 'isinfo': y_train})
df_majority_train = train_df[train_df['isinfo'] == majority_class]
df_minority_train = train_df[train_df['isinfo'] == minority_class]
num_aug = round((len(df_majority_train)-len(df_minority_train))/len(df_minority_train))  # Initial number of augmentations
augmentText = TextAugment(alpha=0.3, num_aug=num_aug, random_state=110)
while True:
    augmented_rows = []
    for index, row in df_minority_train.iterrows():
        augmented_texts = augmentText.augment_text(row['textToken'])
        for text in augmented_texts:
            augmented_rows.append({'textToken': text, 'isinfo': row['isinfo']})
    df_minority_augmented_train = pd.DataFrame(augmented_rows)
    df_balanced_train = pd.concat([df_majority_train, df_minority_train, df_minority_augmented_train])
    majority_count = df_balanced_train[df_balanced_train['isinfo'] == majority_class].shape[0]
    minority_count = df_balanced_train[df_balanced_train['isinfo'] == minority_class].shape[0]
    if minority_count > majority_count:
        # Calculate then remove excess rows in minority
        diff = minority_count - majority_count
        df_minority_augmented_train = df_minority_augmented_train.iloc[:-diff] #<-- Remove excess rows from augmented minority here
        break # Break out of loop, classes are balanced
    else:
        num_aug += 1
        augmentText = TextAugment(alpha=0.3, num_aug=num_aug, random_state=110)
# Combine majority class with oversampled minority class in the training data
df_balanced_train = pd.concat([df_majority_train, df_minority_train, df_minority_augmented_train])
dfBalancedTrain = df_balanced_train.sample(frac=1, random_state=42).reset_index(drop=True) #<-- Shuffle the data
X_train = dfBalancedTrain['textToken']
y_train = dfBalancedTrain['isinfo']

train_df.to_csv('./Datasets/train_data.csv', index=False)
test_df = pd.DataFrame({'textToken': X_test, 'isinfo': y_test})
test_df.to_csv('./Datasets/test_data.csv', index=False)
train_df.to_excel('./Datasets/train_data.xlsx', index=False)
test_df.to_excel('./Datasets/test_data.xlsx', index=False)

vectorizer = SimpleTfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

modelNB = SimpleMultinomialNB()
modelNB.fit(X_train_vec, y_train)
predictionsNB = modelNB.predict(X_test_vec)

accNB = accuracy_score(y_test, predictionsNB)
reportNB = classification_report(y_test, predictionsNB)

print(f"Accuracy: Naive Bayes {accNB}")
print("Classification Report: Naive Bayes")
print(reportNB)

conf_matrixNB = calculate_confusion_matrix(y_test, predictionsNB)
print("Confusion Matrix:")
print(conf_matrixNB)
# Save the results
results_nb = pd.DataFrame({
    'textToken': X_test,
    'actual_label': y_test,
    'predicted_label_nb': predictionsNB
})
results_nb.to_csv('./Datasets/results_nb2.csv', index=False)
results_nb.to_excel('./Datasets/results_nb2.xlsx', index=False)
# Save the TF-IDF vectors
tfidf_train = pd.DataFrame({'textToken': X_train, 'tfidf': X_train_vec})
tfidf_test = pd.DataFrame({'textToken': X_test, 'tfidf': X_test_vec})
tfidf_train.to_csv('./Datasets/train_tfidf.csv', index=False)
tfidf_train.to_excel('./Datasets/train_tfidf.xlsx', index=False)
tfidf_test.to_csv('./Datasets/test_tfidf.csv', index=False)
tfidf_test.to_excel('./Datasets/test_tfidf.xlsx', index=False)
# Save the model to a file
model_name=['nb_model_fix', 'tfidf_model']
model_var=[modelNB, vectorizer]
for names, models in zip(model_name, model_var):
    with open(f'{names}.pkl', 'wb') as tempfile:
        pickle.dump(models, tempfile)
print("\nModel Berhasil Disimpan")
