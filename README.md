# Store Intelligence System

## Overview

This project is a video analytics pipeline developed for the Purplle Tech Challenge.

The system processes store CCTV footage and generates visitor events, analytics, heatmaps, funnels, anomaly detection, and a dashboard.

## Features

* Person Detection using YOLOv8
* Visitor Tracking
* Event Generation
* Store Metrics
* Conversion Funnel
* Zone Heatmap
* Anomaly Detection
* System Health Monitoring
* FastAPI Backend
* Streamlit Dashboard

## Event Schema

Each generated event follows:

```json
{
  "event_id": "uuid-v4",
  "store_id": "STORE_BLR_002",
  "camera_id": "CAM_ENTRY_01",
  "visitor_id": "VIS_123",
  "event_type": "ZONE_DWELL",
  "timestamp": "2026-03-03T14:22:10Z",
  "zone_id": "SKINCARE",
  "dwell_ms": 8400,
  "is_staff": false,
  "confidence": 0.91,
  "metadata": {
    "queue_depth": null,
    "sku_zone": "SKINCARE",
    "session_seq": 5
  }
}
```

## Project Structure

```text
app/
dashboard/
pipeline/
tests/
data/
output/
```

## Installation

```bash
pip install -r requirements.txt
```

## Run Pipeline

```bash
python pipeline/detect.py
python pipeline/tracker.py
python pipeline/emit.py
```

## Run API

```bash
uvicorn app.main:app --reload
```

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

## Run Tests

```bash
pytest tests -v
```
