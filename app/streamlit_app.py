import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

def format_f1_time(ms):
    ms = int(round(ms))
    total_seconds = ms / 1000
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int(ms % 1000)
    return f"{minutes}:{seconds:02d}.{milliseconds:03d}"

def prediction_slider(label, min_value, max_value, value, timing=False, step=1):
    state_key = (
        label.replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
        .lower()
    )

    slider_key = f"{state_key}_slider"
    input_key = f"{state_key}_input"

    if slider_key not in st.session_state:
        st.session_state[slider_key] = value

    if input_key not in st.session_state:
        st.session_state[input_key] = value

    def slider_changed():
        st.session_state[input_key] = st.session_state[slider_key]

    def input_changed():
        st.session_state[slider_key] = st.session_state[input_key]

    slider_col, input_col = st.columns([4, 1])

    with slider_col:
        st.slider(
            label,
            min_value=min_value,
            max_value=max_value,
            step=step,
            key=slider_key,
            on_change=slider_changed
        )

    with input_col:
        st.number_input(
            " ",
            min_value=min_value,
            max_value=max_value,
            step=step,
            key=input_key,
            label_visibility="collapsed",
            on_change=input_changed
        )

    selected = st.session_state[slider_key]

    if timing:
        st.caption(f"⏱️ Lap Time Format: {format_f1_time(selected)}")
    else:
        st.markdown("<div class='caption-spacer'></div>", unsafe_allow_html=True)

    return selected

# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "processed" / "f1_pit_strategy_model_data.csv"
MODEL_PATH = BASE_DIR / "models" / "random_forest_model.pkl"
MODEL_COLUMNS_PATH = BASE_DIR / "models" / "model_columns.pkl"
FIGURES_DIR = BASE_DIR / "figures"

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(DATA_PATH)

model = joblib.load(MODEL_PATH)

model_columns = joblib.load(MODEL_COLUMNS_PATH)

# =========================================================
# CONSTRUCTOR NAME NORMALIZATION
# =========================================================

constructor_mapping = {
    # Minor formatting consistency
    "Alpine F1 Team": "Alpine",
    "Haas F1 Team": "Haas",
    "Kick Sauber": "Sauber",
    "Lotus F1" : "Lotus",
    "Manor Marussia": "Marussia",
    "RB F1 Team": "Racing Bulls",
    "Red Bull": "Red Bull Racing"
}

df["constructor_clean"] = (
    df["constructor_name"]
    .replace(constructor_mapping)
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="F1 Pit Stop Strategy Predictions",
    page_icon="🏎️",
    layout="wide"
)

# =========================================================
# TEAM THEMES
# =========================================================

TEAM_THEMES = {
    "Default": {
        "primary": "#E10600",
        "secondary": "#FFFFFF",
        "background": "#0E1117"
    },
    "Alpine": {
        "primary": "#479FE2",
        "secondary": "#FD4BC7",
        "background": "#00101F"
    },
    "Aston Martin": {
        "primary": "#4B9774",
        "secondary": "#CEDC00",
        "background": "#001A16"
    },
    "Audi": {
        "primary": "#EB4526",
        "secondary": "#FFFFFF",
        "background": "#150500"
    },
    "Cadillac": {
        "primary": "#AAAADD",
        "secondary": "#FFFFFF",
        "background": "#111122"
    },
    "Ferrari": {
        "primary": "#D52E37",
        "secondary": "#FFF200",
        "background": "#160000"
    },
    "Haas": {
        "primary": "#DFE1E2",
        "secondary": "#E10600",
        "background": "#111111"
    },
    "McLaren": {
        "primary": "#ef8733",
        "secondary": "#FFFFFF",
        "background": "#1A0D00"
    },
    "Mercedes": {
        "primary": "#75F1D3",
        "secondary": "#FFFFFF",
        "background": "#001F1F"
    },
    "Red Bull Racing": {
        "primary": "#4570C0",
        "secondary": "#FFCC00",
        "background": "#050A30"
    },
    "Visa Cash App Racing Bulls": {
        "primary": "#7091f8",
        "secondary": "#FFFFFF",
        "background": "#050A25"
    },
    "Williams": {
        "primary": "#3267D4",
        "secondary": "#FFFFFF",
        "background": "#000A1F"
    }
}

# =========================================================
# SIDEBAR
# =========================================================

