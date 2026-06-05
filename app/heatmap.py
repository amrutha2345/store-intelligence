import os
import json

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

            try:

                events.append(
                    json.loads(line)
                )

            except Exception:
                pass

    return events


def get_heatmap(
    store_id
):

    events = load_events()

    store_events = [

        event

        for event in events

        if event.get(
            "store_id"
        ) == store_id
    ]

    zone_stats = {}

    for event in store_events:

        if event.get(
            "event_type"
        ) != "ZONE_DWELL":

            continue

        zone_id = event.get(
            "zone_id",
            "UNKNOWN"
        )

        visitor_id = event.get(
            "visitor_id",
            "UNKNOWN"
        )

        dwell_ms = event.get(
            "dwell_ms",
            0
        )

        if zone_id not in zone_stats:

            zone_stats[zone_id] = {

                "visitors": set(),

                "total_dwell_ms": 0
            }

        zone_stats[zone_id][
            "visitors"
        ].add(
            visitor_id
        )

        zone_stats[zone_id][
            "total_dwell_ms"
        ] += dwell_ms

    max_visits = 1

    if zone_stats:

        max_visits = max(

            len(
                zone["visitors"]
            )

            for zone in zone_stats.values()
        )

    heatmap_data = []

    for zone_id, data in zone_stats.items():

        visits = len(
            data["visitors"]
        )

        avg_dwell_seconds = 0

        if visits > 0:

            avg_dwell_seconds = round(

                (
                    data[
                        "total_dwell_ms"
                    ]
                    /
                    visits
                )
                /
                1000,

                2
            )

        normalized_score = round(

            (
                visits
                /
                max_visits
            )
            * 100,

            2
        )

        heatmap_data.append({

            "zone_id":
                zone_id,

            "visits":
                visits,

            "avg_dwell_seconds":
                avg_dwell_seconds,

            "normalized_score":
                normalized_score
        })

    heatmap_data.sort(

        key=lambda x:
            x[
                "normalized_score"
            ],

        reverse=True
    )

    return {

        "store_id":
            store_id,

        "zones":
            heatmap_data,

        "data_confidence":
            "HIGH"
    }


if __name__ == "__main__":

    result = get_heatmap(
        "STORE_BLR_001"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )