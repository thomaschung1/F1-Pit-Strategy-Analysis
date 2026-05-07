import streamlit as st
import pandas as pd

from src.ui_components import prediction_slider

def render_race_prediction_page(df, model, model_columns, METRICS_PATH):
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