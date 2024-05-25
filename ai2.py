import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
import ast

# Read data from CSV files
def read_data_from_csv(incompatible_file, compatible_file):
    incompatible_data = pd.read_csv(incompatible_file)
    compatible_data = pd.read_csv(compatible_file)
    return incompatible_data, compatible_data

# Prepare data for training
def prepare_data(incompatible_data, compatible_data):
    illnesses = set(incompatible_data['Illness']).union(set(compatible_data['Illness']))

    data = []
    for illness in illnesses:
        row = {'Illness': illness}
        if illness in set(incompatible_data['Illness']):
            row['Incompatible Drugs'] = incompatible_data[incompatible_data['Illness'] == illness]['incompatible Drugs'].values[0]
        else:
            row['Incompatible Drugs'] = "[]"

        if illness in set(compatible_data['Illness']):
            row['Compatible Drugs'] = compatible_data[compatible_data['Illness'] == illness]['Compatible Drugs'].values[0]
        else:
            row['Compatible Drugs'] = "[]"

        data.append(row)

    return pd.DataFrame(data)

# Extract features and labels
def extract_features_and_labels(data):
    data['Incompatible Drugs'] = data['Incompatible Drugs'].apply(ast.literal_eval)
    data['Compatible Drugs'] = data['Compatible Drugs'].apply(ast.literal_eval)

    all_drugs = set([drug for sublist in data['Incompatible Drugs'] for drug in sublist] +
                    [drug for sublist in data['Compatible Drugs'] for drug in sublist])

    X = data['Illness']
    y_incompatible = pd.DataFrame({drug: data['Incompatible Drugs'].apply(lambda x: int(drug in x)) for drug in all_drugs})
    y_compatible = pd.DataFrame({drug: data['Compatible Drugs'].apply(lambda x: int(drug in x)) for drug in all_drugs})

    return X, y_incompatible, y_compatible, all_drugs

# Define and train the model
def train_model(X, y_incompatible, y_compatible):
    vectorizer = CountVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model_incompatible = MultiOutputClassifier(RandomForestClassifier(random_state=0))
    model_incompatible.fit(X_vec, y_incompatible)

    model_compatible = MultiOutputClassifier(RandomForestClassifier(random_state=0))
    model_compatible.fit(X_vec, y_compatible)

    return vectorizer, model_incompatible, model_compatible

# Predict compatible and incompatible drugs for an illness
def predict_drugs_for_illness(vectorizer, model_incompatible, model_compatible, all_drugs, illness):

    X_vec = vectorizer.transform([illness])

    incompatible_predictions = model_incompatible.predict(X_vec)[0]
    compatible_predictions = model_compatible.predict(X_vec)[0]

    incompatible_drugs = [drug for drug, pred in zip(all_drugs, incompatible_predictions) if pred == 1]
    compatible_drugs = [drug for drug, pred in zip(all_drugs, compatible_predictions) if pred == 1]

    return compatible_drugs, incompatible_drugs

# Check drug compatibility with current medications
drug_interactions_df = pd.read_csv('drug_interactions_binary.csv')
def check_drug_compatibility(current_drug, drugs_taken):
    if not drugs_taken:
        return True

    incompatible_interactions = drug_interactions_df[
        (drug_interactions_df['Drug1'] == current_drug) &
        (drug_interactions_df['Drug2'].isin(drugs_taken)) &
        (drug_interactions_df['interaction'] == 0)
        ]

    return incompatible_interactions.empty

# Read age compatibility data from CSV file
def read_age_compatibility(age_file):
    age_data = pd.read_csv(age_file)
    return age_data


# Check drug compatibility with age
def check_age_compatibility(age, age_recommendations):
    if pd.isnull(age_recommendations):
        return True
    age_min = int(age_recommendations)
    return age >= age_min



# Check medication compatibility
def check_medication_compatibility(patient_age, patient_illness, current_medication, data):
    for index, row in data.iterrows():
        if not check_age_compatibility(patient_age, row.get('Age', None)):
            return False, "Ce médicament n'est pas recommandé pour cet âge."
        if not check_drug_compatibility(current_medication, row.get('Incompatible Drugs', [])):
            incompatible_drugs = row.get('Incompatible Drugs', [])
            # Pass all required arguments to predict_drugs_for_illness function
            alternative_drugs = predict_drugs_for_illness(vectorizer, model_incompatible, model_compatible, all_drugs, patient_illness)
            if alternative_drugs:
                # Convert each item in alternative_drugs to string
                alternative_drugs = [str(drug) for drug in alternative_drugs]
                return False, "Ce médicament est incompatible avec un autre médicament que le patient prend déjà. Voici des alternatives compatibles : " + ', '.join(alternative_drugs)
            else:
                return False, "Ce médicament est incompatible avec un autre médicament que le patient prend déjà."
        if not check_drug_compatibility(patient_illness, row.get('Incompatible Illnesses', [])):
            return False, "Ce médicament est incompatible avec une maladie que le patient a."
    return True, "Ce médicament est compatible."



# File paths for the CSV files
incompatible_file = 'illness_xdrugs.csv'
compatible_file = 'illness_drugs.csv'

# Read data from CSV files
incompatible_data, compatible_data = read_data_from_csv(incompatible_file, compatible_file)

# Prepare data for training
data = prepare_data(incompatible_data, compatible_data)

# Extract features and labels
X, y_incompatible, y_compatible, all_drugs = extract_features_and_labels(data)

# Train the model
vectorizer, model_incompatible, model_compatible = train_model(X, y_incompatible, y_compatible)




# Example usage
patient_age = 30
patient_illness = "Hypertension"
current_medication = "Albuterol"
#Atorvastatin
compatible, message = check_medication_compatibility(patient_age, patient_illness, current_medication, data)
print(message)