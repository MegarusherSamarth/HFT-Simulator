# Custom Charts

import plotly.express as px

def plot_pnl(df):
    df["cumulative_pnl"] = df["pnl"].cumsum()
    fig = px.line(df, x="timestamp", y="cumulative_pnl", title="Cumulative PnL")
    return fig

def plot_trades(df):
    fig = px.scatter(df, x="timestamp", y="price", color="signal", size="volume", title="Trade Execution Map")
    return fig