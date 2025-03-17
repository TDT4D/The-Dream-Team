import data_cleaning_version4
import storage
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.model_selection import train_test_split
from imblearn.ensemble import BalancedBaggingClassifier
from sklearn.preprocessing import MinMaxScaler

MODEL_NAME = "meta_model"

def train(load="rawData", model_name=MODEL_NAME, cleaning:bool=True):
    """
    Trains a Meta model to predict the 'relation' of a student to a project.

    - Cleans data if needed
    - Splits data into train & test sets
    - Trains XGBoost, and Random Forest base models
        and XGBoost meta-model and Stacking model to finalize results
    - Also balances data, because lack of potential and selected students for now
    - Evaluates accuracy of the model
    - Generates scores and saves the predictions to storage

    Returns:
        dict: A dictionary containing test predictions and their scores.
    """
    if cleaning:
        data = get_cleaner("default_cleaner").clean_data(load)
    else:
        data = storage.load_json(load)

    # Check if data was loaded correctly
    if data is None or len(data) == 0:
        print("ERROR: No data available for training.")
        return None

    # Additional check to ensure clean_data is not just a file name
    if isinstance(data, str):
        print(f"ERROR: Expected data but received a file name: {data}")
        return None

    df = pd.DataFrame(data)  # Convert to DataFrame

    print("Columns in cleaned data:", df.columns)  # Debugging

    # Identify One-Hot Encoded `relation_*` Columns
    relation_columns = [col for col in df.columns if "relation_" in col]

    if len(relation_columns) == 0:
        print("ERROR: 'relation' column missing after data cleaning!")
        return None

    # Convert One-Hot Encoded `relation_*` Columns Back to a Single `relation` Column
    df['relation'] = df[relation_columns].idxmax(axis=1)  # Gets the column with max value (1)
    df['relation'] = df['relation'].apply(lambda x: int(x.split("_")[-1]))  # Extracts numerical value

    # Drop one-hot relation columns after merging them
    df = df.drop(columns=relation_columns)

    # Define feature set (excluding relation)
    X = df.drop(columns=['relation'])  # Remove target column
    y = df['relation']  # Target column

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Balance data, because lack of potential and selected students for now
    smote = SMOTE(sampling_strategy="auto", random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)
    sample_weights = compute_sample_weight(class_weight="balanced", y=y_train)


    base_models = {
        "XGBoost": BalancedBaggingClassifier(
                                    estimator=XGBClassifier(
                                            n_estimators=50, # Increasing this value might make model better,
                                                             # but increases risk over overfitting
                                            max_depth=3), # Increasing this value gives model change to make more
                                                          # complicated decisions, but increases risk over overfitting
                                    sampling_strategy="not majority", # Resample all classes but the majority class
                                    random_state=42),
        "RandomForest": BalancedBaggingClassifier(
                                    estimator=RandomForestClassifier(
                                        n_estimators=100,
                                        max_depth=5),
                                        sampling_strategy="not majority",
                                        random_state=42)
    }
    meta_model = XGBClassifier(n_estimators=50, max_depth=3)

    # Stacking model to blend model predictions
    stacking_model = StackingClassifier(
        estimators=list(base_models.items()),
        final_estimator=meta_model
    )

    # Train stacking-model for base models
    stacking_model.fit(X_train, y_train)

    # Train stacking-model for meta-model with weighted samples
    stacking_model.final_estimator_.fit(
        stacking_model.transform(X_train), y_train, sample_weight=sample_weights
    )

    # Predict with test data and print info about details about stacking model
    y_pred = stacking_model.predict(X_test)

    stacking_accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"\nModel Training Accuracy: {stacking_accuracy:.2f}%\n")

    print("More detailed info about model:\n")
    print(classification_report(y_test, y_pred, zero_division=1, labels=[0, 1, 2]))

    if storage.save_model(stacking_model, model_name):
        print(f"Model '{model_name}' trained and saved succesfully")
        return True
    else:
        print("Error saving the model")
        return False

def predict(load="rawData", model_name=MODEL_NAME, score_file="student_scores_meta_default", cleaning:bool=True):
    """
    Loads a trained stacking-model and makes predictions using the storage utility.
    Saves predictions to a JSON file.

    Args:
        data (str): Raw or pre-cleaned data.
        model_name (str): Name of the saved model file to load.
        score_file (str): Name of the file to save predictions.
        cleaning (bool): Whether to clean data before prediction.

    Returns:
        dict: A dictionary containing predictions and scores.
    """

    # load the model
    stacking_model = storage.load_model(model_name)

    if not stacking_model:
        print(f"Model '{model_name}' could not be loaded.")
        return None

    if cleaning:
        data = data_cleaning_version4.clean_data(load)
    else:
        data = storage.load_json(load)

    # Additional check to ensure clean_data is not just a file name
    if isinstance(data, str):
        print(f"ERROR: Expected data but received a file name: {data}")
        return None

    df = pd.DataFrame(data)  # Convert to DataFrame

    print("Columns in cleaned data:", df.columns)  # Debugging

    # Identify One-Hot Encoded `relation_*` Columns
    relation_columns = [col for col in df.columns if "relation_" in col]

    if len(relation_columns) == 0:
        print("ERROR: 'relation' column missing after data cleaning!")
        return None

    # Convert One-Hot Encoded `relation_*` Columns Back to a Single `relation` Column
    df['relation'] = df[relation_columns].idxmax(axis=1)  # Gets the column with max value (1)
    df['relation'] = df['relation'].apply(lambda x: int(x.split("_")[-1]))  # Extracts numerical value

    # Drop one-hot relation columns after merging them
    df = df.drop(columns=relation_columns)
    X = df.drop(columns=['relation'])

    # Predict with stacking-model
    y_pred = stacking_model.predict(X)

    # Give score to students
    probabilities_list = stacking_model.predict_proba(X)[:, 1]
    scaler = MinMaxScaler(feature_range=(0, 100))
    probabilities_scaled = scaler.fit_transform(probabilities_list.reshape(-1, 1)).flatten()

    # Create dataframe and store it to dict
    results = X.copy()
    results['Predicted_Relation'] = y_pred
    results['Score'] = probabilities_scaled

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

    # Clean data and change the file name to proper
    if cleaning:
        get_cleaner("default_cleaner").clean_data(data, "t_meta_predict_clean")
        data = "t_meta_predict_clean"
    train(data, model_name, cleaning=False)
    return predict(data, model_name, score_file, cleaning=False)