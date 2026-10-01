from pathlib import Path
import pandas as pd

# Find the project's data folder
data_folder = Path(__file__).parent.parent / "data"

# Find every CSV file
csv_files = list(data_folder.glob("*.csv"))

for file in csv_files:
    df = pd.read_csv(file)

    # Convert DateTime into an actual date/time
    df["DateTime"] = pd.to_datetime(df["DateTime"])

    print("=" * 70)
    print(f"GAME: {file.stem}")
    print("=" * 70)

    # Show rows where Final price is missing
    missing_price = df[df["Final price"].isna()]

    if len(missing_price) > 0:
        print("\nMissing Final price:")
        print(missing_price.to_string(index=False))

    # Show rows where Final price is zero
    zero_price = df[df["Final price"] == 0]

    if len(zero_price) > 0:
        print("\nZERO-PRICE ROWS:")
        print(zero_price.to_string(index=False))

    print()