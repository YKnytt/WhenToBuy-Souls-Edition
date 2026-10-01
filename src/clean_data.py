from pathlib import Path
import pandas as pd

# Project folders
project_folder = Path(__file__).parent.parent
raw_folder = project_folder / "data" / "raw"
cleaned_folder = project_folder / "data" / "cleaned"

# Create cleaned folder if it doesn't exist
cleaned_folder.mkdir(exist_ok=True)

# Find CSV files inside data/raw
csv_files = list(raw_folder.glob("*.csv"))

print(f"Found {len(csv_files)} CSV files.")
print()

for file in csv_files:
    print("=" * 70)
    print(f"Cleaning: {file.stem}")
    print("=" * 70)

    # Load the CSV
    df = pd.read_csv(file)

    # Convert DateTime into an actual datetime value
    df["DateTime"] = pd.to_datetime(df["DateTime"])

    # Remove rows without a Final price
    before = len(df)
    df = df.dropna(subset=["Final price"])
    removed_missing = before - len(df)

    # Sort chronologically
    df = df.sort_values("DateTime").reset_index(drop=True)

    # Special handling for Elden Ring
    if file.stem == "elden_ring":

        # Remove pre-release records
        release_date = pd.Timestamp("2022-02-24 23:10:02")
        df = df[df["DateTime"] >= release_date]

        # Remove invalid zero-price records
        df = df[df["Final price"] > 0]

        # Reset row numbers
        df = df.reset_index(drop=True)

    # Save cleaned file
    output_file = cleaned_folder / file.name
    df.to_csv(output_file, index=False)

    print(f"Original rows: {before}")
    print(f"Missing-price rows removed: {removed_missing}")
    print(f"Final cleaned rows: {len(df)}")
    print(f"Saved to: {output_file}")
    print()


print("=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)