# Streamlit or Dash App

import streamlit as st
import pandas as pd
import time
from performance import calculate_metrics
from plots import plot_pnl, plot_trades

st.set_page_config(page_title = "HFT Simulator Dashboard", layout="wide")
st.title("HFT Simulator Dashboard")

# Load trade log (simulate live updates)
trade_log_path = "dashboard/trade_log.csv"

placeholder = st.empty()
while True:
    try:
        df = pd.read_csv(trade_log_path)
        metrics = calculate_metrics(df)
        
        with placeholder.container():
            st.subheader("Performance Metrics")
            st.metric("Total PnL", f"${metrics['total_pnl']:.2f}")
            st.metric("Sharpe Ratio", f"${metrics['sharpe']:.2f}")
            st.metric("Max Drawdown", f"${metrics['drawdown']:.2f}")
            
            st.subheader("Trade History")
            st.dataframe(df.tail(10))
            
            st.subheader("PnL Over Time")
            st.plotly_chart(plot_trades(df), use_container_width=True)
        
        time.sleep(5) # Refresh every 5 seconds
    
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        time.sleep(5)