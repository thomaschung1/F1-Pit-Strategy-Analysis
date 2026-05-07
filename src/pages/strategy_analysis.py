import streamlit as st
from src.formatting import format_lap_time

def render_strategy_analysis_page(df):
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
            format_lap_time(avg_pit)
        )


    with c4:
        avg_lap = filtered_df["avg_lap_time"].mean()
        st.metric(
            "Avg Lap Time",
            format_lap_time(avg_lap)
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
            width='stretch'
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
            width='stretch'
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
        width='stretch'
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
        width='stretch'
    )