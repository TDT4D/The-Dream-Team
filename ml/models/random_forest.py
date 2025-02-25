
from data_handling import data_cleaning
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from utils import storage
import pandas as pd

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

    #Create test results dataframe
    test_results = X_test.copy()
    test_results['Predicted_Relation'] = y_pred
    test_results['Score'] = (y_pred / y_pred.max()) * 100  #Normalize scores to 0-100


    #Save results to storage
    storage.save_json(test_results.to_dict(orient="records"), save_name)

    print(f"Model trained successfully. Predictions saved as '{save_name}.json'")

    return test_results.to_dict(orient="records")  #Return predictions as a dictionary


