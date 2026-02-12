import pandas as pd
from pathlib import Path
import numpy as np

# File path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "vm_data.csv"


def load_vm_data():

    # Read CSV
    df = pd.read_csv(DATA_PATH)

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Aggregate per VM
    grouped = (
        df.groupby("vm_id")
        .agg({
            "cpu_usage": "mean",
            "memory_usage": "mean",
            "network_traffic": "mean",
            "power_consumption": "mean",
            "execution_time": "mean"
        })
        .reset_index()
    )

    # =========================
    # Derived Metrics
    # =========================

    # Monthly cost formula
    grouped["monthly_cost"] = (
        grouped["cpu_usage"] * 2.0 +
        grouped["memory_usage"] * 1.2 +
        grouped["power_consumption"] * 0.15 +
        grouped["execution_time"] * 0.5
    )

    # Avg Utilization (NEW — UI + Rightsizing)
    grouped["avg_utilization"] = (
        grouped["cpu_usage"] +
        grouped["memory_usage"]
    ) / 2

    # =========================
    # UI Helper Fields
    # =========================

    grouped["name"] = grouped["vm_id"]
    grouped["region"] = "Dataset"
    grouped["size"] = "Standard"

    # Clean NaN / Inf
    grouped = grouped.replace([np.inf, -np.inf], 0).fillna(0)

    # Return JSON format
    return grouped.to_dict(orient="records")
