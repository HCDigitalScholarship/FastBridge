import pandas as pd
import numpy as np
import os

path = os.getcwd()
df = pd.read_csv(path + '/tibullus_textstructurenode_202002111032.csv')
primary_index = ['0']
secondary_index = ['0']
subsection_index_count = [-1]

def create_subsection_label(row):
    if row['subsection_level'] == 0:
        return np.NaN
    elif row['subsection_level'] == 1:
        primary_index[0] = str(row['subsection_id'])
        return primary_index[0]
    elif row['subsection_level'] == 2:
        secondary_index[0] = str(row['subsection_id'])
        return primary_index[0] + "." + secondary_index[0]
    elif row['subsection_level'] == 3:
        return primary_index[0] + "." + secondary_index[0] + '.' + str(row['subsection_id'])

def create_subsection_index(row):
    print(str(row['subsection_label']).split("."))
    print(type(row['subsection_label']))
    if len(str(row['subsection_label']).split(".")) == 3:
        subsection_index_count[0] += 1
        return int(subsection_index_count[0])
    else:
        return np.NaN

# if retrieving subsection_label == "1", return all subsection_label LIKE "1%"

df['subsection_label'] = df.apply(create_subsection_label, axis=1)
df['subsection_index'] = df.apply(create_subsection_index, axis=1)
df = df.drop(['new_least_mindiv', 'new_subsection_id'], axis=1)




print(df)
