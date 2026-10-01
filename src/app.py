import streamlit as st
import pandas as pd
import joblib


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="When To Buy: Souls Edition",
    page_icon="⚔️",
    layout="wide",
)


# =========================================================
# GAME CONFIGURATION
# =========================================================
# Each game has:
# - its own data file
# - its own trained model
# - its own visual theme

GAMES = {
    "Elden Ring": {
        "file": "elden_ring",
        "ml_available": True,
        "subtitle": "Guidance for the Tarnished.",
        "description": "The Lands Between",
        "theme": {
            "primary": "#d7b56d",
            "secondary": "#8b6930",
            "background_top": "#2b2418",
            "background_mid": "#11110f",
            "background_bottom": "#08090b",
            "card": "#131416",
            "border": "#37342e",
            "text": "#e8e4da",
            "muted": "#aaa49a",
            "recommendation": "#563e1b",
        },
    },

    "Elden Ring Nightreign": {
        "file": "elden_ring_nightreign",
        "ml_available": True,
        "subtitle": "Guidance beneath the Night.",
        "description": "The Nightfarers",
        "theme": {
            "primary": "#aab8d5",
            "secondary": "#536887",
            "background_top": "#172033",
            "background_mid": "#0c111d",
            "background_bottom": "#06080d",
            "card": "#10151f",
            "border": "#303b50",
            "text": "#dfe5f1",
            "muted": "#9ba6b9",
            "recommendation": "#1d2c45",
        },
    },

    "Dark Souls II": {
        "file": "dark_souls_2",
        "ml_available": True,
        "subtitle": "Guidance for the Bearer of the Curse.",
        "description": "Drangleic",
        "theme": {
            "primary": "#b49b6a",
            "secondary": "#756344",
            "background_top": "#28251f",
            "background_mid": "#121210",
            "background_bottom": "#080807",
            "card": "#151513",
            "border": "#39362f",
            "text": "#ddd7ca",
            "muted": "#a29b8c",
            "recommendation": "#3b3427",
        },
    },

    "Dark Souls III": {
        "file": "dark_souls_3",
        "ml_available": True,
        "subtitle": "Guidance for the Unkindled.",
        "description": "Lothric",
        "theme": {
            "primary": "#c27645",
            "secondary": "#713923",
            "background_top": "#281b18",
            "background_mid": "#110d0c",
            "background_bottom": "#070707",
            "card": "#151211",
            "border": "#3e302b",
            "text": "#e1d8cf",
            "muted": "#a59b92",
            "recommendation": "#3b2119",
        },
    },

    "Dark Souls Remastered": {
        "file": "dark_souls_remastered",
        "ml_available": True,
        "subtitle": "Guidance for the Chosen Undead.",
        "description": "Lordran",
        "theme": {
            "primary": "#c28a4a",
            "secondary": "#704b27",
            "background_top": "#2b2117",
            "background_mid": "#120f0c",
            "background_bottom": "#070706",
            "card": "#151310",
            "border": "#3d3228",
            "text": "#e0d7c9",
            "muted": "#a59b8c",
            "recommendation": "#3b2919",
        },
    },

    "Sekiro: Shadows Die Twice": {
        "file": "sekiro",
        "ml_available": True,
        "subtitle": "Guidance for the Wolf.",
        "description": "Ashina",
        "theme": {
            "primary": "#b83b35",
            "secondary": "#762621",
            "background_top": "#291817",
            "background_mid": "#110d0d",
            "background_bottom": "#070707",
            "card": "#151211",
            "border": "#422b29",
            "text": "#e2d9ca",
            "muted": "#a79c8e",
            "recommendation": "#3a1c1a",
        },
    },
}


FEATURES = [
    "Price",
    "historical_low",
    "price_above_low",
    "percent_above_low",
    "days_since_price_change",
    "sales_last_365_days",
    "avg_price_last_365_days",
    "price_changes_last_365_days",
]


# =========================================================
# GAME SELECTION
# =========================================================

