import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib


# Extract features from a password for strength analysis
def extractFeatures(password):
    features = {
        'length': len(password),
        'has_upper': int(any(c.isupper() for c in password)),
        'has_lower': int(any(c.islower() for c in password)),
        'has_digit': int(any(c.isdigit() for c in password)),
        'has_symbol': int(any(c in '!@#$%^&*()_+' for c in password)),
        'repeated_chars': sum(password.count(c) > 1 for c in set(password))
    }
    return features


# Train the password strength model
def trainModel():
    df = pd.read_csv(r'../Input Files/password_model_training.csv')
    df = df.dropna()
    features_df = df['password'].apply(extractFeatures).apply(pd.Series)
    df = pd.concat([df, features_df], axis=1)
    X = df.drop(["Unnamed: 0", "password", "strength"], axis=1)
    y = df['strength']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    rf_pipeline = Pipeline([
        ('rf', RandomForestClassifier())
    ])
    rf_pipeline.fit(X_train, y_train)
    joblib.dump(rf_pipeline, r'../Output Files/password_strength_model.pkl')


# Predict the strength of a password using the trained model
def predictPasswordStrength(password, model):
    features = extractFeatures(password)
    features_df = pd.DataFrame([features])
    prediction = model.predict(features_df)
    return prediction[0]
