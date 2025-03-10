
from data_handling import get_cleaner
from utils import storage
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold, KFold
from imblearn.over_sampling import SMOTE

MODEL_NAME = "meta_model"

def train(load="rawData", model_name=MODEL_NAME, cleaning:bool=True):
    """
    Trains a Meta model to predict the 'relation' of a student to a project.

    - Cleans data if needed
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
        data = get_cleaner("default_cleaner").clean_data(load)
    else:
        data=storage.load_json(load)

    #Check if data was loaded correctly
    if data is None or len(data) == 0:
        print("ERROR: No data available for training.")
        return None

    #Additional check to ensure clean_data is not just a file name
    if isinstance(data, str):
        print(f"ERROR: Expected data but received a file name: {data}")
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

    base_models = {
        "XGBoost": XGBClassifier(n_estimators=50, max_depth=3),
        "AdaBoost": AdaBoostClassifier(n_estimators=50, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "NaiveBayes": GaussianNB()
    }
    meta_model = XGBClassifier(n_estimators=50, max_depth=3)

    # K-fold for base-models
    K = 5
    skf = StratifiedKFold(n_splits=K, shuffle=True, random_state=42)


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

    if storage.save_model(meta_model, model_name):
        print(f"Model '{model_name}' trained and saved succesfully")
        return True
    else:
        print("Error saving the model")
        return False

def predict(load="rawData", model_name=MODEL_NAME, score_file="student_scores_meta_default", cleaning:bool=True):
    """
    Loads a trained meta-model and makes predictions using the storage utility.
    Saves predictions to a JSON file.
    
    Args:
        data (str): Raw or pre-cleaned data.
        model_name (str): Name of the saved model file to load.
        score_file (str): Name of the file to save predictions.
        cleaning (bool): Whether to clean data before prediction.
        
    Returns:
        dict: A dictionary containing predictions and scores.
    """

    #load the model
    meta_model = storage.load_model(model_name)

    if not meta_model:
        print(f"Model '{model_name}' could not be loaded.")
        return None
    
    if cleaning:
        data = get_cleaner("default_cleaner").clean_data(load)
    else:
        data=storage.load_json(load)

    #Additional check to ensure clean_data is not just a file name
    if isinstance(data, str):
        print(f"ERROR: Expected data but received a file name: {data}")
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

    #Recreate base models (using the same configuration as during training)
    base_models = {
        "XGBoost": XGBClassifier(n_estimators=50, max_depth=3),
        "AdaBoost": AdaBoostClassifier(n_estimators=50, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "NaiveBayes": GaussianNB()
    }

    #Generate stacked predictions from base models
    stacked_X = np.zeros((len(X), len(base_models)))

    for model_idx, (name, model) in enumerate(base_models.items()):
        print(f"Fitting base model '{name}' for stacking...")
        model.fit(X, y)  # Fit the model on the full dataset
        stacked_X[:, model_idx] = model.predict(X)

    #Predict using the meta-model
    y_pred = meta_model.predict(stacked_X)

    results = X.copy()
    results['Predicted_Relation'] = y_pred
    results['Score'] = (y_pred / y_pred.max()) * 100

    scores = results.to_dict(orient="records")
    storage.save_json(scores, score_file)

    print(f"Predictions successfully saved as '{score_file}.json'")
    return scores

def t_predict(data="rawData", model_name=f"{MODEL_NAME}_t", score_file="student_scores_meta_t_default", cleaning:bool=True):
    """
    Trains a new meta-model and immediately makes predictions on the provided data.
    
    Args:
        data (str): Raw or pre-cleaned data.
        model_name (str): Name to save the trained model.
        score_file (str): Name of the file to save predictions.
        cleaning (bool): Whether to clean data before training/prediction.
        
    Returns:
        dict: A dictionary containing predictions and scores.
    """
    
    #Clean data and change the file name to proper
    if cleaning:
        get_cleaner("default_cleaner").clean_data(data, "t_meta_predict_clean")
        data = "t_meta_predict_clean"

    train(data, model_name, cleaning=False)
    return predict(data, model_name, score_file, cleaning=False)


