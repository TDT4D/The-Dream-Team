import json
import pandas as pd
from io import StringIO
from utils import storage
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from scipy.spatial import distance

from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

# luetaan dataa ja tehdään tauluja
# sama kuin versio 3, mutta lisätty samanlaisuuden testaus projektin kuvauksen
# ja hakemusten whyProject sekä whyExperience kohtien kanssa.
# systeemi on kokeilullinen ja sen tuomaa hyötyä pitää testata.
# 2025-02-26 oikee rawData
def clean_data(load_name="2025-02-26", save_name="cleaned_data"):

    #luetaan data
    bronze_data = storage.load_json(load_name)

    if not bronze_data:
        print("ERROR: Failed to load data.")
        return None

    # studyfieldit joita ei valittu yhteenkään projektiin eivät ole mukana lopullisessa json tiedostossa
    
    official_fields = ['Performing arts','Visual arts', 'History', 'Languages and literature', 'Law','Philosophy', 'Theology',
                       'Anthropology','Economics','Geography','Political science','Psychology','Sociology','Social Work',
                       'Biology','Chemistry','Earth science','Space sciences','Physics','Computer Science','Mathematics','Business',
                       'Engineering and technology','Medicine and health'
                       ]

    # tehdään opiskelijoiden talu ja muokataan sitä paremmaks
    temp = json.dumps(bronze_data['students'])
    df = pd.read_json(StringIO(temp))
    dfstu= df[['id', 'degreeLevelType', 'studiesField']]
    dfstu.loc[dfstu["degreeLevelType"] == 'Other', "degreeLevelType"] = 'Other_degree'
    dfstu.loc[~dfstu["studiesField"].isin(official_fields), "studiesField"] = 'Other_field'
    dfstu = dfstu[['id', 'degreeLevelType', 'studiesField']]
    dfstu.rename(columns={'id':'studentId'}, inplace=True)

    # tehdään projektien talu ja muokataan sitä paremmaks
    temp = json.dumps(bronze_data['projects'])
    dfpro = pd.read_json(StringIO(temp))
    dfpro = dfpro[['id','description', 'themes', 'tags']]
    dfpro.rename(columns={'id':'projectId'}, inplace=True)

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
    dfapp = dfapp[['projectId', 'studentId','whyProject','whyExperience', 'relation']]
    dfapp.loc[dfapp["relation"] == 'Dropout', "relation"] = 'Selected'

    # yhdistetään hakemukset ja opiskelijat
    merged_df = pd.merge(dfapp, dfstu, on='studentId')

    # yhdistetään aikaisempitaulu ja projektit viimeiseksi tauluksi
    # (kaikkia projekteja ei mainittu projekteissa)
    final_merge_df = pd.merge(merged_df, dfpro, on='projectId', how='left')

    final_merge_df['tags'] = final_merge_df['tags'].apply(lambda d: d if isinstance(d, list) else [])

    # tagien tiivistys
    bigdict = tag_per_studyfield(final_merge_df)
    final_merge_df=tag_condenser(final_merge_df, bigdict)

    # samanlaisuuden testaus ja vaihetaan samanlaisuus scoreksi
    temporary_df = similaritytest(final_merge_df)
    final_merge_df['whyProject'] = temporary_df['whyProject']
    final_merge_df['whyExperience'] = temporary_df['whyExperience']
    final_merge_df = final_merge_df[['projectId','studentId','whyProject','whyExperience','relation','degreeLevelType','studiesField','themes','tags']]

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
    one_hot = pd.get_dummies(fdf['themes'].apply(pd.Series).stack(), prefix="theme").groupby(level=0).sum()
    fdf = fdf.drop('themes', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['degreeLevelType'].apply(pd.Series).stack(), prefix="degree").groupby(level=0).sum()
    fdf = fdf.drop('degreeLevelType', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['studiesField'].apply(pd.Series).stack(),  prefix="field").groupby(level=0).sum()
    fdf = fdf.drop('studiesField', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['relation'].apply(pd.Series).stack(), prefix="relation").groupby(level=0).sum()
    fdf = fdf.drop('relation', axis=1).join(one_hot)

    return fdf

