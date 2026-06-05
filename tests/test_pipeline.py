"""
Prompt Used:

Validate event generation pipeline.

Requirements:
1. Events must contain required fields.
2. event_id must exist.
3. event_type must exist.
4. store_code must exist.
5. camera_id must exist.
6. Output should not be empty.
"""
import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

EVENTS_FILE = os.path.join(
    BASE_DIR,
    "output",
    "events.jsonl"
)


def load_events():

    events = []

    if not os.path.exists(
        EVENTS_FILE
    ):
        return events

    with open(
        EVENTS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            events.append(
                json.loads(line)
            )

    return events


def test_events_file_exists():

    assert os.path.exists(
        EVENTS_FILE
    )


def test_events_generated():

    events = load_events()

    assert len(
        events
    ) > 0


def test_event_schema():

    events = load_events()

    event = events[0]

    required_fields = [

        "event_id",

        "store_id",

        "camera_id",

        "visitor_id",

        "event_type",

        "timestamp",

        "zone_id",

        "dwell_ms",

        "is_staff",

        "confidence",

        "metadata"
    ]

    for field in required_fields:

        assert field in event


def test_metadata_schema():

    events = load_events()

    event = events[0]

    metadata = event[
        "metadata"
    ]

    assert (
        "queue_depth"
        in metadata
    )

    assert (
        "sku_zone"
        in metadata
    )

    assert (
        "session_seq"
        in metadata
    )


def test_store_id_exists():

    events = load_events()

    for event in events:

        assert event[
            "store_id"
        ] is not None


def test_visitor_id_exists():

    events = load_events()

    for event in events:

        assert event[
            "visitor_id"
        ] is not None


def test_confidence_range():

    events = load_events()

    for event in events:

        confidence = event[
            "confidence"
        ]

        assert (
            0.0
            <= confidence
            <= 1.0
        )


def test_dwell_non_negative():

    events = load_events()

    for event in events:

        assert (
            event[
                "dwell_ms"
            ]
            >= 0
        )


def test_event_types():

    events = load_events()

    allowed = [

        "ENTRY",

        "EXIT",

        "ZONE_DWELL",

        "BILLING_QUEUE_JOIN",

        "BILLING_QUEUE_EXIT"
    ]

    for event in events:

        assert (
            event[
                "event_type"
            ]
            in allowed
        )


def test_session_seq_exists():

    events = load_events()

    for event in events:

        assert (

            event[
                "metadata"
            ][
                "session_seq"
            ]

            >= 1
        )