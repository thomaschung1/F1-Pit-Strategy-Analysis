import streamlit as st
import pandas as pd

def render_model_performance_page(METRICS_PATH, FEATURE_IMPORTANCE_PATH):
    st.header("🤖 Model Performance Dashboard")

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