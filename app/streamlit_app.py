import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "processed" / "f1_pit_strategy_model_data.csv"
MODEL_PATH = BASE_DIR / "models" / "random_forest_model.pkl"
MODEL_COLUMNS_PATH = BASE_DIR / "models" / "model_columns.pkl"
FIGURES_DIR = BASE_DIR / "figures"

st.set_page_config(
    page_title="F1 Pit Strategy Analysis",
    layout="wide"
)

st.title("Formula 1 Pit Strategy Analysis")

st.write("""
This dashboard explores how Formula 1 pit stop strategy relates to race performance.
The project uses historical race, qualifying, lap time, and pit stop data to predict
position change during a race.
""")

df = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)
model_columns = joblib.load(MODEL_COLUMNS_PATH)

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Key Dataset Information")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

with col3:
    st.metric("Seasons", f"{int(df['year'].min())}–{int(df['year'].max())}")

st.subheader("Saved Visualizations")

figures = [
    "position_change_distribution.png",
    "pit_stops_vs_position_change.png",
    "qualifying_vs_position_change.png",
    "lap_time_vs_position_change.png",
    "feature_importance.png",
    "model_comparison.png"
]

for fig in figures:
    fig_path = FIGURES_DIR / fig
    if fig_path.exists():
        st.image(str(fig_path), caption=fig.replace("_", " ").replace(".png", "").title())
        
st.divider()

st.subheader("Interactive Race Outcome Prediction")

st.write("""
Use the controls below to simulate race conditions and predict how many positions
a driver is expected to gain or lose during a race.
""")

col1, col2 = st.columns(2)

with col1:
    grid = st.slider("Starting Grid Position", 1, 20, 10)
    qualifying_position = st.slider("Qualifying Position", 1, 20, 10)
    num_pit_stops = st.slider("Number of Pit Stops", 0, 5, 2)
    first_pit_lap = st.slider("First Pit Lap", 0, 80, 18)
    last_pit_lap = st.slider("Last Pit Lap", 0, 80, 45)
    avg_pit_lap = st.slider("Average Pit Lap", 0, 80, 32)

with col2:
    avg_pit_duration = st.slider("Average Pit Duration (ms)", 15000, 40000, 22000)
    total_pit_duration = st.slider("Total Pit Duration (ms)", 0, 150000, 45000)
    avg_lap_time = st.slider("Average Lap Time (ms)", 70000, 130000, 90000)
    lap_time_std = st.slider("Lap Time Standard Deviation", 0, 20000, 3000)
    fastest_lap_time = st.slider("Fastest Lap Time (ms)", 60000, 120000, 85000)
    total_laps_completed = st.slider("Total Laps Completed", 0, 80, 55)

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

st.metric(
    "Predicted Position Change",
    round(prediction, 2)
)

if prediction > 0:
    st.success(f"The model predicts the driver may gain about {round(prediction, 2)} positions.")
elif prediction < 0:
    st.error(f"The model predicts the driver may lose about {abs(round(prediction, 2))} positions.")
else:
    st.info("The model predicts no major position change.")
