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

# luetaan dataa ja tehdään tauluja
# sama kuin versio 3, mutta lisätty samanlaisuuden testaus projektin kuvauksen
# ja hakemusten whyProject sekä whyExperience kohtien kanssa.
# systeemi on kokeilullinen ja sen tuomaa hyötyä pitää testata.
def clean_data(load_name="rawData", save_name="cleaned_data"):

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
    dfstu= df[['id','city', 'degreeLevelType', 'studiesField']]
    dfstu.loc[dfstu["degreeLevelType"] == 'Other', "degreeLevelType"] = 'Other_degree'
    dfstu.loc[~dfstu["studiesField"].isin(official_fields), "studiesField"] = 'Other_field'
    dfstu = dfstu[['id','city', 'degreeLevelType', 'studiesField']]
    dfstu.rename(columns={'id':'studentId'}, inplace=True)

    # tehdään projektien talu ja muokataan sitä paremmaks
    temp = json.dumps(bronze_data['projects'])
    dfpro = pd.read_json(StringIO(temp))

    # temporary check so that the older data works
    if 'locations' not in dfpro.columns:
        dfpro['locations'] = [[] for _ in range(len(dfpro))]

    dfpro = dfpro[['id','description','locations', 'themes', 'tags']]
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
    dfapp = dfapp[['chosenBatch','projectId', 'studentId','whyProject','whyExperience', 'relation']]
    dfapp.loc[dfapp["relation"] == 'Dropout', "relation"] = 'Selected'

    # yhdistetään hakemukset ja opiskelijat
    merged_df = pd.merge(dfapp, dfstu, on='studentId')

    # yhdistetään aikaisempitaulu ja projektit viimeiseksi tauluksi
    # (kaikkia projekteja ei mainittu projekteissa)
    final_merge_df = pd.merge(merged_df, dfpro, on='projectId', how='left')

    final_merge_df['tags'] = final_merge_df['tags'].apply(lambda d: d if isinstance(d, list) else [])
    final_merge_df['locations'] = final_merge_df['locations'].apply(lambda d: d if isinstance(d, list) else [])

    # condensing tags
    bigdict = tag_per_studyfield(final_merge_df)
    final_merge_df=tag_condenser(final_merge_df, bigdict)
    final_merge_df['was_selected'] = was_already_chosen(final_merge_df)
    final_merge_df['locations'] = location_match(final_merge_df)
    final_merge_df.rename(columns={'locations': 'location_match'}, inplace=True)

    # samanlaisuuden testaus ja vaihetaan samanlaisuus scoreksi
    temporary_df = similaritytest(final_merge_df)
    final_merge_df['whyProject'] = temporary_df['whyProject']
    final_merge_df['whyExperience'] = temporary_df['whyExperience']
    final_merge_df = final_merge_df[['projectId','studentId','whyProject','whyExperience','relation','degreeLevelType','studiesField','themes','tags', 'was_selected', 'location_match']]

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

def similaritytest_helper(model, df):
    r = 0
    indexes = df.index
    for row in df.itertuples():
        sentences = [row.whyProject, row.whyExperience]

        desc = row.description

        desc_vec = model.encode([desc])[0]

        whyProject_score = 1 - distance.cosine(desc_vec, model.encode([sentences[0]])[0])
        df.loc[indexes[r], 'whyProject'] = whyProject_score

        whyExperience_score = 1 - distance.cosine(desc_vec,model.encode([sentences[1]])[0])
        df.loc[indexes[r], 'whyExperience'] = whyExperience_score

        r +=1

    return df

def similaritytest(df):
    #from sentence_transformers import SentenceTransformer # type: ignore
    df = df[['whyProject','whyExperience', 'relation', 'description']]
    df.dropna(subset=['description'], inplace=True)
    df['whyProject'] = df['whyProject'].fillna("")
    df['whyExperience'] = df['whyExperience'].fillna("")

    #SBERT
    model = SentenceTransformer('all-MiniLM-L6-v2')

    return similaritytest_helper(model, df)

def was_already_chosen(df):
    df = df[['studentId', 'chosenBatch', 'relation']]
    df['was_selected'] = 0
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
                        df.at[i, 'was_selected'] = 1
                temp.clear()
                rel.clear()
                temp.append(row.Index)
                rel.append(row.relation)
                previd = row.studentId
                prevbatch = row.chosenBatch
                if row.Index == length-1:
                    if 'Selected' in rel:
                        for i in temp:
                            df.at[i, 'was_selected'] = 1
    return df['was_selected']