st.sidebar.markdown("## ⚔️ WHEN TO BUY")
st.sidebar.caption("Souls Edition")

selected_game = st.sidebar.selectbox(
    "Choose a game",
    list(GAMES.keys()),
)

config = GAMES[selected_game]
theme = config["theme"]


# =========================================================
# DYNAMIC THEME
# =========================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(
                circle at 50% -20%,
                {theme["background_top"]} 0%,
                {theme["background_mid"]} 38%,
                {theme["background_bottom"]} 78%
            );
        color: {theme["text"]};
    }}

    [data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                {theme["background_mid"]},
                {theme["background_bottom"]}
            );
        border-right: 1px solid {theme["border"]};
    }}

    [data-testid="stSidebar"] * {{
        color: {theme["text"]};
    }}

    [data-testid="stSidebar"] .stSelectbox label {{
        color: {theme["muted"]};
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    [data-baseweb="select"] > div {{
        background: {theme["card"]};
        border-color: {theme["border"]};
    }}

    [data-testid="stAppViewContainer"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }}

    .hero-title {{
        font-family: 'Cinzel', serif;
        font-size: 42px;
        font-weight: 700;
        letter-spacing: 1px;
        color: {theme["primary"]};
        margin-bottom: 4px;
    }}

    .hero-game {{
        font-family: 'Cinzel', serif;
        font-size: 16px;
        color: {theme["secondary"]};
        text-transform: uppercase;
        letter-spacing: 2px;
        line-height: 1.4;
        margin-top: 4px;
        margin-bottom: 7px;
    }}

    .hero-title {{
        font-family: 'Cinzel', serif;
        font-size: 42px;
        font-weight: 700;
        letter-spacing: 1px;
        color: {theme["primary"]};
        margin-top: 2px;
        margin-bottom: 5px;
        line-height: 1.15;
    }}

    .hero-subtitle {{
        color: {theme["muted"]};
        font-size: 15px;
        line-height: 1.5;
        margin-top: 0;
        margin-bottom: 28px;
    }}

    .section-title {{
        font-family: 'Cinzel', serif;
        color: {theme["primary"]};
        font-size: 22px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-top: 12px;
        margin-bottom: 14px;
    }}

    .gold-line {{
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            {theme["secondary"]},
            transparent
        );
        margin: 30px 0;
    }}

    .metric-card {{
        background: rgba(19, 20, 22, 0.95);
        border: 1px solid {theme["border"]};
        border-radius: 8px;
        padding: 18px;
        min-height: 120px;
    }}

    .metric-label {{
        color: {theme["muted"]};
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.1px;
    }}

    .metric-value {{
        color: {theme["text"]};
        font-size: 28px;
        font-weight: 700;
        margin-top: 7px;
    }}

    .metric-description {{
        color: #77736b;
        font-size: 12px;
        margin-top: 5px;
        line-height: 1.4;
    }}

    .insight-card {{
        background: rgba(17, 18, 20, 0.92);
        border: 1px solid {theme["border"]};
        border-radius: 8px;
        padding: 19px;
        min-height: 150px;
    }}

    .insight-title {{
        color: {theme["primary"]};
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 9px;
    }}

    .insight-text {{
        color: {theme["muted"]};
        font-size: 13px;
        line-height: 1.6;
    }}

    .recommendation {{
        background:
            linear-gradient(
                135deg,
                {theme["recommendation"]},
                rgba(22, 21, 18, 0.97)
            );
        border: 1px solid {theme["secondary"]};
        border-left: 5px solid {theme["primary"]};
        border-radius: 9px;
        padding: 25px 28px;
        margin: 18px 0 26px 0;
    }}

    .recommendation-title {{
        font-family: 'Cinzel', serif;
        color: {theme["primary"]};
        font-size: 29px;
        font-weight: 600;
    }}

    .recommendation-description {{
        color: #c3beb3;
        font-size: 15px;
        line-height: 1.6;
        margin-top: 8px;
    }}

    .recommendation-small {{
        color: #77736b;
        font-size: 12px;
        margin-top: 12px;
    }}

    .warning-card {{
        background: rgba(40, 35, 25, 0.75);
        border: 1px solid {theme["secondary"]};
        border-left: 4px solid {theme["primary"]};
        border-radius: 8px;
        padding: 20px;
        margin: 18px 0 26px 0;
    }}

    .warning-title {{
        color: {theme["primary"]};
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 7px;
    }}

    .warning-text {{
        color: {theme["muted"]};
        font-size: 13px;
        line-height: 1.6;
    }}

    .tech-card {{
        background: rgba(14, 15, 17, 0.90);
        border: 1px solid {theme["border"]};
        border-radius: 8px;
        padding: 20px;
        min-height: 150px;
    }}

    .tech-number {{
        color: {theme["secondary"]};
        font-family: 'Cinzel', serif;
        font-size: 25px;
        font-weight: 700;
    }}

    .tech-title {{
        color: {theme["text"]};
        font-weight: 600;
        margin-top: 5px;
    }}

    .tech-text {{
        color: #858178;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 7px;
    }}

    .footer {{
        color: #625f58;
        font-size: 11px;
        text-align: center;
        margin-top: 35px;
    }}

    .stCaption {{
        color: {theme["muted"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA / MODEL HELPERS
# =========================================================

@st.cache_data
def load_daily_data(file_name):
    path = f"data/daily/{file_name}.csv"

    daily = pd.read_csv(path)
    daily["Date"] = pd.to_datetime(daily["Date"])

    daily = (
        daily
        .sort_values("Date")
        .reset_index(drop=True)
    )

    return daily


@st.cache_resource
def load_model(file_name):
    path = f"data/features/{file_name}_model.pkl"
    return joblib.load(path)


def build_live_features(daily):
    """
    Recreate the features used by the trained models.

    The live app uses the FULL daily dataset because a current
    prediction does not require a known future 30-day outcome.
    """

    daily = daily.copy()

    # Historical low
    daily["historical_low"] = (
        daily["Price"].cummin()
    )

    # Distance from historical low
    daily["price_above_low"] = (
        daily["Price"]
        - daily["historical_low"]
    )

    # Percentage above historical low
    daily["percent_above_low"] = (
        daily["price_above_low"]
        / daily["historical_low"]
        * 100
    )

    # ---------------------------------------------------------
    # Days since price change
    # ---------------------------------------------------------

    price_changed = (
        daily["Price"]
        != daily["Price"].shift()
    )

    price_change_group = (
        price_changed.cumsum()
    )

    change_start = (
        daily.loc[price_changed, "Date"]
        .groupby(
            price_change_group[price_changed]
        )
        .first()
    )

    daily["price_start_date"] = (
        price_change_group.map(change_start)
    )

    daily["price_start_date"] = (
        daily["price_start_date"]
        .fillna(daily["Date"].iloc[0])
    )

    daily["days_since_price_change"] = (
        daily["Date"]
        - daily["price_start_date"]
    ).dt.days

    daily = daily.drop(
        columns=["price_start_date"]
    )

    # ---------------------------------------------------------
    # Recent 365-day features
    # ---------------------------------------------------------

    daily["price_difference"] = (
        daily["Price"].diff()
    )

    # A price decrease means a sale.
    daily["sale_event"] = (
        daily["price_difference"] < 0
    ).astype(int)

    daily["price_change_event"] = (
        daily["price_difference"] != 0
    ).astype(int)

    # Shift by one day so today's price is not included.
    daily["sales_last_365_days"] = (
        daily["sale_event"]
        .shift(1)
        .rolling(365)
        .sum()
        .fillna(0)
    )

    daily["avg_price_last_365_days"] = (
        daily["Price"]
        .shift(1)
        .rolling(365)
        .mean()
        .fillna(daily["Price"])
    )

    daily["price_changes_last_365_days"] = (
        daily["price_change_event"]
        .shift(1)
        .rolling(365)
        .sum()
        .fillna(0)
    )

    return daily


# =========================================================
# LOAD SELECTED GAME
# =========================================================

daily = load_daily_data(
    config["file"]
)

daily = build_live_features(daily)

current = daily.iloc[-1]

current_date = current["Date"]
current_price = float(current["Price"])
historical_low = float(current["historical_low"])
average_price = float(current["avg_price_last_365_days"])
days_since_change = int(current["days_since_price_change"])
sales_last_year = int(current["sales_last_365_days"])


# =========================================================
# MODEL PREDICTION
# =========================================================

probability = None
recommendation = None
recommendation_text = None

if config["ml_available"]:

    model = load_model(
        config["file"]
    )

    X_current = pd.DataFrame(
        [current[FEATURES]],
        columns=FEATURES,
    )

    probability = (
        model
        .predict_proba(X_current)[0][1]
    )

    if probability >= 0.50:
        recommendation = "WAIT"

        recommendation_text = (
            f"The model estimates a "
            f"{probability:.0%} chance that "
            f"{selected_game} will fall below "
            f"its current price within the next "
            f"30 days."
        )

    else:
        recommendation = "BUY"

        recommendation_text = (
            f"The model estimates only a "
            f"{probability:.0%} chance that "
            f"{selected_game} will fall below "
            f"its current price within the next "
            f"30 days."
        )


# =========================================================
# PRICE ANALYSIS
# =========================================================

historical_high = float(
    daily["Price"].max()
)

potential_savings = (
    current_price
    - historical_low
)

percent_above_low = (
    potential_savings
    / historical_low
    * 100
)

current_vs_average = (
    current_price
    - average_price
)

percent_vs_average = (
    current_vs_average
    / average_price
    * 100
)


# =========================================================
# SALE FREQUENCY
# =========================================================

if sales_last_year > 0:
    sale_frequency = round(
        365 / sales_last_year
    )
else:
    sale_frequency = None


# =========================================================
# TYPICAL SALE PRICE
# =========================================================

sale_prices = daily[
    daily["Price"] < historical_high
]["Price"]

if len(sale_prices) > 0:

    typical_sale_price = float(
        sale_prices.mean()
    )

    typical_discount = (
        historical_high
        - typical_sale_price
    )

else:

    typical_sale_price = historical_high
    typical_discount = 0


# =========================================================
# HEADER
# =========================================================

# =========================================================
# HEADER
# =========================================================
# Use separate Streamlit markdown blocks for the hero instead
# of one st.html block. This prevents Streamlit's HTML renderer
# from clipping the first line at the top of the page.

st.markdown(
    f'''
    <div class="hero-game">
        {config["description"]}
    </div>
    ''',
    unsafe_allow_html=True,
)

st.markdown(
    '''
    <div class="hero-title">
        ⚔️ WHEN TO BUY
    </div>
    ''',
    unsafe_allow_html=True,
)

st.markdown(
    f'''
    <div class="hero-subtitle">
        <b>{selected_game}</b> — {config["subtitle"]}
        <br>
        Steam price intelligence for players deciding
        whether to buy now or wait.
    </div>
    ''',
    unsafe_allow_html=True,
)

st.caption(
    f"Live analysis based on the latest available price data: "
    f"{current_date.strftime('%B %d, %Y')}"
)


# =========================================================
# RECOMMENDATION / MODEL STATUS
# =========================================================

if config["ml_available"]:

    st.html(
        f"""
        <div class="recommendation">

            <div class="recommendation-title">
                ⚔️ Recommendation: {recommendation}
            </div>

            <div class="recommendation-description">
                {recommendation_text}
            </div>

            <div class="recommendation-small">
                Prediction window:
                {current_date.strftime('%b %d')}
                →
                {(current_date + pd.Timedelta(days=30)).strftime('%b %d, %Y')}
                &nbsp;•&nbsp;
                Model estimate: {probability:.0%}
            </div>

        </div>
        """
    )

else:

    st.html(
        f"""
        <div class="warning-card">

            <div class="warning-title">
                ⚔️ Historical Analysis Mode
            </div>

            <div class="warning-text">
                The current machine-learning model for
                <b>{selected_game}</b> did not demonstrate
                sufficient predictive signal in its evaluation.
                Rather than presenting a misleading BUY/WAIT
                probability, this dashboard provides the
                game's historical pricing analytics instead.
            </div>

        </div>
        """
    )


# =========================================================
# KEY METRICS
# =========================================================

if config["ml_available"]:

    col1, col2, col3, col4 = st.columns(4)

else:

    col1, col2, col3 = st.columns(3)


with col1:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Current Price
            </div>

            <div class="metric-value">
                ${current_price:.2f}
            </div>

            <div class="metric-description">
                Latest observed Steam price
            </div>

        </div>
        """
    )


with col2:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Historical Low
            </div>

            <div class="metric-value">
                ${historical_low:.2f}
            </div>

            <div class="metric-description">
                Lowest observed price in history
            </div>

        </div>
        """
    )


with col3:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Potential Savings
            </div>

            <div class="metric-value">
                ${potential_savings:.2f}
            </div>

            <div class="metric-description">
                Savings if price returns to its historical low
            </div>

        </div>
        """
    )


if config["ml_available"]:

    with col4:

        st.html(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Lower Price Estimate
                </div>

                <div class="metric-value">
                    {probability:.0%}
                </div>

                <div class="metric-description">
                    Model estimate within the next 30 days
                </div>

            </div>
            """
        )


# =========================================================
# PRICE CONTEXT
# =========================================================

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-title">
        PRICE CONTEXT
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)


with col1:

    comparison = (
        "above"
        if current_vs_average >= 0
        else "below"
    )

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                📊 Current vs. 365-Day Average
            </div>

            <div class="insight-text">

                The current price is
                <b>${abs(current_vs_average):.2f}</b>
                {comparison} the 365-day average of
                <b>${average_price:.2f}</b>.

                <br><br>

                That is a
                <b>{abs(percent_vs_average):.1f}%</b>
                difference from the recent average.

            </div>

        </div>
        """
    )


with col2:

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                💰 Distance From Historical Low
            </div>

            <div class="insight-text">

                The current price is
                <b>${potential_savings:.2f}</b>
                above the historical low.

                <br><br>

                That means the current price is
                <b>{percent_above_low:.1f}%</b>
                above the lowest observed price.

            </div>

        </div>
        """
    )


