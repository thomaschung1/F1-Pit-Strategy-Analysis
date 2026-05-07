import streamlit as st

def render_about_page():
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