# -----------------------------
# Session State Defaults
# -----------------------------

if "page" not in st.session_state:
    st.session_state.page = "🏁 Race Prediction"

if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Default"

# -----------------------------
# Navigation
# -----------------------------

nav_items = [
    "🏁 Race Prediction",
    "📊 Strategy Analysis",
    "🤖 Model Performance",
    "ℹ️ About Project"
]

for item in nav_items:
    is_active = st.session_state.page == item

    if st.sidebar.button(
        item,
        key=f"nav_{item}",
        width="stretch",
        type="primary" if is_active else "secondary"
    ):
        st.session_state.page = item
        st.rerun()

page = st.session_state.page

# -----------------------------
# Theme Selector
# -----------------------------

st.sidebar.divider()

theme_options = [
    "Default",
    "Alpine",
    "Aston Martin",
    "Audi",
    "Cadillac",
    "Ferrari",
    "Haas",
    "McLaren",
    "Mercedes",
    "Red Bull Racing",
    "Visa Cash App Racing Bulls",
    "Williams"
]

theme_choice = st.sidebar.selectbox(
    "Choose Your F1 Team Livery Theme",
    theme_options,
    index=theme_options.index(st.session_state.theme_choice),
    key="theme_selectbox"
)

if theme_choice != st.session_state.theme_choice:
    st.session_state.theme_choice = theme_choice
    st.rerun()

