from data_handling import motivation_data_cleaning_version2
from data_handling import get_cleaner
from utils import storage
from sklearn.preprocessing import MinMaxScaler
from imblearn.combine import SMOTEENN
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from pathlib import Path

MODEL_NAME = "motivation_model"
data_dir = Path(__file__).resolve().parent / "data"

def train(load="rawData", model_name=MODEL_NAME, cleaning:bool=True):
    """
    Trains a one-vs-rest model to predict the motivation of a student to a project.

    - Cleans data if needed
    - Splits data into train & test sets
    - Trains Pipeline with Standardscaler and Randomforest
    - Also balances data, because lack of potential and selected students for now
    - Evaluates accuracy of the model
    - Generates scores for motivation to storage

    Returns:
        bool: Confirmation of model save.
    """

    # Check if data file is found
    if not (data_dir / load).exists():
        return None

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

    # Modify y to combine every class to 0 except Droputs to class 1
    y_binary = y.apply(lambda x: 1 if x == 3 else 0)

    # Split data for trainging and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42, stratify=y)

    # SMOTEENN tested to be best out of different SMOTE's, because of unbalanced data
    smoteenn = SMOTEENN(random_state=42)
    X_train_res, y_train_res = smoteenn.fit_resample(X_train, y_train)

    # Create pipeline with standardscaler and Randomforest
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(
            random_state=42,
            class_weight='balanced',
            n_estimators=100,
            max_depth=10
        ))
    ])

    # Train, predict results and print accuracy
    pipeline.fit(X_train_res, y_train_res)
    y_pred = pipeline.predict(X_test)

    print("More detailed info about model:\n")
    print(classification_report(y_test, y_pred))

    if storage.save_model(pipeline, model_name):
        print(f"Model '{model_name}' trained and saved succesfully")
        return True
    else:
        print("Error saving the model")
        return False

def predict(load="rawData", model_name=MODEL_NAME, score_file="motivation_student_scores_meta_default", cleaning:bool=True):
    """
    Loads a trained one-vs-rest and makes predictions using the storage utility.
    Saves predictions to a JSON file.

    Args:
        data (str): Raw or pre-cleaned data.
        model_name (str): Name of the saved model file to load.
        score_file (str): Name of the file to save predictions.
        cleaning (bool): Whether to clean data before prediction.

    Returns:
        dict: A dictionary containing predictions and scores.
    """

    # Check if data file is found
    if not (data_dir / load).exists():
        return None

    # load the model
    stacking_model = storage.load_model(model_name)

    if not stacking_model:
        print(f"Model '{model_name}' could not be loaded.")
        return None

    if cleaning:
        data = motivation_data_cleaning_version2.clean_data(load)
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
    X = df.drop(columns=['relation'])

    # Ennustetaan todennäköisyydet luokalle 3
    proba_class3 = stacking_model.predict_proba(X)[:, 1]

    # Lasketaan "ei-luokka-3" -score
    not_class3_score = 1 - proba_class3
    scaler = MinMaxScaler(feature_range=(0, 100))
    not_class3_score_scaled = scaler.fit_transform(not_class3_score.reshape(-1, 1)).flatten()
    # Create dataframe and store it to dict
    results = X.copy()
    results['motivation'] = not_class3_score_scaled
    scores = results.to_dict(orient="records")
    storage.save_json(scores, score_file)

    print(f"Predictions successfully saved as '{score_file}.json'")
    return scores

def t_predict(data="rawData", model_name=f"{MODEL_NAME}_t", score_file="motivation_student_scores_meta_t_default", cleaning:bool=True):
    """
    Trains one-vs-rest and immediately makes predictions on the provided data.

    Args:
        data (str): Raw or pre-cleaned data.
        model_name (str): Name to save the trained model.
        score_file (str): Name of the file to save predictions.
        cleaning (bool): Whether to clean data before training/prediction.

    Returns:
        dict: A dictionary containing predictions and scores.
    """
    if cleaning:
        get_cleaner("motivation_data_cleaning_version2").clean_data(data, "motivation_t_meta_predict_clean")
        data = "motivation_t_meta_predict_clean"
    train(data, model_name, cleaning=False)
    return predict(data, model_name, score_file, cleaning=False)