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

DETECTIONS_FILE = os.path.join(
    OUTPUT_DIR,
    "detections.json"
)

TRACKED_FILE = os.path.join(
    OUTPUT_DIR,
    "tracked_events.json"
)


def load_detections():

    if not os.path.exists(
        DETECTIONS_FILE
    ):
        return []

    with open(
        DETECTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def determine_event_type(
    camera_id
):

    camera = str(
        camera_id
    ).upper()

    if "ENTRY" in camera:
        return "ENTRY"

    if "EXIT" in camera:
        return "EXIT"

    if "BILLING" in camera:
        return "BILLING_QUEUE_JOIN"

    return "ZONE_DWELL"


def current_timestamp():

    return datetime.now(
        timezone.utc
    ).isoformat()


def main():

    detections = load_detections()

    tracked_events = []

    session_counter = {}

    for detection in detections:

        track_id = detection.get(
            "track_id"
        )

        if track_id is None:
            continue

        visitor_id = (
            f"VIS_{track_id}"
        )

        if visitor_id not in session_counter:

            session_counter[
                visitor_id
            ] = 1

        else:

            session_counter[
                visitor_id
            ] += 1

        zone_id = detection.get(
            "zone_id",
            "UNKNOWN"
        )

        event_type = determine_event_type(

            detection.get(
                "camera_id"
            )
        )

        event = {

            "event_id":
                str(uuid.uuid4()),

            "store_id":
                detection.get(
                    "store_id",
                    "STORE_BLR_002"
                ),

            "camera_id":
                detection.get(
                    "camera_id",
                    "CAM_UNKNOWN"
                ),

            "visitor_id":
                visitor_id,

            "event_type":
                event_type,

            "timestamp":
                current_timestamp(),

            "zone_id":
                zone_id,

            "dwell_ms":
                detection.get(
                    "dwell_ms",
                    5000
                ),

            "is_staff":
                False,

            "confidence":
                round(
                    float(
                        detection.get(
                            "confidence",
                            0.90
                        )
                    ),
                    2
                ),

            "metadata": {

                "queue_depth":

                    1

                    if event_type ==
                    "BILLING_QUEUE_JOIN"

                    else None,

                "sku_zone":
                    zone_id,

                "session_seq":

                    session_counter[
                        visitor_id
                    ]
            }
        }

        tracked_events.append(
            event
        )

    with open(
        TRACKED_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            tracked_events,
            f,
            indent=4
        )

    print(
        f"Generated {len(tracked_events)} tracked events"
    )

    print(
        f"Saved to {TRACKED_FILE}"
    )


if __name__ == "__main__":
    main()
