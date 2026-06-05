import os
import json
from datetime import (
    datetime,
    timezone
)

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

EVENTS_FILE = os.path.join(
    BASE_DIR,
    "output",
    "events.jsonl"
)

STALE_THRESHOLD_MINUTES = 60


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


def get_health():

    events = load_events()

    if not events:

        return {

            "status":
                "NO_DATA",

            "stores":
                {}
        }

    stores = {}

    for event in events:

        store_id = event.get(
            "store_id",
            "UNKNOWN"
        )

        timestamp = event.get(
            "timestamp"
        )

        if not timestamp:
            continue

        if store_id not in stores:

            stores[store_id] = {

                "last_event":
                    timestamp,

                "event_count":
                    1
            }

        else:

            stores[store_id][
                "event_count"
            ] += 1

            if timestamp > stores[
                store_id
            ][
                "last_event"
            ]:

                stores[
                    store_id
                ][
                    "last_event"
                ] = timestamp

    now = datetime.now(
        timezone.utc
    )

    for store_id in stores:

        try:

            last_event = datetime.fromisoformat(

                stores[
                    store_id
                ][
                    "last_event"
                ].replace(
                    "Z",
                    "+00:00"
                )
            )

            age_minutes = (

                now -
                last_event

            ).total_seconds() / 60

            stores[
                store_id
            ][
                "stale_feed"
            ] = (

                age_minutes >
                STALE_THRESHOLD_MINUTES
            )

        except Exception:

            stores[
                store_id
            ][
                "stale_feed"
            ] = True

    return {

        "status":
            "HEALTHY",

        "stores":
            stores
    }


if __name__ == "__main__":

    result = get_health()

    print(
        json.dumps(
            result,
            indent=4
        )
    )