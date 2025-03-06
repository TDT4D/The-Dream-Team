from data_handling import data_cleaning
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from utils import storage
import pandas as pd


def train(data="rawData", model_name="randomforest_v2", cleaning:bool=True):
    """
    Trains a Random Forest model and saves it using storage utils
    
    Args:
        data (str): Raw data or pre-cleaned data.
        save_name (str): Name to save the trained model.
        
    Returns:
        str: Confirmation of model save.
    """
    
    if cleaning:
        clean_data = data_cleaning.clean_data_v2(data)
    else:
        clean_data = data
    
    if clean_data is None or len(clean_data) == 0:
        print("ERROR: No data available for training.")
        return None

    #Training ___________________________________

    df = pd.DataFrame(clean_data)  # Convert to DataFrame

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

    #____________________________________________

    #Predict on the test set
    y_pred = model.predict(X_test)

    #Compute accuracy
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f"\nModel Training Accuracy: {accuracy:.2f}%\n")
    print("More detailed info about model:\n")
    print(classification_report(y_test, y_pred, zero_division=1, labels=[0, 1, 2]))

    if storage.save_model(model, model_name):
        return f"Model '{model_name}' trained with accuracy: {accuracy:.2f}% and saved successfully."
    else:
        return "Error saving the model."

def predict(data="rawData", model_name="randomforest_v2", score_file="student_scores_default", cleaning:bool=True):
    """
    - Loads a trained Random Forest model and makes predictions using the storage utility.
    - Saves predictions
    
    Args:
        data (str): Raw data or pre-cleaned data.
        model_name (str): Name of the saved model file to load.
        save_name (str): Name of the file to save predictions.
        cleaning (bool): check if cleaning of data is needed
        
    Returns:
        dict: A dictionary containing test predictions and their scores.
    """

    model = storage.load_model(model_name)

    if model is None:
        print(f"Model '{model_name}' could not be loaded.")
        return None

    if cleaning:
        cleaned_data = data_cleaning.clean_data_v2(data)
    else:
        cleaned_data=data

    if cleaned_data is None or len(cleaned_data) == 0:
        print("ERROR: No data available for prediction.")
        return None

    df = pd.DataFrame(cleaned_data)

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

    y_pred = model.predict(X)

    #Create test results dataframe
    results = X.copy()
    results['Predicted_Relation'] = y_pred
    results['Score'] = (y_pred / y_pred.max()) * 100  #Normalize scores to 0-100

    #Save results to storage
    scores = results.to_dict(orient="records")

    storage.save_json(scores, score_file)

    print(f"Predictions succesfully saved as '{score_file}.json'")
    return scores  #Return predictions as a dictionary

def t_predict(data="rawData", model_name="randomforest_v2_t", score_file="student_scores_t_default", cleaning:bool=True):
    """
    Trains a new Random Forest model and predicts the 'relation' of a student to a project.

    - Uses cleaned, encoded data from `clean_data_v2()`
    - Splits data into train & test sets
    - Trains a Random Forest model
    - Evaluates accuracy of the model
    - Generates scores and saves the predictions to storage

    Returns:
        dict: A dictionary containing test predictions and their scores.
    """
    
    #Avoid redundant cleaning
    if cleaning:
        cleaned_data = data_cleaning.clean_data_v2(data)
    else:
        cleaned_data=data

    train(cleaned_data, model_name, cleaning=False)

    return predict(cleaned_data, model_name, score_file, cleaning=False)  #Return predictions as a dictionary

