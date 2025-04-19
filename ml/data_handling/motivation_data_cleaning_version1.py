import json
import pandas as pd
from io import StringIO
from utils import storage
from sklearn.preprocessing import LabelEncoder
from scipy.spatial import distance
try:
    from sentence_transformers import SentenceTransformer #type: ignore
except ModuleNotFoundError:
    import sys
    def sentence_transformers(reqModel: str) -> None:
        print(f"SentenceTransformer package not imported! Tried loading model {reqModel}", file=sys.stderr)
        raise


# start here
def clean_data(load_name="rawData", save_name="cleaned_data_motivation"):
    # this function reads and cleans data for motivation

    #reading data and checking if it has the necessary fields
    bronze_data = storage.load_json(load_name)

    if not bronze_data:
        print("ERROR: Failed to load data.")
        return None

    keys1 = bronze_data.keys()

    if 'students' not in keys1:
        print("ERROR: The field 'students' is missing from data.")
        return None
    if 'projects' not in keys1:
        print("ERROR: The field 'projects' is missing from data.")
        return None

    def check_fields(needed_fields, df, name):
        for field in needed_fields:
            if field not in df.columns:
                print(
                    "ERROR: The field '" + field + "' is missing from "
                    +name+" data.")
                return False
        return True

    # making the student table
    temp = json.dumps(bronze_data['students'])
    df = pd.read_json(StringIO(temp))

    needed_fields_student = ['id', 'cvLink','socialNetworkLinks',
                             'studiesDescription','whyJoinDemola',
                             'whyGoodCreator','whyRole', 'degreeLevelType']

    if not check_fields(needed_fields_student, df, 'students'):
        return None

    dfstu = df[['id', 'cvLink','socialNetworkLinks','studiesDescription',
                'whyJoinDemola','whyGoodCreator','whyRole', 'degreeLevelType']]

    dfstu.rename(columns={'id': 'studentId'}, inplace=True)

    # making the projects table
    temp = json.dumps(bronze_data['projects'])
    dfpro = pd.read_json(StringIO(temp))

    needed_fields_project = ['id']

    if not check_fields(needed_fields_project, dfpro, 'projects'):
        return None

    dfpro = dfpro[['id']]
    dfpro.rename(columns={'id': 'projectId'}, inplace=True)

    # making the applications table
    needed_fields_application = ['projectId', 'studentId','chosenBatch',
                                 'whyProject','whyExperience', 'relation']
    first = True
    for application_set in df['applications']:
        temp = json.dumps(application_set)
        if first:
            first = False
            dfapp = pd.read_json(StringIO(temp))

            if not check_fields(needed_fields_application, dfapp, 'applications'):
                return None
        else:
            dftemp = pd.read_json(StringIO(temp))
            dfapp = pd.concat([dfapp, dftemp])

    dfapp = dfapp[['projectId', 'studentId','chosenBatch','whyProject',
                   'whyExperience', 'relation']]

    # combining applications and students to one table
    merged_df = pd.merge(dfapp, dfstu, on='studentId')

    # combining the previous table with projects
    final_merge_df = pd.merge(merged_df, dfpro, on='projectId', how='left')

    # making the data more usable
    final_merge_df['whyProject'] = final_merge_df['whyProject'].fillna("")
    final_merge_df['whyExperience'] = final_merge_df['whyExperience'].fillna("")

    # checking if the data is usable
    def is_dict_ok(final_merge_df, name1):
        for value_dict in final_merge_df[name1]:
            if isinstance(value_dict, dict):
                for value in value_dict:
                    if not isinstance(value, str):
                        print("ERROR: A dict key was not of type string")
                        return False
                    if isinstance(value_dict[value], list):
                        for list_value in value_dict[value]:
                            if not isinstance(list_value, str):
                                print(
                                    "ERROR: A dict payload list element was not of type string")
                                return False
                    else:
                        print("ERROR: A dict payload was not of type list")
                        return False
            else:
                print(
                    "ERROR: The field '" + name1 + "' had a value that was not a dict.")
                return False
        return True

    def is_number_ok(final_merge_df, name1):
        for value in final_merge_df[name1]:
            if not isinstance(value, int):
                if not value.is_integer():
                    print("ERROR: A " + name1 + " was not of correct type")
                    return False
        return True

    def is_string_ok(final_merge_df, name1):
        for value in final_merge_df[name1]:
            if not isinstance(value, str):
                print("ERROR: A " + name1 + " was not of type string")
                return False
        return True

    def is_string_that_can_be_none_ok(final_merge_df, name1):
        for value in final_merge_df[name1]:
            if not isinstance(value, str):
                if value:
                    print("ERROR: A " + name1 + " was not of type string")
                    return False
        return True

    def is_batch_ok(final_merge_df, name1):
        for value in final_merge_df[name1]:
            if not isinstance(value, int):
                if not value.is_integer():
                    if value and (not pd.isna(value)):
                        print("ERROR: A " + name1 + " was not of correct type")
                        return False
        return True

    if not is_number_ok(final_merge_df, 'studentId'):
        return None
    if not is_number_ok(final_merge_df, 'projectId'):
        return None
    if not is_batch_ok(final_merge_df, 'chosenBatch'):
        return None
    if not is_string_ok(final_merge_df, 'relation'):
        return None
    if not is_string_ok(final_merge_df, 'whyProject'):
        return None
    if not is_string_ok(final_merge_df, 'whyExperience'):
        return None
    if not is_string_that_can_be_none_ok(final_merge_df, 'cvLink'):
        return None
    if not is_dict_ok(final_merge_df, 'socialNetworkLinks'):
        return None
    if not is_string_that_can_be_none_ok(final_merge_df, 'studiesDescription'):
        return None
    if not is_string_that_can_be_none_ok(final_merge_df, 'whyJoinDemola'):
        return None
    if not is_string_that_can_be_none_ok(final_merge_df, 'whyGoodCreator'):
        return None
    if not is_string_that_can_be_none_ok(final_merge_df, 'whyRole'):
        return None

    # checking links
    temporary_df = cv_and_link_checker(final_merge_df)
    final_merge_df['cvLink'] = temporary_df['cvLink']
    final_merge_df['socialNetworkLinks'] = temporary_df['socialNetworkLinks']

    # checking filling rate for optional fields
    temporary_df = optional_field_calculator(final_merge_df)
    final_merge_df['optional field percentage'] = temporary_df['optional field percentage']

    # cleaning up the tabel
    final_merge_df.drop(
        ['studiesDescription', 'whyJoinDemola', 'whyGoodCreator', 'whyRole',
         ], axis=1, inplace=True)

    # checking if student was selected in the same batch
    final_merge_df['was_selected'] = 0
    final_merge_df['was_selected'] = was_already_chosen(final_merge_df)

    # checking free text field similarity
    final_merge_df["similarity_score_avg_whyProject"] = 0
    final_merge_df["similarity_score_max_whyProject"] = 0
    final_merge_df["similarity_score_avg_whyExperience"] = 0
    final_merge_df["similarity_score_max_whyExperience"] = 0

    temporary_df = application_similarity(final_merge_df)

    final_merge_df["similarity_score_avg_whyProject"] = temporary_df["similarity_score_avg_whyProject"]
    final_merge_df["similarity_score_max_whyProject"] = temporary_df["similarity_score_max_whyProject"]
    final_merge_df["similarity_score_avg_whyExperience"] = temporary_df["similarity_score_avg_whyExperience"]
    final_merge_df["similarity_score_max_whyExperience"] = temporary_df["similarity_score_max_whyExperience"]

    # cleaning up the tabel
    old_size = final_merge_df.shape[0]
    final_merge_df.dropna(subset=['degreeLevelType'], inplace=True)
    new_size = final_merge_df.shape[0]
    if new_size < old_size:
        per = (1 - new_size / old_size) * 100
        print("WARNING: some rows were dropped from table, because "
              "'degreeLevelType' didn't have a value in that row."
              "the dropped rows accounted for " + str(per) + "% of the current"
                                                             " dataframe.")

    old_size = final_merge_df.shape[0]
    final_merge_df.dropna(subset=['chosenBatch'], inplace=True)
    new_size = final_merge_df.shape[0]
    if new_size < old_size:
        per = (1 - new_size / old_size) * 100
        print("WARNING: some rows were dropped from table, because "
              "'chosenBatch' didn't have a value in that row."
              "the dropped rows accounted for " + str(
            per) + "% of the current dataframe.")

    final_merge_df.drop(
        ['whyProject', 'whyExperience', 'chosenBatch', 'degreeLevelType'], axis=1, inplace=True)

    # encoding and saving
    final_merge_df, encoders = alternative_encode(
        final_merge_df)

    final_merge_df = one_hot_encode(final_merge_df)

    final_merge_df.fillna(0, inplace=True)
    final_merge_df = final_merge_df.astype(float)

    cleaned = final_merge_df.to_dict(orient="records")

    storage.save_json(cleaned, save_name)

    return cleaned


