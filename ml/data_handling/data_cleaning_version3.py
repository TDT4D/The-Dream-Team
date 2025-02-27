import os
import json
import pandas as pd
from io import StringIO

# luetaan dataa ja tehdään tauluja (lisää myös koodaus)
# sama kuin versio 1, mutta tiivistetty tagit uudella scoring systeemillä
# systeemi on kokeilullinen ja sen tuomaa hyötyä pitää testata.
def clean_data_ev3():
    #luetaan data (muokattava sit ku tiedetään miten se saapuu, mistä ja milloin)
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
    dfstu= df[['id', 'degreeLevelType', 'studiesField']]
    dfstu.loc[dfstu["degreeLevelType"] == 'Other', "degreeLevelType"] = 'Other_degree'
    dfstu.loc[~dfstu["studiesField"].isin(official_fields), "studiesField"] = 'Other_field'
    dfstu = dfstu[['id', 'degreeLevelType', 'studiesField']]
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

    final_merge_df['tags'] = final_merge_df['tags'].apply(lambda d: d if isinstance(d, list) else [])
    final_merge_df['themes'] = final_merge_df['themes'].apply(lambda d: d if isinstance(d, list) else [])

    bigdict = tag_per_studyfield(final_merge_df)
    final_merge_df=tag_condenser(final_merge_df, bigdict)

    final_merge_df = one_hot_encode(final_merge_df)
    final_merge_df.fillna(0, inplace=True)
    final_merge_df = final_merge_df.astype(float)
    #print(final_merge_df)
    save_data(final_merge_df)

# tallennetaan käytettävä data
def save_data(table):
    dir = os.path.dirname(__file__)
    location = os.path.join(dir, 'data\cleaned_data.csv')
    table.to_csv(location)

def one_hot_encode(fdf):
    one_hot = pd.get_dummies(fdf['themes'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('themes', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['degreeLevelType'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('degreeLevelType', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['studiesField'].apply(pd.Series).stack()).groupby(level=0).sum()
    fdf = fdf.drop('studiesField', axis=1).join(one_hot)

    one_hot = pd.get_dummies(fdf['relation'].apply(pd.Series).stack()).groupby(level=0).sum()
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

#clean_data_v3()