def tag_condenser(df, bigdict):
    # score lasketaan (tag%+...+tag%)*pp,
    # missä tag%=tagin esiintymä studifieldissä
    # ja pp=projektin esiintymisprosentti valituista
    r = 0
    for row in df.itertuples():
        score = 0
        if not df['tags'][r]:
            df.loc[r, 'tags'] = score
        else:
            for i in df['tags'][r]:
                skip = False
                if row.studiesField in bigdict:
                    if i not in bigdict[row.studiesField]:
                        score += 0
                    else:
                        score += bigdict[row.studiesField][i]
                else:
                    skip = True
            if not skip:
                df.loc[r, 'tags'] = score * bigdict[row.studiesField]['percentage_of_chosen']
            else:
                df.loc[r, 'tags'] = 0
        r += 1
    return df

def tag_per_studyfield(df):
    empty = False

    df = df[['tags','studiesField', 'relation']]
    df2 = df[df['relation'].str.contains('Selected')]
    r = df2.shape[0]
    df2 = df2[['tags', 'studiesField']]

    #halutaan kaikki prosenttilaskuun mukaan, mutta dicitiin vain ei tyhjät

    t2 = df2['studiesField'].value_counts()
    t2dict = t2.to_dict()
    appearance = {}
    for i in t2dict:
        appearance.update({i: t2dict[i] / r})
    if not empty:
        df2 = df2[df2.astype(str)['tags'] != '[]']
    #studyfield_selection(df2)

    # kaikista valituista sudyfieldeistä, mitkä oli niiden tag prosentit
    bigdict = {}
    if empty:
        for row in df2.itertuples():
            if row.studiesField not in bigdict:
                bigdict.update({row.studiesField:{}})
            smalldict = bigdict[row.studiesField]
            if len(row.tags) == 0:
                if 'empty' not in smalldict:
                    smalldict.update({'empty':1})
                else:
                    ammount = smalldict['empty']
                    ammount +=1
                    smalldict.update({'empty':ammount})
            for i in row.tags:
                if i not in smalldict:
                    smalldict.update({i:1})
                else:
                    ammount = smalldict[i]
                    ammount +=1
                    smalldict.update({i:ammount})
    else:
        for row in df2.itertuples():
            if row.studiesField not in bigdict:
                bigdict.update({row.studiesField:{}})
            smalldict = bigdict[row.studiesField]
            for i in row.tags:
                if i not in smalldict:
                    smalldict.update({i:1})
                else:
                    ammount = smalldict[i]
                    ammount +=1
                    smalldict.update({i:ammount})

    for i in bigdict:
        for j in bigdict[i]:
            smalldict = bigdict[i]
            smalldict.update({j:bigdict[i][j] / t2dict[i]})
        smalldict.update({'percentage_of_chosen': appearance[i]})
    return bigdict

def alternative_encode(final_merge_df):
    encoders = {}

    for column in ['themes']:
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

def similaritytest_helper(model, tokenizer, df):

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

    r = 0
    indexes = df.index
    for row in df.itertuples():
        sentences = [row.whyProject, row.whyExperience]

        desc = row.description

        desc_vec = shortcut(model, tokenizer, desc)

        whyProject_score = 1 - distance.cosine(desc_vec, shortcut(model, tokenizer, sentences[0]))
        df.loc[indexes[r], 'whyProject'] = whyProject_score

        whyExperience_score = 1 - distance.cosine(desc_vec, shortcut(model, tokenizer, sentences[1]))
        df.loc[indexes[r], 'whyExperience'] = whyExperience_score

        r +=1

    return df

def similaritytest(df):
    df = df[['whyProject','whyExperience', 'relation', 'description']]
    df.dropna(subset=['description'], inplace=True)
    df['whyProject'] = df['whyProject'].fillna("")
    df['whyExperience'] = df['whyExperience'].fillna("")

    #SBERT this will take some time
    tokenizer = AutoTokenizer.from_pretrained("../models/similarity_tokenizer")
    model = AutoModel.from_pretrained("../models/similarity_model")

    return similaritytest_helper(model, tokenizer, df)

clean_data()