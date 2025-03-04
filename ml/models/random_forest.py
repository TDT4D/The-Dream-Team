
from data_handling import data_cleaning
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from utils import storage
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold, KFold
from imblearn.over_sampling import SMOTE


# Random Forest -malli
def randomforest():
    data = data_cleaning.clean_data_v2()
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

def randomforest_v2(load="rawData", save_name="student_scores", cleaning:bool=True):
    """
    Trains a Random Forest model to predict the 'relation' of a student to a project.

    - Uses cleaned, encoded data from `clean_data_v2()`
    - Splits data into train & test sets
    - Trains a Random Forest model
    - Evaluates accuracy of the model
    - Generates scores and saves the predictions to storage

    Returns:
        dict: A dictionary containing test predictions and their scores.
    """
    if cleaning:
        data = data_cleaning.clean_data_v2(load)
    else:
        data=load

    #Check if data was loaded correctly
    if data is None or len(data) == 0:
        print("ERROR: No data available for training.")
        return None

    df = pd.DataFrame(data)  # Convert to DataFrame

    print("Columns in cleaned data:", df.columns)  #Debugging

    #Identify One-Hot Encoded `relation_*` Columns
    relation_columns = [col for col in df.columns if "relation_" in col]

    if len(relation_columns) == 0:
        print("ERROR: 'relation' column missing after data cleaning!")
        return None

    #Convert One-Hot Encoded `relation_*` Columns Back to a Single `relation` Column
    df['relation'] = df[relation_columns].idxmax(axis=1)  # Gets the column with max value (1)
    df['relation'] = df['relation'].apply(lambda x: int(x.split("_")[-1]))  # Extracts numerical value

    #Drop one-hot relation columns after merging them
    df = df.drop(columns=relation_columns)

    #Define feature set (excluding relation)
    X = df.drop(columns=['relation'])  # Remove target column
    y = df['relation']  # Target column

    #Split into training & testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Train the Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    #Predict on the test set
    y_pred = model.predict(X_test)

    #Compute accuracy
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"\nModel Training Accuracy: {accuracy:.2f}%\n")
    print("More detailed info about model:\n")
    print(classification_report(y_test, y_pred, zero_division=1, labels=[0, 1, 2]))
    #Create test results dataframe
    test_results = X_test.copy()
    test_results['Predicted_Relation'] = y_pred
    test_results['Score'] = (y_pred / y_pred.max()) * 100  #Normalize scores to 0-100


    #Save results to storage
    storage.save_json(test_results.to_dict(orient="records"), save_name)

    print(f"Model trained successfully. Predictions saved as '{save_name}.json'")

    return test_results.to_dict(orient="records")  #Return predictions as a dictionary

def meta_model_v1(load="rawData", save_name="student_scores", cleaning:bool=True):
    """
    Trains a Random Forest model to predict the 'relation' of a student to a project.

    - Uses cleaned, encoded data from `clean_data_v2()`
    - Splits data into train & test sets
    - Trains XGBoost, AdaBoost, KNN and NaiveBayes base models
        and XGBoost meta-model
    - Also balances data, because lack of potential and selected students for now
    - Evaluates accuracy of the model
    - Generates scores and saves the predictions to storage

    Returns:
        dict: A dictionary containing test predictions and their scores.
    """
    if cleaning:
        data = data_cleaning.clean_data_v2(load)
    else:
        data=load

    #Check if data was loaded correctly
    if data is None or len(data) == 0:
        print("ERROR: No data available for training.")
        return None

    df = pd.DataFrame(data)  # Convert to DataFrame

    print("Columns in cleaned data:", df.columns)  #Debugging

    #Identify One-Hot Encoded `relation_*` Columns
    relation_columns = [col for col in df.columns if "relation_" in col]

    if len(relation_columns) == 0:
        print("ERROR: 'relation' column missing after data cleaning!")
        return None

    #Convert One-Hot Encoded `relation_*` Columns Back to a Single `relation` Column
    df['relation'] = df[relation_columns].idxmax(axis=1)  # Gets the column with max value (1)
    df['relation'] = df['relation'].apply(lambda x: int(x.split("_")[-1]))  # Extracts numerical value

    #Drop one-hot relation columns after merging them
    df = df.drop(columns=relation_columns)

    #Define feature set (excluding relation)
    X = df.drop(columns=['relation'])  # Remove target column
    y = df['relation']  # Target column

    # Balance data, because lack of potential and selected students for now
    smote = SMOTE(random_state=42)
    X, y = smote.fit_resample(X, y)

    """
    Model parameters:

    XGBoost:
        n_estimators - Bigger values makes the models more complex and slower, but too big values lead to overlearning
        max_depth    - Lower value helps to avoid overlearning, but too small makes it hard to learn complex
                       relations
    AdaBoost:
        n_estimators - Bigger values makes the models more complex and slower, but too big values lead to overlearning
        random_state - If it's predefined to for example 42, the results are always the same with same data
    
    KNN:
        n_neighbours - Smaller amount of neighbours lead to overlearnign and too many neighbours can make the model 
                       too simple

    NaiveBayes       - Based on Gaussian normal distribution

    K-fold:
        n_splits     - To how many folds data is divided to. Bigger value is slower to count, but also more 
                       reliable than smaller
        shuffle      - Is data shuffled before use
    """
    base_models = {
        "XGBoost": XGBClassifier(n_estimators=50, max_depth=3),
        "AdaBoost": AdaBoostClassifier(n_estimators=50, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "NaiveBayes": GaussianNB()
    }
    meta_model = XGBClassifier(n_estimators=50, max_depth=3)

    # K-fold for base-models
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


    stacked_X = np.zeros((len(y), len(base_models)))

    # Base models training
    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        for model_idx, (name, model) in enumerate(base_models.items()):
            model.fit(X_train, y_train)
            stacked_X[test_idx, model_idx] = model.predict(X_test)


    # K-fold for meta-model
    kf = KFold(n_splits=K, shuffle=True, random_state=42)
    meta_preds = np.zeros(len(y))

    # Meta-model training
    for fold_idx, (train_idx, test_idx) in enumerate(kf.split(stacked_X, y)):
        X_meta_train, X_meta_test = stacked_X[train_idx], stacked_X[test_idx]
        y_meta_train, y_meta_test = y.iloc[train_idx], y.iloc[test_idx]

        meta_model.fit(X_meta_train, y_meta_train)
        meta_preds[test_idx] = meta_model.predict(X_meta_test)

    #Compute accuracy
    accuracy = accuracy_score(y, meta_preds) * 100
    print(f"\nModel Training Accuracy: {accuracy:.2f}%\n")

    print("More detailed info about model:\n")
    print(classification_report(y, meta_preds, zero_division=1, labels=[0, 1, 2]))

    # Create test results dataframe so that predicted relation can be estimated
    test_results = pd.DataFrame(stacked_X)

    test_results['Predicted_Relation'] = meta_preds
    test_results['Score'] = (meta_preds / meta_preds.max()) * 100  #Normalize scores to 0-100

    #Save results to storage
    storage.save_json(test_results.to_dict(orient="records"), save_name)

    print(f"Model trained successfully. Predictions saved as '{save_name}.json'")

    return test_results.to_dict(orient="records")  #Return predictions as a dictionary