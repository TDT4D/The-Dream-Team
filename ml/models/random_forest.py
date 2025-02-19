
from ml.data import data_cleaning
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
# Random Forest -malli
def randomforest():
    data = siivooja.clean_data()
    data['tags'] = data['tags'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    data['themes'] = data['themes'].apply(lambda x: len(x) if isinstance(x, list) else 0)

    X = data[['tags', 'themes', 'homeUniversity', 'degreeLevelType', 'studiesField']]
    y = data['relation']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Ennustetaan testijoukolle
    y_pred = model.predict(X_test)

    # Tulostetaan ennustettu relation (0=interested, 1=potential ja 2=selected
    # ja alkeellinen score
    test_results = X_test.copy()
    test_results['Predicted_Relation'] = y_pred
    test_results['Score'] = (test_results['Predicted_Relation'] / 3) * 100  # 0-100
    # Palautetaan aluksi vain relaatio ja lisätään 
    # piakkoin eri funktiot eri palautuksille
    return int(test_results.iloc[0]['Predicted_Relation'])