def one_hot_encode(fdf):
    one_hot = pd.get_dummies(fdf['relation'].apply(pd.Series).stack(),
                             prefix="relation").groupby(level=0).sum()
    fdf = fdf.drop('relation', axis=1).join(one_hot)

    return fdf

def alternative_encode(final_merge_df):
    encoders = {}

    for column in ['relation']:
        le = LabelEncoder()
        final_merge_df[column] = le.fit_transform(
            final_merge_df[column])  # Muuntaa tekstin numeroiksi
        encoders[column] = le

    return final_merge_df, encoders

def cv_and_link_checker(df):
    # this function marks all aplication cv nad link fields
    # with 1 if it is filled and 0 if not
    df = df[['studentId','cvLink','socialNetworkLinks']]
    df['cvLink'] = df['cvLink'].fillna(0)
    df['socialNetworkLinks'] = df['socialNetworkLinks'].fillna(0)
    df.loc[df['cvLink'] != 0, 'cvLink'] = 1
    df.loc[df['socialNetworkLinks'] == {}, 'socialNetworkLinks'] = 0
    df.loc[df['socialNetworkLinks'] != 0, 'socialNetworkLinks'] = 1
    return df

def optional_field_calculator(df):
    # calculates how many optional fields the students has filled (doesn't include cv and links).
    # the fields are: studiesDescription, whyJoinDemola, whyGoodCreator, whyRole, whyProject, whyExperience
    # it also checks if the length of the written text is 10 or more
    # (6 or more with whyRole, because they could just write: leader etc.)
    df = df[['studentId', 'studiesDescription','whyJoinDemola','whyGoodCreator','whyRole', 'whyProject', 'whyExperience']]

    def calculate_percentage(row):
        # calculates the percentage of filled optional fields
        score = 0
        if row['studiesDescription']:
            if len(row['studiesDescription']) >= 10:
                score += 1
        if row['whyJoinDemola']:
            if len(row['whyJoinDemola']) >= 10:
                score += 1
        if row['whyGoodCreator']:
            if len(row['whyGoodCreator']) >= 10:
                score += 1
        if row['whyProject']:
            if len(row['whyProject']) >= 10:
                score += 1
        if row['whyExperience']:
            if len(row['whyExperience']) >= 10:
                score += 1
        if row['whyRole']:
            if len(row['whyRole']) >= 6:
                score += 1
        return score/6

    df['optional field percentage'] = df.apply(calculate_percentage, axis=1)
    return df