theme = TEAM_THEMES[st.session_state.theme_choice]

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(f"""
<style>

/* ================================
   MAIN APP
================================ */

.stApp {{
    background-color: {theme['background']};
    color: white;
}}

/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        #151722 0%,
        #11131D 100%
    );
    border-right: 1px solid {theme['primary']};
}}

/* ================================
   SIDEBAR NAV BUTTONS
================================ */

section[data-testid="stSidebar"] button {{
    text-align: left !important;
    justify-content: flex-start !important;

    border-radius: 10px !important;

    margin-bottom: 8px !important;

    font-weight: 700 !important;

    background-color: transparent !important;

    color: #EAEAEA !important;

    border: 1px solid transparent !important;

    transition: all 0.15s ease-in-out !important;
}}

/* ACTIVE PAGE */

section[data-testid="stSidebar"] button[kind="primary"] {{

    background-color: rgba(255,255,255,0.04) !important;

    color: #FFFFFF !important;

    border: 2px solid {theme['primary']} !important;

    box-shadow:
        0 0 12px rgba(255,255,255,0.08),
        0 0 6px {theme['secondary']} !important;
}}

/* HOVER EFFECT */

section[data-testid="stSidebar"] button[kind="secondary"]:hover {{

    background-color: rgba(255,255,255,0.08) !important;

    color: {theme['primary']} !important;

    border: 1px solid {theme['primary']} !important;
}}

/* ================================
   SIDEBAR TEXT
================================ */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {{
    color: white !important;
}}

/* ================================
   SIDEBAR COLLAPSE ARROW
================================ */

[data-testid="collapsedControl"] {{
    color: {theme['secondary']} !important;
    opacity: 1 !important;
    visibility: visible !important;
}}

[data-testid="collapsedControl"] svg {{
    fill: {theme['secondary']} !important;
    color: {theme['secondary']} !important;
    opacity: 1 !important;
}}

/* ================================
   HEADINGS
================================ */

h1, h2, h3 {{
    color: {theme['primary']};
}}

/* ================================
   METRIC CARDS
================================ */

div[data-testid="metric-container"] {{

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.06),
            rgba(255,255,255,0.02)
        );

    border: 1px solid {theme['primary']};

    padding: 16px;

    border-radius: 14px;

    box-shadow:
        0 0 18px rgba(0,0,0,0.35);

    transition: 0.2s ease-in-out;
}}

div[data-testid="metric-container"]:hover {{

    transform: translateY(-2px);

    border: 1px solid {theme['secondary']};
}}

[data-testid="stMetricValue"] {{
    color: {theme['primary']};
}}

/* ================================
   SELECTBOXES / DROPDOWNS
================================ */

div[data-baseweb="select"] > div {{

    background-color: #242633;

    border: 1px solid {theme['primary']};

    color: white;

    border-radius: 10px;
}}

div[data-baseweb="select"] svg {{
    fill: {theme['secondary']} !important;
    color: {theme['secondary']} !important;
    opacity: 1 !important;
}}

[data-testid="stSelectbox"] svg,
[data-testid="stMultiSelect"] svg {{
    fill: {theme['secondary']} !important;
    color: {theme['secondary']} !important;
    opacity: 1 !important;
}}

/* ================================
   SLIDERS
================================ */

.stSlider [data-baseweb="slider"] {{
    padding-top: 12px;
    padding-bottom: 12px;
}}

/* Full track glow layer */

.stSlider [data-baseweb="slider"] > div > div {{
    background: linear-gradient(
        90deg,
        {theme['primary']} 0%,
        {theme['primary']} 45%,
        {theme['secondary']} 100%
    ) !important;

    height: 6px !important;
    border-radius: 999px !important;

    box-shadow:
        0 0 10px {theme['primary']},
        0 0 18px {theme['secondary']} !important;
}}

/* Force internal progress layers away from default red */

.stSlider [data-baseweb="slider"] div {{
    border-color: {theme['primary']} !important;
}}

/* Slider knob */

.stSlider [role="slider"] {{
    background-color: {theme['secondary']} !important;
    border: 2px solid {theme['primary']} !important;

    box-shadow:
        0 0 10px {theme['secondary']},
        0 0 18px {theme['primary']},
        0 0 24px rgba(255,255,255,0.20) !important;
}}

.stSlider [role="slider"]:hover {{
    transform: scale(1.08);

    box-shadow:
        0 0 14px {theme['secondary']},
        0 0 26px {theme['primary']},
        0 0 34px rgba(255,255,255,0.25) !important;
}}

/* Slider value labels */

.stSlider [data-testid="stThumbValue"] {{
    color: {theme['primary']} !important;
    font-weight: 800 !important;
}}

.stSlider label {{
    color: white !important;
    font-weight: 600;
}}

.caption-spacer {{
    height: 38.5px;
}}

/* ================================
   TABLES
================================ */

[data-testid="stDataFrame"] {{
    border: 1px solid {theme['primary']};
    border-radius: 12px;
    overflow: hidden;
}}

/* ================================
   DIVIDERS
================================ */

hr {{
    border-color: {theme['primary']};
}}

/* ================================
   GENERAL BUTTONS
================================ */

.stButton>button {{

    border-radius: 10px;

    font-weight: 700;

    border: 1px solid {theme['primary']};

    background-color: rgba(255,255,255,0.04);

    color: white;
}}

.stButton>button:hover {{

    border: 1px solid {theme['secondary']};

    color: {theme['primary']};
}}

[data-testid="stNumberInput"] input {{
    background-color: #242633 !important;
    color: white !important;
    border: 1px solid {theme['primary']} !important;
    border-radius: 8px !important;
    text-align: center !important;
    font-weight: 700 !important;
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.title("🏎️ Formula 1 Pit Stop Strategy Analytics")

st.write("""
Analyze Formula 1 pit stop strategies, race performance, and predictive race outcomes using machine learning.
""")

# =========================================================
# PAGE: RACE PREDICTION
# =========================================================


if page == "🏁 Race Prediction":


    METRICS_PATH = BASE_DIR / "data" / "processed" / "model_metrics.csv"


    metrics_df = pd.read_csv(METRICS_PATH)


    best_model_row = metrics_df.sort_values(
        by="R2",
        ascending=False
    ).iloc[0]


    st.header("🏁 Race Prediction")


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.metric("Race Entries", len(df))


    with col2:
        st.metric(
            "Seasons",
            f"{df['year'].min()}–{df['year'].max()}"
        )


    with col3:
        st.metric(
            "Best Model",
            best_model_row["Model"]
        )


    with col4:
        st.metric(
            "R² Score",
            round(best_model_row["R2"], 2)
        )


    st.divider()


    left, right = st.columns(2)


    with left:


        grid = prediction_slider(
            "Starting Grid Position",
            1,
            20,
            10
        )


        qualifying_position = prediction_slider(
            "Qualifying Position",
            1,
            20,
            10
        )


        num_pit_stops = prediction_slider(
            "Number of Pit Stops",
            0,
            5,
            2
        )


        first_pit_lap = prediction_slider(
            "First Pit Lap",
            1,
            80,
            18
        )


        last_pit_lap = prediction_slider(
            "Last Pit Lap",
            1,
            80,
            45
        )


        avg_pit_lap = prediction_slider(
            "Average Pit Lap",
            1,
            80,
            32
        )


    with right:


        avg_pit_duration = prediction_slider(
            "Average Pit Duration (ms)",
            15000,
            40000,
            22000,
            timing=True
        )


        total_pit_duration = prediction_slider(
            "Total Pit Duration (ms)",
            0,
            150000,
            45000,
            timing=True
        )


        avg_lap_time = prediction_slider(
            "Average Lap Time (ms)",
            70000,
            130000,
            95000,
            timing=True
        )


        lap_time_std = prediction_slider(
            "Lap Time Consistency (ms)",
            0,
            20000,
            3000,
            timing=True
        )


        fastest_lap_time = prediction_slider(
            "Fastest Lap Time (ms)",
            60000,
            120000,
            85000,
            timing=True
        )


        total_laps_completed = prediction_slider(
            "Total Laps Completed",
            0,
            80,
            55
        )


    input_data = pd.DataFrame({
        "grid": [grid],
        "qualifying_position": [qualifying_position],
        "num_pit_stops": [num_pit_stops],
        "first_pit_lap": [first_pit_lap],
        "last_pit_lap": [last_pit_lap],
        "avg_pit_lap": [avg_pit_lap],
        "avg_pit_duration": [avg_pit_duration],
        "total_pit_duration": [total_pit_duration],
        "avg_lap_time": [avg_lap_time],
        "lap_time_std": [lap_time_std],
        "fastest_lap_time": [fastest_lap_time],
        "total_laps_completed": [total_laps_completed]
    })


    for col in model_columns:
        if col not in input_data.columns:
            input_data[col] = 0


    input_data = input_data[model_columns]


    prediction = model.predict(input_data)[0]


    st.divider()


    st.subheader("Predicted Race Outcome")


    st.metric(
        "Predicted Position Change",
        round(prediction, 2)
    )


    if prediction > 0:


        st.success(
            f"Driver is predicted to gain approximately {round(prediction,2)} positions."
        )


    elif prediction < 0:


        st.error(
            f"Driver is predicted to lose approximately {abs(round(prediction,2))} positions."
        )


    else:


        st.info("Minimal position change predicted.")

# =========================================================
# PAGE: STRATEGY ANALYSIS
# =========================================================

elif page == "📊 Strategy Analysis":


    st.header("📊 Strategy Analysis Dashboard")


    st.markdown(
        """
        Explore Formula 1 race strategy patterns, pit stop performance,
        and constructor-level race analytics.
        """
    )


    st.divider()


    # =====================================================
    # FILTERS
    # =====================================================


    filter1, filter2, filter3 = st.columns(3)

    with filter1:
        selected_year = st.selectbox(
            "Season",
            sorted(df["year"].unique())
        )

    # Filter available constructors AFTER season is selected
    year_df = df[df["year"] == selected_year]

    available_constructors = sorted(
        year_df["constructor_clean"].dropna().unique().tolist()
    )

    with filter2:
        selected_constructor = st.selectbox(
            "Constructor",
            ["All"] + available_constructors
        )

    # Filter available pit stop values AFTER year + constructor
    filtered_for_pit = year_df.copy()

    if selected_constructor != "All":
        filtered_for_pit = filtered_for_pit[
            filtered_for_pit["constructor_clean"] == selected_constructor
        ]

    available_pit_stops = sorted(
        filtered_for_pit["num_pit_stops"].dropna().unique().tolist()
    )

    with filter3:
        selected_pit_stops = st.selectbox(
            "Pit Stops",
            ["All"] + available_pit_stops
        )

    # =====================================================
    # FILTER DATA
    # =====================================================


    filtered_df = year_df.copy()


    if selected_constructor != "All":


        filtered_df = filtered_df[
            filtered_df["constructor_clean"] == selected_constructor
        ]


    if selected_pit_stops != "All":


        filtered_df = filtered_df[
            filtered_df["num_pit_stops"] == selected_pit_stops
        ]


    st.divider()


    # =====================================================
    # QUICK STATS
    # =====================================================


    st.subheader("🏁 Quick Statistics")


    c1, c2, c3, c4 = st.columns(4)


    with c1:


        st.metric(
            "Entries",
            len(filtered_df)
        )


    with c2:


        st.metric(
            "Avg Position Change",
            round(filtered_df["position_change"].mean(), 2)
        )


    with c3:


        avg_pit = filtered_df["avg_pit_duration"].mean()


        st.metric(
            "Avg Pit Duration",
            format_f1_time(avg_pit)
        )


    with c4:


        avg_lap = filtered_df["avg_lap_time"].mean()


        st.metric(
            "Avg Lap Time",
            format_f1_time(avg_lap)
        )


    st.divider()


    # =====================================================
    # POSITION CHANGE LEADERS
    # =====================================================


    left, right = st.columns(2)


    with left:


        st.subheader("📈 Biggest Position Gainers")


        gainers = filtered_df.sort_values(
            by="position_change",
            ascending=False
        )[
            [
                "driver_name",
                "constructor_clean",
                "grid",
                "positionOrder",
                "position_change"
            ]
        ].head(10)


        st.dataframe(
            gainers,
            use_container_width=True
        )


    with right:


        st.subheader("📉 Biggest Position Losers")


        losers = filtered_df.sort_values(
            by="position_change",
            ascending=True
        )[
            [
                "driver_name",
                "constructor_clean",
                "grid",
                "positionOrder",
                "position_change"
            ]
        ].head(10)


        st.dataframe(
            losers,
            use_container_width=True
        )


    st.divider()


    # =====================================================
    # CONSTRUCTOR ANALYTICS
    # =====================================================


    st.subheader("🏎️ Constructor Strategy Comparison")


    constructor_summary = (
        filtered_df.groupby("constructor_clean")
        .agg({
            "position_change": "mean",
            "avg_pit_duration": "mean",
            "avg_lap_time": "mean",
            "num_pit_stops": "mean"
        })
        .reset_index()
    )


    constructor_summary.columns = [
        "Constructor",
        "Avg Position Change",
        "Avg Pit Duration",
        "Avg Lap Time",
        "Avg Pit Stops"
    ]


    st.dataframe(
        constructor_summary,
        use_container_width=True
    )


    st.divider()


    # =====================================================
    # VISUALIZATIONS
    # =====================================================


    st.subheader("📊 Strategy Visualizations")


    viz1, viz2 = st.columns(2)


    with viz1:


        st.markdown("#### Average Pit Duration by Constructor")


        pit_chart = (
            filtered_df.groupby("constructor_clean")[
                "avg_pit_duration"
            ]
            .mean()
            .sort_values()
        )


        st.bar_chart(pit_chart)


    with viz2:


        st.markdown("#### Average Position Change by Constructor")


        pos_chart = (
            filtered_df.groupby("constructor_clean")[
                "position_change"
            ]
            .mean()
            .sort_values()
        )


        st.bar_chart(pos_chart)


    st.divider()


    # =====================================================
    # FILTERED DATASET
    # =====================================================


    st.subheader("🗂️ Filtered Dataset Preview")


    preview_columns = [
        "driver_name",
        "constructor_clean",
        "grid",
        "positionOrder",
        "position_change",
        "num_pit_stops",
        "avg_pit_duration",
        "avg_lap_time"
    ]


    st.dataframe(
        filtered_df[preview_columns].head(100),
        use_container_width=True
    )

# =========================================================
# PAGE: MODEL PERFORMANCE
# =========================================================

elif page == "🤖 Model Performance":

    st.header("🤖 Model Performance Dashboard")

    METRICS_PATH = BASE_DIR / "data" / "processed" / "model_metrics.csv"
    FEATURE_IMPORTANCE_PATH = BASE_DIR / "data" / "processed" / "feature_importance.csv"

    metrics_df = pd.read_csv(METRICS_PATH)
    feature_importance_df = pd.read_csv(FEATURE_IMPORTANCE_PATH)

    best_model_row = metrics_df.sort_values(by="R2", ascending=False).iloc[0]

    st.markdown("### 🏆 Best Model Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Best Model", best_model_row["Model"])

    with c2:
        st.metric("Best R²", round(best_model_row["R2"], 2))

    with c3:
        st.metric("Best MAE", round(best_model_row["MAE"], 2))

    with c4:
        st.metric("Best RMSE", round(best_model_row["RMSE"], 2))

    st.divider()

    st.markdown("### 📊 Model Comparison")

    metric_choice = st.selectbox(
        "Choose Evaluation Metric",
        ["R2", "MAE", "RMSE"]
    )

    sorted_metrics = metrics_df.sort_values(
        by=metric_choice,
        ascending=False if metric_choice == "R2" else True
    )

    st.dataframe(
        sorted_metrics,
        width="stretch"
    )

    st.bar_chart(
        sorted_metrics.set_index("Model")[metric_choice]
    )

    st.divider()

    st.markdown("### 🔍 Compare Individual Models")

    selected_model = st.selectbox(
        "Select Model",
        metrics_df["Model"].tolist()
    )

    selected_row = metrics_df[
        metrics_df["Model"] == selected_model
    ].iloc[0]

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("MAE", round(selected_row["MAE"], 2))

    with m2:
        st.metric("RMSE", round(selected_row["RMSE"], 2))

    with m3:
        st.metric("R²", round(selected_row["R2"], 2))

    if selected_model == best_model_row["Model"]:
        st.success(
            f"{selected_model} is currently the strongest model based on R² score."
        )
    else:
        st.info(
            f"{selected_model} is useful for comparison, but {best_model_row['Model']} performs best overall."
        )

    st.divider()

    st.markdown("### 🧠 Feature Importance")

    top_features = feature_importance_df.head(15)

    st.bar_chart(
        top_features.set_index("feature")["importance"]
    )

    st.caption(
        "Feature importance is based on the Random Forest model, which helps identify which race and strategy variables contributed most to predictions."
    )

    st.divider()

    st.markdown("### 🏁 Model Interpretation")

    st.info(
        """
        Random Forest achieved the strongest predictive performance, suggesting that Formula 1 race outcomes are influenced by nonlinear relationships between grid position, qualifying performance, lap pace, and pit strategy variables.
        """
    )

# =========================================================
# PAGE: ABOUT
# =========================================================

elif page == "ℹ️ About Project":

    st.header("ℹ️ About This Project")

    st.markdown("""
    ### 🏁 Research Question

    To what extent can Formula 1 pit stop strategy and race-performance variables
    predict a driver's finishing position delta?

    In this project, **finishing position delta** is defined as:

    `Starting Grid Position - Final Finishing Position`

    Positive values indicate that a driver gained positions during the race, while
    negative values indicate that a driver lost positions.

    ---

    ### 📊 Dataset

    This project uses historical Formula 1 race data from the Kaggle Formula 1
    World Championship dataset. The final modeling dataset combines:

    - Race results
    - Qualifying results
    - Pit stop records
    - Lap timing data
    - Constructor information
    - Driver information

    The data was cleaned, merged, and engineered into a unified race-level dataset
    for machine learning and strategy analysis.

    ---

    ### 🛠️ Feature Engineering

    The model uses race strategy and performance features such as:

    - Starting grid position
    - Qualifying position
    - Number of pit stops
    - First, last, and average pit lap
    - Average and total pit stop duration
    - Average lap time
    - Fastest lap time
    - Lap time consistency
    - Total laps completed

    Constructor names were also cleaned to reduce naming inconsistencies while
    preserving historical team identities where appropriate.

    ---

    ### 🤖 Machine Learning Models

    Four regression models were trained and compared:

    - Linear Regression
    - Decision Tree Regression
    - Random Forest Regression
    - Gradient Boosting Regression

    The models were evaluated using:

    - Mean Absolute Error (MAE)
    - Root Mean Squared Error (RMSE)
    - R² Score

    Random Forest Regression achieved the strongest overall performance and is
    used as the primary prediction model in this dashboard.

    ---

    ### 🧠 Main Finding

    The results suggest that Formula 1 race outcomes are influenced by nonlinear
    interactions between qualifying performance, pit stop execution, lap pace, and
    race consistency.

    While no model can perfectly predict race outcomes due to unpredictable factors
    such as weather, safety cars, mechanical failures, and race incidents, the
    dashboard demonstrates that historical strategy data contains meaningful
    predictive information.

    ---

    ### 🖥️ Dashboard Purpose

    This Streamlit dashboard allows users to:

    - Simulate race strategy inputs
    - Predict finishing position delta
    - Compare model performance
    - Analyze constructor-level strategy trends
    - Explore historical race-performance patterns

    The goal is to turn the machine learning pipeline into an interactive tool for
    Formula 1 strategy exploration.
    """)

    st.divider()

    st.subheader("GitHub Repository")

    st.link_button(
        "Open GitHub Repository",
        "https://github.com/thomaschung1/F1-Pit-Strategy-Analysis"
    )
