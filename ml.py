import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset from CSV
csv_path = r"asserts\crop_yield_data.csv"
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print("❌ CSV file not found. Check your path.")
    exit()

# Check expected columns
expected_cols = ["Soil Moisture", "Humidity", "Temperature", 
                 "Light Intensity", "Month", "Status"]
if not all(col in df.columns for col in expected_cols):
    print("❌ CSV is missing required columns.")
    exit()

# Encode the month column
# le = LabelEncoder()
# df["Month"] = le.fit_transform(df["Month"])

# Split features and labels
X = df.drop("Status", axis=1)
y = df["Status"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train Decision Tree model
model =  RandomForestClassifier(class_weight='balanced')
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))
print(f"✅ Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

joblib.dump(model, "crop_yield_decision_tree_model.joblib")
print("✅ Model saved as crop_yield_decision_tree_model.joblib")