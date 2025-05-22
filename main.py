import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

st.title("📈 CO₂ Emission Forecast")

# Spinner while fetching data
with st.spinner("Fetching prediction data..."):
    response = requests.get("https://ecocred-api.onrender.com/predict")
    if response.status_code == 200:
        data = response.json()
        inputs = data["input"]
        predictions = data["prediction"]
        all_values = inputs + predictions

        # Generate timestamps
        now = datetime.now()
        timestamps = [now - timedelta(minutes=2), now - timedelta(minutes=1), now, now + timedelta(minutes=1), now + timedelta(minutes=2)]

        # Create DataFrame
        df = pd.DataFrame({
            "Timestamp": timestamps,
            "CO₂ Value": all_values
        })

        # Plot line chart
        st.success("Data fetched successfully!")
        st.subheader("Line Chart (Time vs CO₂ Value)")
        fig = px.line(df, x="Timestamp", y="CO₂ Value", markers=True, title="CO₂ Emission: Last & Predicted")
        fig.update_layout(xaxis_title="Time", yaxis_title="CO₂ Value (ppm)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Failed to fetch data from API.")
