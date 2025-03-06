#Commented out for now
"""

import os
import json
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from utils import storage
from io import StringIO
from data_cleaning_version3 import clean_data_ev3
from data_cleaning_version3 import clean_data_ev2

encoders = {}


# luetaan dataa ja tehdään tauluja (lisää myös koodaus)
def clean_data():
    #luetaan data (poistettu yliopisto)
    dir = os.path.dirname(__file__)
    filename = "489-tampere-autumn 2024.json"
    location = os.path.join(dir, filename)
    bronze_file = open(location, encoding='utf8')
    bronze_data = json.load(bronze_file)
    bronze_file.close()

    if not bronze_data:
        print("ERROR: Failed to load data.")
        return None

    official_fields = ['Performing arts','Visual arts', 'History', 'Languages and literature', 'Law','Philosophy', 'Theology',
                       'Anthropology','Economics','Geography','Political science','Psychology','Sociology','Social Work',
                       'Biology','Chemistry','Earth science','Space sciences','Physics','Computer Science','Mathematics','Business',
                       'Engineering and technology','Medicine and health'
                       ]

    # tehdään opiskelijoiden talu ja muokataan sitä paremmaks
    temp = json.dumps(bronze_data['students'])
    df = pd.read_json(StringIO(temp))
    dfstu= df[['id', 'homeUniversity','attendingUniversity', 'degreeLevelType', 'studiesField']]
    dfstu.loc[dfstu["attendingUniversity"].notna(), "homeUniversity"] = dfstu['attendingUniversity']
    dfstu.loc[dfstu["degreeLevelType"] == 'Other', "degreeLevelType"] = 'Other_degree'
    dfstu.loc[~dfstu["studiesField"].isin(official_fields), "studiesField"] = 'Other_field'
    dfstu = dfstu[['id', 'homeUniversity', 'degreeLevelType', 'studiesField']]
    dfstu.rename(columns={'id':'studentId'}, inplace=True)

    # tehdään projektien talu ja muokataan sitä paremmaks
    temp = json.dumps(bronze_data['projects'])
    dfpro = pd.read_json(StringIO(temp))
    dfpro = dfpro[['id','themes', 'tags']]
    dfpro.rename(columns={'id':'projectId'}, inplace=True)

    # haetaan kaikki hakemukset (applications) ja tehdään niistä yksi taulu
    temp=''
    first = True
    for application_set in df['applications']:
        temp = json.dumps(application_set)
        if first:
            first = False
            dfapp = pd.read_json(StringIO(temp))
        else:
            dftemp = pd.read_json(StringIO(temp))
            dfapp = pd.concat([dfapp, dftemp])
    dfapp = dfapp[['projectId', 'studentId', 'relation']]
    dfapp.loc[dfapp["relation"] == 'Dropout', "relation"] = 'Selected'

    # yhdistetään hakemukset ja opiskelijat
    merged_df = pd.merge(dfapp, dfstu, on='studentId')

    # yhdistetään aikaisempitaulu ja projektit viimeiseksi tauluksi
    # (kaikkia projekteja ei mainittu projekteissa)
    final_merge_df = pd.merge(merged_df, dfpro, on='projectId', how='left')
    final_merge_df = final_merge_df[['tags','themes', 'degreeLevelType', 'studiesField', 'relation']]


    alternative_encode(final_merge_df)
    save_data(final_merge_df)
    return final_merge_df

    

    #final_merge_df['tags'] = final_merge_df['tags'].apply(lambda d: d if isinstance(d, list) else [])
    #final_merge_df['themes'] = final_merge_df['themes'].apply(lambda d: d if isinstance(d, list) else [])

    #final_merge_df = one_hot_encode(final_merge_df)
    #final_merge_df.fillna(0, inplace=True)
    #final_merge_df = final_merge_df.astype(int)
    #print(final_merge_df)
    #save_data(final_merge_df)

    

def clean_data_v2(load_name="rawData", save_name="cleaned_data"):
    # Return cleaned data as a list of Python dictionarys
    return clean_data_ev2(load_name, save_name)

def clean_data_v3(load_name="rawData", save_name="cleaned_data"):
    # Return cleaned data as a list of Python dictionarys
    return clean_data_ev3(load_name, save_name)

# tallennetaan käytettävä data
def save_data(table):
    dir = os.path.dirname(__file__)
    location = os.path.join(dir, 'data/cleaned_data.csv')
    table.to_csv(location)

def one_hot_encode(fdf):
    one_hot = pd.get_dummies(fdf['themes'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('themes', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['tags'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('tags', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['homeUniversity'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('homeUniversity', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['degreeLevelType'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('degreeLevelType', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['studiesField'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('studiesField', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['relation'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('relation', axis=1).join(one_hot)

    return fdf


def one_hot_encode_v2(fdf):
    # One-Hot Encode 'themes' with a prefix
    one_hot = pd.get_dummies(fdf['themes'].apply(pd.Series).stack(), prefix="theme").groupby(level=0).sum()
    fdf = fdf.drop('themes', axis=1).join(one_hot)

    # One-Hot Encode 'tags' with a prefix
    one_hot = pd.get_dummies(fdf['tags'].apply(pd.Series).stack(), prefix="tag").groupby(level=0).sum()
    fdf = fdf.drop('tags', axis=1).join(one_hot)

    # One-Hot Encode 'homeUniversity' with a prefix
    one_hot = pd.get_dummies(fdf['homeUniversity'], prefix="university")
    fdf = fdf.drop('homeUniversity', axis=1).join(one_hot)

    # One-Hot Encode 'degreeLevelType' with a prefix
    one_hot = pd.get_dummies(fdf['degreeLevelType'], prefix="degree")
    fdf = fdf.drop('degreeLevelType', axis=1).join(one_hot)

    # One-Hot Encode 'studiesField' with a prefix
    one_hot = pd.get_dummies(fdf['studiesField'], prefix="field")
    fdf = fdf.drop('studiesField', axis=1).join(one_hot)

    # One-Hot Encode 'relation' with a prefix
    one_hot = pd.get_dummies(fdf['relation'], prefix="relation")
    fdf = fdf.drop('relation', axis=1).join(one_hot)

    return fdf




#Toinen enkoodaus funktio, koska piti saada yhteen sarakkeeseen tässä vaiheessa
#kaikki yhden teeman tiedot

def alternative_encode(final_merge_df):
    encoders = {}

    for column in ['tags', 'themes']:
        # Flatten the lists, ensuring we skip any non-list values (e.g., NaN)
        flat_list = [item for sublist in final_merge_df[column] if isinstance(sublist, list) for item in sublist]

        le = LabelEncoder()
        le.fit(flat_list)

        # Fit on the unique values and transform
        final_merge_df[column] = final_merge_df[column].apply(
            lambda x: le.transform(x) if isinstance(x, list) else 0 if pd.isna(x) else x)

        # Store the encoder
        encoders[column] = le

    for column in ['homeUniversity', 'degreeLevelType', 'studiesField', 'relation']:
        le = LabelEncoder()
        final_merge_df[column] = le.fit_transform(final_merge_df[column])  # Muuntaa tekstin numeroiksi
        encoders[column] = le

    return final_merge_df, encoders
#clean_data()

#clean_data()

"""