with col3:

    frequency_text = (
        f"approximately every {sale_frequency} days"
        if sale_frequency
        else "no recent sale pattern detected"
    )

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                🔥 Sale Activity
            </div>

            <div class="insight-text">

                {selected_game} went on sale
                <b>{sales_last_year} times</b>
                during the previous 365 days.

                <br><br>

                That's approximately
                <b>{frequency_text}</b>.

            </div>

        </div>
        """
    )


# =========================================================
# PRICE HISTORY
# =========================================================

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-title">
        PRICE HISTORY
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Historical Steam pricing. Downward movements represent discounted periods."
)

chart_data = daily[
    ["Date", "Price"]
].copy()

chart_data = chart_data.set_index(
    "Date"
)

st.line_chart(
    chart_data,
    height=350,
)


# =========================================================
# SALE PATTERN
# =========================================================

st.markdown(
    """
    <div class="section-title">
        SALE PATTERN
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)


with col1:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Typical Sale Price
            </div>

            <div class="metric-value">
                ${typical_sale_price:.2f}
            </div>

            <div class="metric-description">
                Average observed price during discounted periods
            </div>

        </div>
        """
    )


with col2:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Typical Discount
            </div>

            <div class="metric-value">
                ${typical_discount:.2f}
            </div>

            <div class="metric-description">
                Average reduction from the ${historical_high:.2f}
                full-price level
            </div>

        </div>
        """
    )


