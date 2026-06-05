from fastapi import FastAPI
from typing import List

from app.models import (
    Event
)

from app.ingestion import (
    ingest_events
)

from app.metrics import (
    calculate_metrics
)

from app.funnel import (
    get_store_funnel
)

from app.heatmap import (
    get_heatmap
)

from app.anomalies import (
    detect_anomalies
)

from app.health import (
    get_health
)

app = FastAPI(
    title="Store Intelligence API",
    description="Purplle Tech Challenge 2026",
    version="1.0.0"
)


# -------------------------
# ROOT
# -------------------------

@app.get("/")
def root():

    return {

        "application":
            "Store Intelligence System",

        "version":
            "1.0.0",

        "status":
            "running"
    }


# -------------------------
# HEALTH
# -------------------------

@app.get("/health")
def health():

    return get_health()


# -------------------------
# INGEST EVENTS
# -------------------------

@app.post("/events/ingest")
def ingest(
    events: List[dict]
):

    return ingest_events(
        events
    )


# -------------------------
# METRICS
# -------------------------

@app.get(
    "/stores/{store_id}/metrics"
)
def metrics(
    store_id: str
):

    return calculate_metrics(
        store_id
    )


# -------------------------
# FUNNEL
# -------------------------

@app.get(
    "/stores/{store_id}/funnel"
)
def funnel(
    store_id: str
):

    return get_store_funnel(
        store_id
    )


# -------------------------
# HEATMAP
# -------------------------

@app.get(
    "/stores/{store_id}/heatmap"
)
def heatmap(
    store_id: str
):

    return get_heatmap(
        store_id
    )


# -------------------------
# ANOMALIES
# -------------------------

@app.get(
    "/stores/{store_id}/anomalies"
)
def anomalies(
    store_id: str
):

    return detect_anomalies(
        store_id
    )


# -------------------------
# EVENTS
# -------------------------

@app.get(
    "/stores/{store_id}/events"
)
def store_events(
    store_id: str
):

    from app.ingestion import (
        get_store_events
    )

    return get_store_events(
        store_id
    )


# -------------------------
# API INFO
# -------------------------

@app.get("/info")
def info():

    return {

        "challenge":
            "Purplle Tech Challenge 2026",

        "services": [

            "metrics",

            "funnel",

            "heatmap",

            "anomalies",

            "health"
        ]
    }