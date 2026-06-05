from pydantic import BaseModel
from typing import Optional, List, Dict, Any


# --------------------------
# EVENT METADATA
# --------------------------

class EventMetadata(BaseModel):

    queue_depth: Optional[int] = None

    sku_zone: Optional[str] = None

    session_seq: int


# --------------------------
# EVENT
# --------------------------

class Event(BaseModel):

    event_id: str

    store_id: str

    camera_id: str

    visitor_id: str

    event_type: str

    timestamp: str

    zone_id: Optional[str] = None

    dwell_ms: int = 0

    is_staff: bool = False

    confidence: float

    metadata: EventMetadata


# --------------------------
# INGESTION
# --------------------------

class IngestResponse(BaseModel):

    status: str

    inserted: int

    duplicates: int

    total_events: int


# --------------------------
# METRICS
# --------------------------

class MetricsResponse(BaseModel):

    store_id: str

    unique_visitors: int

    entries: int

    exits: int

    zone_visits: int

    billing_count: int

    transactions: int

    total_revenue: float

    conversion_rate: float

    queue_depth: int

    abandonment_rate: float

    avg_dwell_time: float


# --------------------------
# FUNNEL
# --------------------------

class FunnelResponse(BaseModel):

    store_id: str

    entry_count: int

    zone_visit_count: int

    billing_count: int

    purchase_count: int

    drop_off_percent: float


# --------------------------
# HEATMAP
# --------------------------

class ZoneMetric(BaseModel):

    zone_id: str

    visits: int

    avg_dwell_seconds: float

    normalized_score: float


class HeatmapResponse(BaseModel):

    store_id: str

    zones: List[ZoneMetric]

    data_confidence: str


# --------------------------
# ANOMALIES
# --------------------------

class Anomaly(BaseModel):

    anomaly_type: str

    severity: str

    suggested_action: str


class AnomalyResponse(BaseModel):

    store_id: str

    active_anomalies: List[Anomaly]

    total_anomalies: int


# --------------------------
# HEALTH
# --------------------------

class StoreHealth(BaseModel):

    last_event: str

    event_count: int

    stale_feed: bool


class HealthResponse(BaseModel):

    status: str

    stores: Dict[str, Any]