def location_match(df):
    # checks if applicant is located "near" the project city
    # 0 if not 1 if is and 2 if it can't be determined
    df = df[['projectId','studentId','city','locations']]
    def cities_near_locations():
        # locations that are "near" the project city.
        # selection was done by looking at google maps and adding locations
        # that are in a circle with an about 23 km radius. with the center
        # point of the circle being the project city center.
        tampere = ['Ylöjärvi', 'Nokia', 'Kangasala', 'ruutana', 'sääksjärvi',
                   'pirkkala', 'kulju', 'vesilahti', 'lempäälä', 'kyötikkälä',
                   'suinula', 'kämmenniemi', 'teisko', 'linnavuori',
                   'siuro', 'mutala', 'pinsiö', 'tottijärvi', 'savo', 'sankila',
                   'pere', 'viitapohja','pohtola', 'aitolahti', 'aitoniemi', 'suomatka',
                   'pelisalmi', 'majaalahti', 'kaivanto', 'raikku',
                   'riku', 'hervanta', 'kaukajärvi', 'hallila', 'leppänen',
                   'koivistonkylä', 'härmälä', 'pispala', 'linnainmaa', 'atala',
                   'takahuhti', 'tasanne', 'olkahinen', 'pirkkala', 'epilä',
                   'tesoma', 'rahola', 'lielahti', 'lentävänniemi',
                   'haukiluoma', 'vuorentausta', 'keskisenkulma', 'säijälä',
                   'sorva', 'kangasniemi', 'pinsiö', 'takamaa', 'vahanta',
                   'lempiäniemi', 'ylinen', 'kuivaspää', 'hulikankulma',
                   'aimala', 'säijä', 'miemola', 'pelisalmi', 'majaalahti']
        helsinki = ['luukki', 'oittaa', 'haltiala', 'espoo', 'masala',
                    'klaukkala','kerava', 'söderkulla', 'vantaa',
                    'kirkkonummi', 'backas', 'pieti', 'myllykylä',
                    'oittaa', 'ämmässuo', 'laajasalo', 'lepsämä', 'lakisto',
                    'korpilampi', 'luukki', 'velskola', 'kauniainen', 'hanaböle',
                    'nuuksio', 'lakisto', 'veikkola', 'lapinkylä', 'sepänkylä',
                    'sarvvik', 'munkkiranta', 'gumbostrand', 'korsnäs', 'nybygget',
                    'hangelby', 'söderkulla', 'immersby', 'hanaböle', 'lahela',
                    'ruotsinkylä', 'hyrylä']
        turku = ['mietoinen', 'masku', 'petäsmäki', 'raisio', 'askainen',
                 'naantali', 'aura', 'otava', 'rymättylä', 'röölä',
                 'ålönsaari', 'parainen','kaarina', 'piikkiö', 'paimio',
                 'lieto', 'paattinen', 'sauvo', 'liittoinen', 'raisio',
                 'upalinko','niemenkulma', 'humikkala', 'rusko', 'nummi',
                 'lemu','mäntymäki', 'haukula','jäkärilä', 'poikko', 'haarla',
                 'toivonlinna']
        oulu = ['huttukylä', 'jääli', 'kiiminki', 'alakylä', 'kalimeenkylä',
                'liikasenperä', 'haukipudas', 'vehkaperä', 'salonpää', 'peuhu',
                'liminka', 'tupos', 'kempele', 'mäntylä', 'murto',
                'päivärinne', 'pikkarala', 'saarela', 'vesala']
        vaasa = ['mustasaari', 'koivulahti', 'petsmo', 'jungsund',
                 'raippaluoto', 'riback', 'jungsund', 'iskmo', 'grönvik',
                 'södrä vallgrund', 'sundom', 'maalahti', 'sulva', 'laihia',
                 'helsingby', 'runsor', 'vähäkyrö', 'alskat', 'koskö',
                 'västerhankmo','österhankmo', 'kuni', 'voitila', 'veikkaala',
                 'merikaarto', 'torkkola', 'vähäkyrö', 'vikby', 'höstvesi',
                 'sulva', 'ruto', 'potila', 'laihia', 'vedenoja',
                 'hiiripelto', 'tervajoki', 'hölby', 'höghulten', 'riimala',
                 'bergbacken', 'övermalax', 'strorbacken', 'kråkbacken',
                 'långåminne', 'söderfjärden', 'öjna', 'åminne']
        glasgow = ['dumbarton', 'clydebank', 'paisley', 'east kilbride',
                   'larkhall','motherwell', 'airdrie', 'cumbernauld']
        london = ['enfield', 'watford', 'harrow', 'wembley', 'southall',
                  'hounslow',
                  'kingston-upon-thames', 'epsom', 'sutton', 'croydon',
                  'orpington',
                  'bromley', 'dartford', 'romford', 'ilford']
        bragança = ['rio de onor', 'Aveleda', 'baçal', 'frança', 'portelo',
                    'montesinho',
                    'meixedo', 'mofreita', 'zeive', 'moimenta', 'montouto',
                    'soeira',
                    'espinhosela', 'gondesende', 'lagarelhos', 'rio de fornos',
                    'sobreiro de cima', 'sobreiro de baixo', 'vinhais',
                    'cidões',
                    'ousilhão', 'castro de avelãs', 'carrazedo', 'falgueiras',
                    'nogueira', 'negreda', 'mós de celas', 'murçós',
                    'espadanedo',
                    'soutelo mourisco', 'rebordaínhos', 'vale de nogueira',
                    'salsa',
                    'fermentãos', 'serapicos', 'pinela', 'failde', 'calvelhe',
                    'paradinha nova', 'parada', 'coelhoso', 'samil',
                    'são pedro de serracenos',
                    'alfaião', 'rio frio', 'quintanilha', 'réfega', 'gimonde',
                    'bairro dos formafigos', 'são julião de palãcio',
                    'vila meã',
                    'deilão', 'guadramil']
        santarem = ['almeiri', 'golegã', 'rio maior']
        budapest = ['pilisvörösvár', 'szentendre', 'dunakeszi', 'gödöllő',
                    'pécel',
                    'gyömrő', 'vecsés', 'Üllő', 'szigetszentmiklós',
                    'százhalombatta', 'érd', 'törökbálint', 'budaörs']
        ostrava = ['bílovec', 'studénka', 'klimkovice', 'příbor', 'hukvaldy',
                   'kopřivnice', 'brušperk', 'frýdlant nad ostravicí',
                   'baška', 'frýdek-místek', 'vratimov', 'těrlicko',
                   'havířov', 'šenov', 'horní suchá', 'petřvald',
                   'karviná', 'rychvald', 'orlová', 'bohumín',
                   'kobeřice', 'bolatice', 'kravaře', 'dolní benešov',
                   'hlučín', 'háj ve slezsku', 'velká polom']
        prague = ['praha', 'kladno', 'unhošt', 'hostivice', 'chýně',
                  'rudná', 'řevnice', 'dobřichovice', 'černošice',
                  'mníšek pod brdy', 'davle', 'štěchovice', 'jílově u prahy',
                  'vestec', 'jesenice', 'psáry', 'kamenice', 'velké popovice',
                  'průhonice', 'mnichovice', 'říčany', 'mukařov',
                  'Úvaly', 'šestajovice', 'čelákovice',
                  'brandýs nad labem-stará boleslav', 'kostelec nad labem',
                  'tišice', 'neratovice', 'líbeznice', 'zdiby', 'klecany',
                  'roztoky', 'veltrusy', 'kralupy nad vltavou', 'odolena voda',
                  'libčice nad vltavou', 'roztoky', 'velké přílepy',
                  'horoměřice', 'buštěhrad']
        hokkaido = ['sapporo', 'otaru', 'ishikari', 'tobetsu', 'ebetsu',
                    'shinshinotsu', 'namporo', 'iwamizawa', 'naganuma',
                    'kitahiroshima', 'eniwa', 'chitose']
        tokyo = ['itabashi', 'tokorozawa', 'tachikawa', 'iruma', 'hanno',
                 'akishima', 'Hachiōji', 'Fuchū', 'mitaka', 'shinjuku',
                 'shibuya', 'sagamihara', 'machida', 'jokohama',
                 'atsugi', 'ayase', 'fujisawa', 'kamakura', 'zushi',
                 'hayama', 'miura', 'yokosuka', 'kawasaki', 'ōta',
                 'shinagawa', 'futtsu', 'kimitsu', 'kisarazu',
                 'sodegaura', 'ichihara', 'chiba', 'yotsukaido',
                 'sakura', 'yachiyo', 'funabashi', 'edogawa', 'matsudo',
                 'narita', 'sakae', 'inzai', 'kashiwa', 'toride', 'moriya',
                 'adachi', 'sōka', 'kawaguchi', 'saitama', 'koshigaya',
                 'noda', 'kasukabe', 'kawagoe', 'hidaka', 'tsurugashima',
                 'sakado', 'kuki']
        nust = ['windhoek', 'brakwater', 'seeis', 'aris', 'gocheganas',
                'groot aub', 'oamities']

        locdict = {'Tampere': tampere, 'Helsinki': helsinki, 'Turku': turku,
                   'Oulu': oulu, 'Vaasa': vaasa, 'Glasgow': glasgow,
                   'London': london,
                   'Bragança': bragança, 'Santarem': santarem,
                   'Budapest': budapest,
                   'Ostrava': ostrava, 'Prague': prague, 'Hokkaido': hokkaido,
                   'Tokyo': tokyo, 'NUST': nust}
        return locdict

    cities = cities_near_locations()
    for row in df.itertuples():
        if row.city:
            if len(row.locations) > 0:
                was_here = False
                for i in row.locations:
                    if i.lower() in row.city.lower():
                        df.at[row.Index,'locations'] = 1
                        was_here = True
                        break
                    elif i in cities:
                        for j in cities[i]:
                            if j.lower() in row.city.lower():
                                df.at[row.Index, 'locations'] = 1
                                was_here = True
                                break

                if was_here == False:
                    df.at[row.Index, 'locations'] = 0
            else:
                df.at[row.Index, 'locations'] = 2
        else:
            if row.locations:
                if 'Online' in row.locations:
                    df.at[row.Index, 'locations'] = 1
                else:
                    df.at[row.Index, 'locations'] = 2
            else:
                df.at[row.Index,'locations'] = 2
    return df['locations']
#clean_data()
