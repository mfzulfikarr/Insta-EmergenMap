import pandas as pd
import numpy as np
import os
curr_dir = os.path.dirname(__file__)
# Sort and convert the raw data to CSV
def sortData (folderRaw):
    fileList = [f for f in os.listdir(folderRaw) if f.endswith('.txt')]
    data = []
    for fileName in fileList:
        convertName = fileName.split('.')[0]
        convertName = convertName.replace('_', ' ')
        fileDate = pd.to_datetime(convertName, format='%Y-%m-%d %H-%M-%S %Z')
        fileDate_WIB = (fileDate + pd.DateOffset(hours=7)).tz_localize(None)
        with open(os.path.join(folderRaw, fileName), 'r', encoding='utf-8') as file:
            content = file.read()
            data.append([fileDate_WIB, content])
    dfRaw = pd.DataFrame(data, columns=['datetime', 'content'])
    return dfRaw
try:
    folderRaw = os.path.join(curr_dir, "../collection")
    if not os.path.exists(folderRaw):
        raise FileNotFoundError(f"Hmm, I can't find the {folderRaw} folder, make sure you put all the data inside collection folder. You may create one if it's not yet exist.\n\n"
                                "Sorry for the inconvenience (˶ᵕ︵ᵕ˶)")
    dfRaw = sortData(folderRaw)
    if not os.path.exists(os.path.join(curr_dir, '../Datasets')):
        os.makedirs(os.path.join(curr_dir, '../Datasets'))
    dfRaw.to_csv(os.path.join(curr_dir, '../Datasets/mergedData.csv'), index=False)
except:
    print(f"Hmm, There's an error. I suggest to check the {folderRaw} folder")