import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score


# Load training and testing data

train_df = pd.read_csv(
    "data/features/fromsoftware_train.csv"
)

test_df = pd.read_csv(
    "data/features/fromsoftware_test.csv"
)


print("Training rows:", len(train_df))
print("Testing rows:", len(test_df))


# Features

numeric_features = [
    "Price",
    "historical_low",
    "price_above_low",
    "percent_above_low",
    "days_since_price_change",
    "sales_last_365_days",
    "avg_price_last_365_days",
    "price_changes_last_365_days"
]

categorical_features = [
    "game"
]


# Separate inputs and target

X_train = train_df[numeric_features + categorical_features]
y_train = train_df["cheaper_within_30_days"]

X_test = test_df[numeric_features + categorical_features]
y_test = test_df["cheaper_within_30_days"]


# Convert game names into numerical columns

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            StandardScaler(),
            numeric_features
        ),
        (
            "game",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


# Create model pipeline

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ]
)


# Train

model.fit(X_train, y_train)

print("\nModel training complete.")


# Predictions

probabilities = model.predict_proba(X_test)

probability_cheaper = probabilities[:, 1]

y_pred = (
    probability_cheaper >= 0.50
).astype(int)


# Confusion matrix

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion matrix:")
print(cm)


# All evaluation metrics

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(
    y_test,
    probability_cheaper
)


print("\nFromSoftware Logistic Regression evaluation:")
print("Precision:", round(precision, 3))
print("Recall:", round(recall, 3))
print("F1:", round(f1, 3))
print("ROC-AUC:", round(roc_auc, 3))

print("\nROC-AUC by game:")

for game in test_df["game"].unique():

    game_mask = test_df["game"] == game

    game_y_test = y_test[game_mask]
    game_probabilities = probability_cheaper[game_mask]

    game_roc_auc = roc_auc_score(
        game_y_test,
        game_probabilities
    )

    print(
        game,
        ":",
        round(game_roc_auc, 3)
    )