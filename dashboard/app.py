import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    layout="wide"
)

API_BASE = "http://127.0.0.1:8000"

st.title(
    "🏪 Store Intelligence Dashboard"
)

STORE_ID = st.sidebar.selectbox(
    "Select Store",
    [
        "STORE_BLR_001",
        "STORE_BLR_002"
    ]
)


def get_json(endpoint):

    try:

        response = requests.get(
            f"{API_BASE}{endpoint}",
            timeout=10
        )

        if response.status_code != 200:

            st.error(
                f"API Error {response.status_code}"
            )

            st.code(
                response.text
            )

            return {}

        return response.json()

    except Exception as e:

        st.error(
            f"Cannot connect to API: {e}"
        )

        return {}


metrics = get_json(
    f"/stores/{STORE_ID}/metrics"
)

funnel = get_json(
    f"/stores/{STORE_ID}/funnel"
)

heatmap = get_json(
    f"/stores/{STORE_ID}/heatmap"
)

anomalies = get_json(
    f"/stores/{STORE_ID}/anomalies"
)

health = get_json(
    "/health"
)

if not metrics:

    st.stop()

# --------------------------------
# KPI SECTION
# --------------------------------

st.subheader(
    "Store Metrics"
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Visitors",
    metrics.get(
        "unique_visitors",
        0
    )
)

c2.metric(
    "Conversion %",
    metrics.get(
        "conversion_rate",
        0
    )
)

c3.metric(
    "Revenue",
    f"₹{metrics.get('total_revenue',0):,.0f}"
)

c4.metric(
    "Queue Depth",
    metrics.get(
        "queue_depth",
        0
    )
)

st.divider()

# --------------------------------
# FUNNEL
# --------------------------------

st.subheader(
    "Conversion Funnel"
)

funnel_df = pd.DataFrame({

    "Stage": [

        "Entry",

        "Zone Visit",

        "Billing",

        "Purchase"
    ],

    "Count": [

        funnel.get(
            "entry_count",
            0
        ),

        funnel.get(
            "zone_visit_count",
            0
        ),

        funnel.get(
            "billing_count",
            0
        ),

        funnel.get(
            "purchase_count",
            0
        )
    ]
})

st.bar_chart(
    funnel_df.set_index(
        "Stage"
    )
)

st.divider()

# --------------------------------
# HEATMAP
# --------------------------------

st.subheader(
    "Zone Heatmap"
)

zones = heatmap.get(
    "zones",
    []
)

if len(zones) > 0:

    heatmap_df = pd.DataFrame(
        zones
    )

    st.dataframe(
        heatmap_df,
        use_container_width=True
    )

else:

    st.info(
        "No heatmap data available"
    )

st.divider()

# --------------------------------
# ANOMALIES
# --------------------------------

st.subheader(
    "Active Anomalies"
)

active = anomalies.get(
    "active_anomalies",
    []
)

if len(active) == 0:

    st.success(
        "No anomalies detected"
    )

else:

        for anomaly in active:

            st.warning(

                f"{anomaly['anomaly_type']} | "
                f"{anomaly['severity']} | "
                f"{anomaly['suggested_action']}"
            )

st.divider()

# --------------------------------
# HEALTH
# --------------------------------

st.subheader(
    "System Health"
)

st.json(
    health
)

st.divider()

# --------------------------------
# RAW API DATA
# --------------------------------

with st.expander(
    "Debug Data"
):

    st.write(
        "Metrics"
    )

    st.json(
        metrics
    )

    st.write(
        "Funnel"
    )

    st.json(
        funnel
    )

    st.write(
        "Heatmap"
    )

    st.json(
        heatmap
    )

    st.write(
        "Anomalies"
    )

    st.json(
        anomalies
    )