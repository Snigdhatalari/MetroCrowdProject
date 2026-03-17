# Backend/crowd/ml_model.py

import pandas as pd
import joblib

from crowd.models import CrowdRecord
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# ✅ STEP 1: Load Data from Database
def load_data():
    data = CrowdRecord.objects.all().values()

    if not data:
        print("No data found in database")
        return None

    df = pd.DataFrame(data)

    # Convert datetime
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Extract features
    df['hour'] = df['created_at'].dt.hour
    df['day'] = df['created_at'].dt.dayofweek

    return df


# ✅ STEP 2: Train Model
def train_model():
    df = load_data()

    if df is None or len(df) < 5:
        print("Not enough data to train model")
        return None

    # Features (INPUT)
    X = df[['hour', 'day', 'people_count']]

    # Target (OUTPUT)
    y = df['crowd_status']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Accuracy (for debugging)
    accuracy = model.score(X_test, y_test)
    print(f"Model trained successfully! Accuracy: {accuracy:.2f}")

    return model


# ✅ STEP 3: Save Model
def save_model():
    model = train_model()

    if model:
        joblib.dump(model, "crowd_model.pkl")
        print("Model saved as crowd_model.pkl")


# ✅ STEP 4: Load Model (Reusable)
def load_model():
    try:
        model = joblib.load("crowd_model.pkl")
        return model
    except:
        print("Model not found. Train and save first.")
        return None


# ✅ STEP 5: Predict Crowd
def predict_crowd(hour, day, people_count):
    model = load_model()

    if model is None:
        return "Model not available"

    prediction = model.predict([[hour, day, people_count]])

    return prediction[0]