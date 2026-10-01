import pandas as pd


df = pd.read_csv("data/features/fromsoftware_combined.csv")


games = df["game"].unique()

train_parts = []
test_parts = []


for game in games:

    game_df = df[df["game"] == game].copy()

    # Make sure the game is ordered chronologically
    game_df = game_df.sort_values("Date").reset_index(drop=True)

    split_index = int(len(game_df) * 0.8)

    train_game = game_df.iloc[:split_index]
    test_game = game_df.iloc[split_index:]

    train_parts.append(train_game)
    test_parts.append(test_game)

    print("\n" + "=" * 60)
    print(game)
    print("=" * 60)

    print("Total rows:", len(game_df))
    print("Training rows:", len(train_game))
    print("Testing rows:", len(test_game))

    print(
        "Training period:",
        train_game["Date"].iloc[0],
        "to",
        train_game["Date"].iloc[-1]
    )

    print(
        "Testing period:",
        test_game["Date"].iloc[0],
        "to",
        test_game["Date"].iloc[-1]
    )


train_df = pd.concat(train_parts, ignore_index=True)
test_df = pd.concat(test_parts, ignore_index=True)


print("\n" + "=" * 60)
print("COMBINED SPLIT")
print("=" * 60)

print("Training rows:", len(train_df))
print("Testing rows:", len(test_df))

print("\nTraining rows by game:")
print(train_df["game"].value_counts())

print("\nTesting rows by game:")
print(test_df["game"].value_counts())


train_df.to_csv(
    "data/features/fromsoftware_train.csv",
    index=False
)

test_df.to_csv(
    "data/features/fromsoftware_test.csv",
    index=False
)


print("\nSaved:")
print("data/features/fromsoftware_train.csv")
print("data/features/fromsoftware_test.csv")