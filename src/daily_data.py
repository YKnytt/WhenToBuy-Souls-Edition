from pathlib import Path
import pandas as pd


# Project folders
project_folder = Path(__file__).parent.parent
cleaned_folder = project_folder / "data" / "cleaned"
daily_folder = project_folder / "data" / "daily"

# Create the daily-data folder
daily_folder.mkdir(exist_ok=True)


# Find all cleaned CSV files
csv_files = list(cleaned_folder.glob("*.csv"))

print(f"Found {len(csv_files)} cleaned CSV files.")
print()


for file in csv_files:

    print("=" * 70)
    print(f"Creating daily data: {file.stem}")
    print("=" * 70)

    # Load the cleaned data
    df = pd.read_csv(file)

    # Convert DateTime to datetime
    df["DateTime"] = pd.to_datetime(df["DateTime"])

    # Make sure the data is chronological
    df = df.sort_values("DateTime").reset_index(drop=True)

    # Use the first and last dates in the dataset
    start_date = df["DateTime"].min().normalize()
    end_date = df["DateTime"].max().normalize()

    # Create one row for every day
    daily_dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D"
    )

    daily_df = pd.DataFrame({
        "Date": daily_dates
    })

    # Match each day with the most recently recorded price
    daily_df = pd.merge_asof(
        daily_df.sort_values("Date"),
        df[["DateTime", "Final price"]].sort_values("DateTime"),
        left_on="Date",
        right_on="DateTime",
        direction="backward"
    )

    # Remove days before the first recorded price
    daily_df = daily_df.dropna(subset=["Final price"])

    # Rename the price column
    daily_df = daily_df.rename(
        columns={"Final price": "Price"}
    )

    # Keep only the columns we need
    daily_df = daily_df[["Date", "Price"]]

    # Save the daily data
    output_file = daily_folder / file.name
    daily_df.to_csv(output_file, index=False)

    print(f"Start date: {daily_df['Date'].min()}")
    print(f"End date: {daily_df['Date'].max()}")
    print(f"Daily rows created: {len(daily_df)}")
    print(f"Saved to: {output_file}")
    print()


print("=" * 70)
print("DAILY DATA CREATION COMPLETE")
print("=" * 70)