with col3:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Days At Current Price
            </div>

            <div class="metric-value">
                {days_since_change}
            </div>

            <div class="metric-description">
                Days since the most recent price change
            </div>

        </div>
        """
    )


# =========================================================
# WHY?
# =========================================================

if config["ml_available"]:

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="section-title">
            WHY THE MODEL SAYS {recommendation}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                The pricing opportunity
            </div>

            <div class="insight-text">

                {selected_game} is currently
                <b>${current_price:.2f}</b>.

                The historical low is
                <b>${historical_low:.2f}</b>.

                <br><br>

                If the price returned to that level,
                the customer would save
                <b>${potential_savings:.2f}</b>.

            </div>

        </div>
        """
    )

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Recent pricing behavior
            </div>

            <div class="insight-text">

                The game experienced
                <b>{sales_last_year} sales</b>
                during the previous 365 days.

                The recent average price was
                <b>${average_price:.2f}</b>.

                Today's observed price is
                <b>{abs(percent_vs_average):.1f}% {comparison}</b>
                that average.

            </div>

        </div>
        """
    )

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                What the prediction means
            </div>

            <div class="insight-text">

                As of
                <b>{current_date.strftime('%B %d, %Y')}</b>,
                the model estimates a
                <b>{probability:.0%}</b>
                probability that a price lower than the
                current price will occur within the following
                30 days.

                <br><br>

                That means the prediction window extends through
                <b>{(current_date + pd.Timedelta(days=30)).strftime('%B %d, %Y')}</b>.

                <br><br>

                This is a model estimate, not a guarantee
                or an exact prediction of the next sale.

            </div>

        </div>
        """
    )

