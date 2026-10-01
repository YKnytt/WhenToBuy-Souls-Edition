from pathlib import Path
import pandas as pd


# Project folders
project_folder = Path(__file__).parent.parent
daily_folder = project_folder / "data" / "daily"
features_folder = project_folder / "data" / "features"

# Create the features folder
features_folder.mkdir(exist_ok=True)


# Find all daily CSV files
csv_files = list(daily_folder.glob("*.csv"))

print(f"Found {len(csv_files)} daily CSV files.")
print()


for file in csv_files:

    print("=" * 70)
    print(f"Creating features: {file.stem}")
    print("=" * 70)

    # Load daily price data
    df = pd.read_csv(file)

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Make sure data is chronological
    df = df.sort_values("Date").reset_index(drop=True)

    # ---------------------------------------------------------
    # BASIC PRICE FEATURES
    # ---------------------------------------------------------

    # Historical lowest price seen up to each day
    df["historical_low"] = df["Price"].cummin()

    # How far today's price is above the historical low
    df["price_above_low"] = df["Price"] - df["historical_low"]

    # Percentage above the historical low
    df["percent_above_low"] = (
        df["price_above_low"] / df["historical_low"]
    ) * 100

    # ---------------------------------------------------------
    # PRICE BEHAVIOR FEATURES
    # ---------------------------------------------------------

    # Identify days when the price changed
    price_changed = df["Price"].ne(df["Price"].shift())

    # Create a group for each period where the price stayed the same
    price_period = price_changed.cumsum()

    # Count how many days have passed since the price changed
    df["days_since_price_change"] = (
        df.groupby(price_period).cumcount()
    )

    # ---------------------------------------------------------
    # SALE TIMING
    # ---------------------------------------------------------

    # Identify days when the price decreased.
    # A decrease means a new sale started.
    sale_day = df["Price"] < df["Price"].shift()

    # Give every sale start a unique number.
    # Days before the first sale belong to group 0.
    sale_group = sale_day.cumsum()

    # Find the date on which each sale started.
    sale_start_dates = (
        df.loc[sale_day, "Date"]
        .groupby(sale_group[sale_day])
        .first()
    )

    # Map each day's sale group to its sale start date.
    df["sale_start_date"] = sale_group.map(sale_start_dates)

    # For days before the first sale, use the beginning
    # of the available price history.
    df["sale_start_date"] = df["sale_start_date"].fillna(df["Date"].iloc[0])

    # Calculate how many days have passed since the
    # most recent sale started.
    df["days_since_sale"] = (
        df["Date"] - df["sale_start_date"]
    ).dt.days

    # The date is only an intermediate calculation.
    # We don't need it in the final feature dataset.
    df = df.drop(columns=["sale_start_date"])

    # ---------------------------------------------------------
    # RECENT SALE FREQUENCY
    # ---------------------------------------------------------

    # Convert True/False into 1/0
    sale_day = sale_day.astype(int)

    # Count price decreases during the previous 365 days
    df["sales_last_365_days"] = (
        sale_day
        .rolling(window=365, min_periods=1)
        .sum()
        .shift(1)
        .fillna(0)
    )

    # ---------------------------------------------------------
    # RECENT AVERAGE PRICE
    # ---------------------------------------------------------

    # Calculate the average price during the previous 365 days
    df["avg_price_last_365_days"] = (
        df["Price"]
        .rolling(window=365, min_periods=1)
        .mean()
        .shift(1)
    )

    # The first day has no previous price history
    df["avg_price_last_365_days"] = (
        df["avg_price_last_365_days"].fillna(df["Price"])
    )

    # ---------------------------------------------------------
    # RECENT PRICE CHANGE FREQUENCY
    # ---------------------------------------------------------

    # Identify days when the price changed
    price_change_day = df["Price"].ne(df["Price"].shift())

    # The first row has no previous price, so it is not a price change
    price_change_day.iloc[0] = False

    # Convert True/False into 1/0
    price_change_day = price_change_day.astype(int)

    # Count price changes during the previous 365 days
    df["price_changes_last_365_days"] = (
        price_change_day
        .rolling(window=365, min_periods=1)
        .sum()
        .shift(1)
        .fillna(0)
    )
    # ---------------------------------------------------------
    # FUTURE TARGET
    # ---------------------------------------------------------

    # Look at the next 30 days and find the lowest future price
    future_low = (
        df["Price"]
        .shift(-1)
        .iloc[::-1]
        .rolling(window=30, min_periods=30)
        .min()
        .iloc[::-1]
    )

    # 1 = a cheaper price occurs within the next 30 days
    # 0 = no cheaper price occurs within the next 30 days
    df["cheaper_within_30_days"] = (
        future_low < df["Price"]
    ).astype(int)

    # Remove the final 29 rows because they do not have
    # a complete 30-day future window
    df = df.iloc[:-29].copy()

    # Save the feature dataset
    output_file = features_folder / file.name
    df.to_csv(output_file, index=False)

    print(f"Rows: {len(df)}")
    print(f"Saved to: {output_file}")
    print()


print("=" * 70)
print("FEATURE CREATION COMPLETE")
print("=" * 70)