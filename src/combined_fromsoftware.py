import pandas as pd


games = {
    "Elden Ring": "data/features/elden_ring.csv",
    "Dark Souls II": "data/features/dark_souls_2.csv",
    "Dark Souls III": "data/features/dark_souls_3.csv",
    "Dark Souls Remastered": "data/features/dark_souls_remastered.csv",
    "Sekiro": "data/features/sekiro.csv"
}


all_games = []

for game_name, file_path in games.items():
    df = pd.read_csv(file_path)

    df["game"] = game_name

    all_games.append(df)

    print(game_name, "rows:", len(df))


combined_df = pd.concat(all_games, ignore_index=True)


print("\nCombined FromSoftware dataset")
print("Rows:", len(combined_df))
print("Columns:", len(combined_df.columns))

print("\nRows by game:")
print(combined_df["game"].value_counts())

print("\nFirst 10 rows:")
print(combined_df.head(10))


combined_df.to_csv(
    "data/features/fromsoftware_combined.csv",
    index=False
)

print("\nSaved to:")
print("data/features/fromsoftware_combined.csv")