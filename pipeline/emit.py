import os
import json
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

TRACKED_FILE = os.path.join(
    OUTPUT_DIR,
    "tracked_events.json"
)

FINAL_FILE = os.path.join(
    OUTPUT_DIR,
    "events.jsonl"
)


def generate_event_id():

    return str(
        uuid.uuid4()
    )


def load_events():

    if not os.path.exists(
        TRACKED_FILE
    ):

        print(
            "tracked_events.json not found"
        )

        return []

    with open(
        TRACKED_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def build_event(event):

    event_type = event.get(
        "event_type",
        "ZONE_DWELL"
    )

    zone_id = event.get(
        "zone_id",
        "UNKNOWN"
    )

    queue_depth = None

    if event_type == "BILLING_QUEUE_JOIN":

        queue_depth = event.get(
            "queue_depth",
            1
        )

    return {

        "event_id":
            generate_event_id(),

        "store_id":
            event.get(
                "store_id",
                "STORE_BLR_002"
            ),

        "camera_id":
            event.get(
                "camera_id",
                "CAM_UNKNOWN"
            ),

        "visitor_id":
            event.get(
                "visitor_id",
                "VIS_UNKNOWN"
            ),

        "event_type":
            event_type,

        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "zone_id":
            zone_id,

        "dwell_ms":
            event.get(
                "dwell_ms",
                5000
            ),

        "is_staff":
            event.get(
                "is_staff",
                False
            ),

        "confidence":
            round(
                float(
                    event.get(
                        "confidence",
                        0.90
                    )
                ),
                2
            ),

        "metadata": {

            "queue_depth":
                queue_depth,

            "sku_zone":
                zone_id,

            "session_seq":
                event.get(
                    "session_seq",
                    1
                )
        }
    }


def main():

    tracked_events = load_events()

    final_events = []

    for event in tracked_events:

        final_events.append(
            build_event(
                event
            )
        )

    with open(
        FINAL_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        for event in final_events:

            f.write(
                json.dumps(event)
            )

            f.write("\n")

    print(
        f"Created {len(final_events)} events"
    )

    print(
        f"Saved to {FINAL_FILE}"
    )


if __name__ == "__main__":
    main()