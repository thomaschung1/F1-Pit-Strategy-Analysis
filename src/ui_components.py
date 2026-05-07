import streamlit as st
from src.formatting import format_lap_time

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
        st.caption(f"⏱️ Lap Time Format: {format_lap_time(selected)}")
    else:
        st.markdown("<div class='caption-spacer'></div>", unsafe_allow_html=True)

    return selected

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