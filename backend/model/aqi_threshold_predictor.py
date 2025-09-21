
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib

# Load and clean data
def load_data(file_path):
    df = pd.read_excel(file_path)
    df = df[['AGE', 'GENDER', 'DIAGNOSISNAME', 'AQI', 'PATIENT_STATUS']].dropna()
    df = df[df['AQI'] > 0]
    df = df.sample(n=1000, random_state=42)  # sample for performance
    return df

# Train model
def train_model(df):
    X = df[['AGE', 'GENDER', 'DIAGNOSISNAME']]
    y = df['AQI']

    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), ['DIAGNOSISNAME'])],
        remainder='passthrough'
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Model trained. MAE: {mae:.2f}")

    joblib.dump(model, "aqi_safe_threshold_model.pkl")
    print("Model saved as 'aqi_safe_threshold_model.pkl'")
    return model

# Predict AQI
def get_safe_aqi(model, age, gender, diagnosis):
    input_df = pd.DataFrame([{
        'AGE': age,
        'GENDER': gender,
        'DIAGNOSISNAME': diagnosis
    }])
    prediction = model.predict(input_df)[0]
    return prediction

# Main execution
if __name__ == "__main__":
    data_file = "copd_generated_data 2.xlsx"
    df = load_data(data_file)
    model = train_model(df)

    # Example prediction
    age = 65
    gender = 1  # 1 = Male, 0 = Female
    diagnosis = "COPD"
    safe_aqi = get_safe_aqi(model, age, gender, diagnosis)
    print(f"Recommended safe AQI threshold for {age}y {'Male' if gender == 1 else 'Female'} with {diagnosis}: {safe_aqi:.2f}")
