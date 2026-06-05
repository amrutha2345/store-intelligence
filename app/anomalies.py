import json
import os
import sys

CURRENT_DIR = os.path.dirname(
    __file__
)

if CURRENT_DIR not in sys.path:

    sys.path.append(
        CURRENT_DIR
    )

from metrics import (
    calculate_metrics
)


def detect_anomalies(
    store_id
):

    metrics = calculate_metrics(
        store_id
    )

    anomalies = []

    conversion_rate = metrics.get(
        "conversion_rate",
        0
    )

    abandonment_rate = metrics.get(
        "abandonment_rate",
        0
    )

    visitors = metrics.get(
        "unique_visitors",
        0
    )

    revenue = metrics.get(
        "total_revenue",
        0
    )

    queue_depth = metrics.get(
        "queue_depth",
        0
    )

    avg_dwell_time = metrics.get(
        "avg_dwell_time",
        0
    )

    # ------------------------
    # LOW CONVERSION
    # ------------------------

    if conversion_rate < 30:

        anomalies.append({

            "anomaly_type":
                "LOW_CONVERSION",

            "severity":
                "HIGH",

            "suggested_action":
                "Improve product placement and customer engagement."
        })

    # ------------------------
    # HIGH ABANDONMENT
    # ------------------------

    if abandonment_rate > 20:

        anomalies.append({

            "anomaly_type":
                "HIGH_ABANDONMENT",

            "severity":
                "HIGH",

            "suggested_action":
                "Reduce queue waiting time and increase staffing."
        })

    # ------------------------
    # LOW FOOTFALL
    # ------------------------

    if visitors < 50:

        anomalies.append({

            "anomaly_type":
                "LOW_FOOTFALL",

            "severity":
                "MEDIUM",

            "suggested_action":
                "Run promotions and marketing campaigns."
        })

    # ------------------------
    # LOW REVENUE
    # ------------------------

    if revenue < 50000:

        anomalies.append({

            "anomaly_type":
                "LOW_REVENUE",

            "severity":
                "MEDIUM",

            "suggested_action":
                "Increase basket size and improve conversion."
        })

    # ------------------------
    # QUEUE CONGESTION
    # ------------------------

    if queue_depth > 25:

        anomalies.append({

            "anomaly_type":
                "QUEUE_CONGESTION",

            "severity":
                "HIGH",

            "suggested_action":
                "Open additional billing counters."
        })

    # ------------------------
    # LOW DWELL TIME
    # ------------------------

    if (
        avg_dwell_time > 0
        and
        avg_dwell_time < 5
    ):

        anomalies.append({

            "anomaly_type":
                "LOW_DWELL_TIME",

            "severity":
                "LOW",

            "suggested_action":
                "Improve product visibility and customer engagement."
        })

    return {

        "store_id":
            store_id,

        "active_anomalies":
            anomalies,

        "total_anomalies":
            len(anomalies)
    }


if __name__ == "__main__":

    result = detect_anomalies(
        "STORE_BLR_001"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )