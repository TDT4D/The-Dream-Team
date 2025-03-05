import json
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from utils import storage
from io import StringIO

def clean_data_ev2(load_name="rawData", save_name="cleaned_data"):
    """
    Cleans the raw dataset and either saves it as JSON or returns it as a dictionary.

    Args:
        load_name (str): Name of the input JSON file.
        save_name (str): Name of the output cleaned data file.

    Returns:
        dict: Cleaned data in dictionary format.
    """

    # Load raw data using storage utility
    bronze_data = storage.load_json(load_name)

    if not bronze_data:
        print("ERROR: Failed to load data.")
        return None

    official_fields = [
        'Performing arts', 'Visual arts', 'History',
        'Languages and literature',
        'Law', 'Philosophy', 'Theology', 'Anthropology', 'Economics',
        'Geography',
        'Political science', 'Psychology', 'Sociology', 'Social Work',
        'Biology',
        'Chemistry', 'Earth science', 'Space sciences', 'Physics',
        'Computer Science',
        'Mathematics', 'Business', 'Engineering and technology',
        'Medicine and health'
    ]

    # Convert JSON data to DataFrame (Students)
    temp = json.dumps(bronze_data['students'])
    df = pd.read_json(StringIO(temp))
    dfstu = df[['id', 'degreeLevelType', 'studiesField']]
    dfstu.loc[dfstu["degreeLevelType"] == 'Other', "degreeLevelType"] = 'Other_degree'
    dfstu.loc[~dfstu["studiesField"].isin(official_fields), "studiesField"] = 'Other_field'
    dfstu = dfstu[['id', 'degreeLevelType', 'studiesField']]
    dfstu.rename(columns={'id': 'studentId'}, inplace=True)

    # Convert JSON data to DataFrame (Projects)
    temp = json.dumps(bronze_data['projects'])
    dfpro = pd.read_json(StringIO(temp))
    dfpro = dfpro[['id', 'themes', 'tags']]
    dfpro.rename(columns={'id': 'projectId'}, inplace=True)

    # Extract applications from students
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

    # Merge applications with students
    merged_df = pd.merge(dfapp, dfstu, on='studentId')

    # Merge previous table with projects
    final_merge_df = pd.merge(merged_df, dfpro, on='projectId', how='left')
    final_merge_df_copy = final_merge_df[
        ['tags', 'themes', 'degreeLevelType', 'studiesField',
         'relation']]

    # Convert to dictionary format
    cleaned_data_copy = final_merge_df_copy.to_dict(orient="records")

    # Save cleaned data using storage utility
    storage.save_json(cleaned_data_copy, save_name)

    # Apply Encoding
    final_merge_df, encoders = alternative_encode(final_merge_df)  # label encoding
    # One-Hot Encode tags & themes
    final_merge_df = one_hot_encode_v2(final_merge_df)

    # Fill missing values and convert data to float for ML compatibility
    final_merge_df.fillna(0, inplace=True)
    final_merge_df = final_merge_df.astype(float)

    # Convert to dictionary format
    cleaned_data = final_merge_df.to_dict(orient="records")

    # Save cleaned data using storage utility
    save2 = "cleaned_data_encoded"
    storage.save_json(cleaned_data, save2)

    return cleaned_data  # Return cleaned data as list of Python dictionarys

def one_hot_encode_v2(fdf):
    # One-Hot Encode 'themes' with a prefix
    one_hot = pd.get_dummies(fdf['themes'].apply(pd.Series).stack(), prefix="theme").groupby(level=0).sum()
    fdf = fdf.drop('themes', axis=1).join(one_hot)

    # One-Hot Encode 'tags' with a prefix
    one_hot = pd.get_dummies(fdf['tags'].apply(pd.Series).stack(), prefix="tag").groupby(level=0).sum()
    fdf = fdf.drop('tags', axis=1).join(one_hot)

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

    for column in ['degreeLevelType', 'studiesField', 'relation']:
        le = LabelEncoder()
        final_merge_df[column] = le.fit_transform(final_merge_df[column])  # Muuntaa tekstin numeroiksi
        encoders[column] = le

    return final_merge_df, encoders

#clean_data_v2()