def application_similarity(df):
    # application similarity in the same batch within fields whyProject and whyExperience
    # checks if the same text or very similar text has been used multiple times
    # in different applications in the same batch with SBERT
    # (this will take some time 2min).
    studentIds = df['studentId'].values.tolist()
    studentIds = list(set(studentIds))

    model = SentenceTransformer('all-MiniLM-L6-v2')

    for i in studentIds:
        locations = df.index[df['studentId'] == i].tolist()
        for j in locations:
            similarity_score_avg_pro = 0
            similarity_score_max_pro = 0
            similarity_score_avg_exp = 0
            similarity_score_max_exp = 0
            row = df.iloc[j]

            jbatch = row['chosenBatch']
            whyProject = row['whyProject']
            test_vec = model.encode([whyProject])[0]
            devider = 0
            for j2 in locations:
                if (j2 != j) and (df.iloc[j2]['chosenBatch'] == jbatch):
                    devider +=1
                    row2 = df.iloc[j2]
                    whyProject2 = row2['whyProject']
                    temp = 1 - distance.cosine(test_vec, model.encode([whyProject2])[0])
                    similarity_score_avg_pro += temp
                    if temp > similarity_score_max_pro:
                        similarity_score_max_pro = temp
            if devider != 0:
                similarity_score_avg_pro = similarity_score_avg_pro/devider
            df.loc[j, 'similarity_score_avg_whyProject'] = similarity_score_avg_pro
            df.loc[j, 'similarity_score_max_whyProject'] = similarity_score_max_pro

            whyExperience = row['whyExperience']
            test_vec = model.encode([whyExperience])[0]
            devider = 0
            for j2 in locations:
                if (j2 != j) and (df.iloc[j2]['chosenBatch'] == jbatch):
                    devider += 1
                    row2 = df.iloc[j2]
                    whyExperience2 = row2['whyExperience']
                    temp = 1 - distance.cosine(test_vec, model.encode([whyExperience2])[0])
                    similarity_score_avg_exp += temp
                    if temp > similarity_score_max_exp:
                        similarity_score_max_exp = temp
            if devider != 0:
                similarity_score_avg_exp = similarity_score_avg_exp /devider
            df.loc[
                j, 'similarity_score_avg_whyExperience'] = similarity_score_avg_exp
            df.loc[
                j, 'similarity_score_max_whyExperience'] = similarity_score_max_exp
    return df

def was_already_chosen(df):
    # checks if a student was already chosen in the same batch

    df = df[['studentId', 'chosenBatch', 'relation']]
    length = df.shape[0]
    previd = 0
    prevbatch = 0
    temp = []
    rel = []
    first = True
    for row in df.itertuples():
        if first:
            temp.append(row.Index)
            rel.append(row.relation)
            first = False
            previd = row.studentId
            prevbatch = row.chosenBatch
        else:
            if (row.studentId == previd) and (row.chosenBatch == prevbatch):
                temp.append(row.Index)
                rel.append(row.relation)
            else:
                if 'Selected' in rel:
                    for i in temp:
                        df.loc[i, 'was_selected'] = 1
                temp.clear()
                rel.clear()
                temp.append(row.Index)
                rel.append(row.relation)
                previd = row.studentId
                prevbatch = row.chosenBatch
                if row.Index == length - 1:
                    if 'Selected' in rel:
                        for i in temp:
                            df.loc[i, 'was_selected'] = 1
    return df['was_selected']

#clean_data()
