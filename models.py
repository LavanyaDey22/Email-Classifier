import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def train_and_save_model(data_path='data/processed_emails.csv', model_path='model/email_classifier.pkl'):
    print("✅ Loading processed data...")
    df = pd.read_csv(data_path)

    X = df['masked_email']
    y = df['type']

    print("✅ Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("✅ Creating pipeline...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    print("✅ Training model...")
    pipeline.fit(X_train, y_train)

    print("✅ Evaluating model...")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    print(f"✅ Saving model to {model_path}")
    joblib.dump(pipeline, model_path)

if __name__ == "__main__":
    train_and_save_model()