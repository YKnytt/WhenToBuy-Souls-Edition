import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ---------------------------------------------------------
# Games we want to support
# ---------------------------------------------------------

games = {
    "Elden Ring": "elden_ring",
    "Elden Ring Nightreign": "elden_ring_nightreign",
    "Dark Souls II": "dark_souls_2",
    "Dark Souls III": "dark_souls_3",
    "Dark Souls Remastered": "dark_souls_remastered",
    "Sekiro: Shadows Die Twice": "sekiro"
}


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


results = []


# ---------------------------------------------------------
# Train one model for each game
# ---------------------------------------------------------

for game_name, file_name in games.items():

    print("\n" + "=" * 60)
    print(game_name)
    print("=" * 60)

    file_path = f"data/features/{file_name}.csv"

    df = pd.read_csv(file_path)

    X = df[features]
    y = df["cheaper_within_30_days"]

    # Chronological 80/20 split
    split_index = int(len(df) * 0.80)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    print(f"Total rows: {len(df)}")
    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")

    # Logistic Regression
    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    # Predictions
    probabilities = model.predict_proba(X_test)[:, 1]

    y_pred = (probabilities >= 0.50).astype(int)

    # Metrics
    cm = confusion_matrix(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    # ROC-AUC requires both classes to exist
    if len(y_test.unique()) == 2:
        roc_auc = roc_auc_score(
            y_test,
            probabilities
        )
    else:
        roc_auc = float("nan")

    print("\nConfusion Matrix:")
    print(cm)

    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1 Score:  {f1:.3f}")
    print(f"ROC-AUC:   {roc_auc:.3f}")

    # Save model
    model_path = f"data/features/{file_name}_model.pkl"

    joblib.dump(model, model_path)

    print(f"\nModel saved to:")
    print(model_path)

    # Store results
    results.append({
        "Game": game_name,
        "Rows": len(df),
        "Train": len(X_train),
        "Test": len(X_test),
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "ROC-AUC": roc_auc
    })


# ---------------------------------------------------------
# Final comparison
# ---------------------------------------------------------

results_df = pd.DataFrame(results)

print("\n\n")
print("=" * 80)
print("FROM SOFTWARE MODEL COMPARISON")
print("=" * 80)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.3f}"
    )
)

print("\nAll models trained and saved.")