else:

    st.markdown(
        '<div class="gold-line"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-title">
            MODEL STATUS
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Why there is no BUY / WAIT prediction
            </div>

            <div class="insight-text">

                The current feature set and model did not
                demonstrate sufficient predictive signal for
                <b>{selected_game}</b> during evaluation.

                <br><br>

                Rather than presenting a probability that could
                give the customer a false sense of precision,
                the application falls back to transparent
                historical price analysis.

                <br><br>

                This means the customer can still see the
                current price, historical low, recent average,
                sale activity, and price history.

            </div>

        </div>
        """
    )


# =========================================================
# HOW IT WORKS
# =========================================================

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-title">
        HOW IT WORKS
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.html(
        """
        <div class="tech-card">

            <div class="tech-number">
                01
            </div>

            <div class="tech-title">
                Historical Data
            </div>

            <div class="tech-text">
                Steam price-change events are converted
                into a daily price history for each game.
            </div>

        </div>
        """
    )


with col2:

    st.html(
        """
        <div class="tech-card">

            <div class="tech-number">
                02
            </div>

            <div class="tech-title">
                Feature Engineering
            </div>

            <div class="tech-text">
                The system calculates historical lows,
                recent sale frequency, average price,
                price changes, and time at the current price.
            </div>

        </div>
        """
    )


with col3:

    if config["ml_available"]:

        tech_title = "ML Prediction"
        tech_text = (
            "A game-specific Logistic Regression model "
            "estimates the likelihood of a lower price "
            "within the next 30 days."
        )

    else:

        tech_title = "Historical Analysis"
        tech_text = (
            "The application uses transparent pricing "
            "analytics because the current model did not "
            "show sufficient predictive signal."
        )

    st.html(
        f"""
        <div class="tech-card">

            <div class="tech-number">
                03
            </div>

            <div class="tech-title">
                {tech_title}
            </div>

            <div class="tech-text">
                {tech_text}
            </div>

        </div>
        """
    )


with col4:

    st.html(
        """
        <div class="tech-card">

            <div class="tech-number">
                04
            </div>

            <div class="tech-title">
                Customer Decision
            </div>

            <div class="tech-text">
                Pricing evidence is presented in a simple
                dashboard so the player can make the final
                purchase decision.
            </div>

        </div>
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.html(
    f"""
    <div class="footer">
        WHEN TO BUY — SOULS EDITION
        • {selected_game}
        • Historical pricing intelligence
        • Model estimates are not guarantees
    </div>
    """
)