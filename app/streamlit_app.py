import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import joblib

from src.styles import get_css
from src.ui_components import TEAM_THEMES
from src.data_utils import clean_constructor_names
from src.config import (
    DATA_PATH,
    MODEL_PATH,
    MODEL_COLUMNS_PATH,
    FIGURES_DIR,
    METRICS_PATH,
    FEATURE_IMPORTANCE_PATH
)

from src.pages.about import render_about_page
from src.pages.strategy_analysis import render_strategy_analysis_page
from src.pages.race_prediction import render_race_prediction_page
from src.pages.model_performance import render_model_performance_page

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(DATA_PATH)

df = clean_constructor_names(df)

model = joblib.load(MODEL_PATH)

model_columns = joblib.load(MODEL_COLUMNS_PATH)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="F1 Pit Stop Strategy Predictions",
    page_icon="🏎️",
    layout="wide"
)

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

st.markdown(
    get_css(theme)
    , unsafe_allow_html=True
)

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
    render_race_prediction_page(
        df, 
        model, 
        model_columns, 
        METRICS_PATH
    )

# =========================================================
# PAGE: STRATEGY ANALYSIS
# =========================================================

elif page == "📊 Strategy Analysis":
    render_strategy_analysis_page(df)

# =========================================================
# PAGE: MODEL PERFORMANCE
# =========================================================

elif page == "🤖 Model Performance":
    render_model_performance_page(
        METRICS_PATH,
        FEATURE_IMPORTANCE_PATH
    )

# =========================================================
# PAGE: ABOUT
# =========================================================

elif page == "ℹ️ About Project":
    render_about_page()