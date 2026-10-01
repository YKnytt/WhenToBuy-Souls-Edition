import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier

# Load the Elden Ring feature dataset
df = pd.read_csv("data/features/elden_ring.csv")

print("Rows:", len(df))
print("Columns:", len(df.columns))
print(df.head())

# Features the model will use
features = [
    "Price",
    "historical_low",
    "price_above_low",
    "percent_above_low",
    "days_since_price_change",
    "sales_last_365_days",
    "avg_price_last_365_days",
    "price_changes_last_365_days"
]

# X = information available when making the prediction
X = df[features]

# y = outcome we want the model to predict
y = df["cheaper_within_30_days"]

print("\nX shape:", X.shape)
print("y shape:", y.shape)

# Split chronologically: earliest 80% for training, latest 20% for testing
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))

print("Training period:", df["Date"].iloc[0], "to", df["Date"].iloc[split_index - 1])
print("Testing period:", df["Date"].iloc[split_index], "to", df["Date"].iloc[-1])

# Create the Logistic Regression baseline model
model = LogisticRegression(max_iter=1000)

# Train the model using only the historical training data
model.fit(X_train, y_train)
joblib.dump(model, "data/features/elden_ring_model.pkl")
print("Model saved.")

# Get predicted probabilities for the test data
probabilities = model.predict_proba(X_test)

print("\nProbability shape:", probabilities.shape)
print(probabilities[:5])

# Probability of a cheaper price within 30 days
probability_cheaper = probabilities[:, 1]

print("\nFirst 5 probabilities of a cheaper price:")
print(probability_cheaper[:5])

print("\nFirst 5 predictions vs actual:")
for i in range(5):
    print(
        "Predicted probability:", round(probability_cheaper[i], 3),
        "| Actual:", y_test.iloc[i]
    )

# Convert probabilities into binary predictions using the default 0.50 threshold
y_pred = (probability_cheaper >= 0.50).astype(int)

print("\nFirst 10 predicted classes:")
print(y_pred[:10])

print("\nFirst 10 actual classes:")
print(y_test.iloc[:10].to_numpy())

# Create the confusion matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion matrix:")
print(cm)

# Calculate precision
precision = precision_score(y_test, y_pred)

print("\nPrecision:", round(precision, 3))

# Calculate recall
recall = recall_score(y_test, y_pred)

print("\nRecall:", round(recall, 3))

# Calculate F1 score
f1 = f1_score(y_test, y_pred)

print("\nF1 score:", round(f1, 3))

# Calculate ROC-AUC
roc_auc = roc_auc_score(y_test, probability_cheaper)

print("\nROC-AUC:", round(roc_auc, 3))

# Show the model's feature coefficients
print("\nFeature coefficients:")

for feature, coefficient in zip(features, model.coef_[0]):
    print(feature, ":", round(coefficient, 4))

print("\nFeature correlations:")
print(df[features].corr().round(2))

print("\nModel training complete.")

# Create the Random Forest model
rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

# Train the Random Forest using the same training data
rf_model.fit(X_train, y_train)

print("\nRandom Forest training complete.")

# Get Random Forest probability predictions
rf_probabilities = rf_model.predict_proba(X_test)

# Probability of a cheaper price within 30 days
rf_probability_cheaper = rf_probabilities[:, 1]

print("\nFirst 5 Random Forest probabilities:")
print(rf_probability_cheaper[:5])

# Convert Random Forest probabilities into binary predictions
rf_y_pred = (rf_probability_cheaper >= 0.50).astype(int)

print("\nFirst 10 Random Forest predictions:")
print(rf_y_pred[:10])

print("\nFirst 10 actual classes:")
print(y_test.iloc[:10].to_numpy())

# Create the Random Forest confusion matrix
rf_cm = confusion_matrix(y_test, rf_y_pred)

print("\nRandom Forest confusion matrix:")
print(rf_cm)

# Calculate Random Forest precision
rf_precision = precision_score(y_test, rf_y_pred)

print("\nRandom Forest precision:", round(rf_precision, 3))

# Random Forest evaluation metrics

rf_recall = recall_score(y_test, rf_y_pred)
rf_f1 = f1_score(y_test, rf_y_pred)
rf_roc_auc = roc_auc_score(y_test, rf_probability_cheaper)

print("\nRandom Forest evaluation:")
print("Precision:", round(rf_precision, 3))
print("Recall:", round(rf_recall, 3))
print("F1:", round(rf_f1, 3))
print("ROC-AUC:", round(rf_roc_auc, 3))