import json
import pandas as pd
from io import StringIO
from utils import storage
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from scipy.spatial import distance

from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

# luetaan dataa ja tehdään tauluja motivaatiolle versio 1
def clean_data(load_name="rawData", save_name="cleaned_data_motivation2"):
    # luetaan data
    bronze_data = storage.load_json(load_name)

    if not bronze_data:
        print("ERROR: Failed to load data.")
        return None

    # tehdään opiskelijoiden talu ja muokataan sitä paremmaks
    temp = json.dumps(bronze_data['students'])
    df = pd.read_json(StringIO(temp))
    dfstu = df[['id', 'cvLink','socialNetworkLinks','studiesDescription','whyJoinDemola','whyGoodCreator','whyRole']]
    dfstu.rename(columns={'id': 'studentId'}, inplace=True)

    # tehdään projektien talu ja muokataan sitä paremmaks
    temp = json.dumps(bronze_data['projects'])
    dfpro = pd.read_json(StringIO(temp))
    dfpro = dfpro[['id']]
    dfpro.rename(columns={'id': 'projectId'}, inplace=True)

    # haetaan kaikki hakemukset (applications) ja tehdään niistä yksi taulu
    first = True
    for application_set in df['applications']:
        temp = json.dumps(application_set)
        if first:
            first = False
            dfapp = pd.read_json(StringIO(temp))
        else:
            dftemp = pd.read_json(StringIO(temp))
            dfapp = pd.concat([dfapp, dftemp])
    dfapp = dfapp[['projectId', 'studentId','chosenBatch','whyProject','whyExperience', 'relation']]

    # yhdistetään hakemukset ja opiskelijat
    merged_df = pd.merge(dfapp, dfstu, on='studentId')

    # yhdistetään aikaisempitaulu ja projektit viimeiseksi tauluksi
    final_merge_df = pd.merge(merged_df, dfpro, on='projectId', how='left')

    # vaihdetaan linkit binääriseen muotoon (etsitään onko kenttä täytetty)
    temporary_df = cv_and_link_checker(final_merge_df)
    final_merge_df['cvLink'] = temporary_df['cvLink']
    final_merge_df['socialNetworkLinks'] = temporary_df['socialNetworkLinks']

    temporary_df = optional_field_calculator(final_merge_df)
    final_merge_df['optional field percentage'] = temporary_df['optional field percentage']
    final_merge_df.drop(
        ['studiesDescription', 'whyJoinDemola', 'whyGoodCreator', 'whyRole',
         ], axis=1, inplace=True)

    final_merge_df["similarity_score_avg_whyProject"] = 0
    final_merge_df["similarity_score_max_whyProject"] = 0
    final_merge_df["similarity_score_avg_whyExperience"] = 0
    final_merge_df["similarity_score_max_whyExperience"] = 0

    temporary_df = application_similarity(final_merge_df)

    final_merge_df["similarity_score_avg_whyProject"] = temporary_df["similarity_score_avg_whyProject"]
    final_merge_df["similarity_score_max_whyProject"] = temporary_df["similarity_score_max_whyProject"]
    final_merge_df["similarity_score_avg_whyExperience"] = temporary_df["similarity_score_avg_whyExperience"]
    final_merge_df["similarity_score_max_whyExperience"] = temporary_df["similarity_score_max_whyExperience"]

    final_merge_df.drop(
        ['whyProject','whyExperience', 'chosenBatch'], axis=1, inplace=True)

    final_merge_df, encoders = alternative_encode(
        final_merge_df)

    final_merge_df = one_hot_encode(final_merge_df)

    final_merge_df.fillna(0, inplace=True)
    final_merge_df = final_merge_df.astype(float)

    cleaned = final_merge_df.to_dict(orient="records")

    # tallennetaan käytettävä data
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
    df['whyProject'] = df['whyProject'].fillna("")
    df['whyExperience'] = df['whyExperience'].fillna("")

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
    df['whyProject'] = df['whyProject'].fillna("")
    df['whyExperience'] = df['whyExperience'].fillna("")
    studentIds = df['studentId'].values.tolist()
    studentIds = list(set(studentIds))

    tokenizer = AutoTokenizer.from_pretrained("../models/similarity_tokenizer")
    model = AutoModel.from_pretrained("../models/similarity_model")

    def shortcut(model, tokenizer, word):

        def mean_pooling(model_output, attention_mask):
            token_embeddings = model_output[
                0]  # First element of model_output contains all token embeddings
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(
                token_embeddings.size()).float()
            return torch.sum(token_embeddings * input_mask_expanded,
                             1) / torch.clamp(input_mask_expanded.sum(1),
                                              min=1e-10)

        # Tokenize sentences
        encoded_input = tokenizer([word][0], padding=True, truncation=True,
                                  return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = model(**encoded_input)

        # Perform pooling
        sentence_embeddings = mean_pooling(model_output,
                                           encoded_input['attention_mask'])

        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings[0]

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

            test_vec = shortcut(model, tokenizer, whyProject)

            for j2 in locations:
                if (j2 != j) and (df.iloc[j2]['chosenBatch'] == jbatch):
                    row2 = df.iloc[j2]
                    whyProject2 = row2['whyProject']
                    temp = 1 - distance.cosine(test_vec, shortcut(model, tokenizer, whyProject2))
                    similarity_score_avg_pro += temp
                    if temp > similarity_score_max_pro:
                        similarity_score_max_pro = temp

            similarity_score_avg_pro = similarity_score_avg_pro/len(locations)
            df.loc[j, 'similarity_score_avg_whyProject'] = similarity_score_avg_pro
            df.loc[j, 'similarity_score_max_whyProject'] = similarity_score_max_pro

            whyExperience = row['whyExperience']
            test_vec = shortcut(model, tokenizer, whyExperience)
            for j2 in locations:
                if (j2 != j) and (df.iloc[j2]['chosenBatch'] == jbatch):
                    row2 = df.iloc[j2]
                    whyExperience2 = row2['whyExperience']
                    temp = 1 - distance.cosine(test_vec, shortcut(model, tokenizer, whyExperience2))
                    similarity_score_avg_exp += temp
                    if temp > similarity_score_max_exp:
                        similarity_score_max_exp = temp
            similarity_score_avg_exp = similarity_score_avg_exp / len(locations)
            df.loc[
                j, 'similarity_score_avg_whyExperience'] = similarity_score_avg_exp
            df.loc[
                j, 'similarity_score_max_whyExperience'] = similarity_score_max_exp
    return df

clean_data()