import os
import json

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

EVENTS_FILE = os.path.join(
    OUTPUT_DIR,
    "events.jsonl"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


def load_events():

    if not os.path.exists(
        EVENTS_FILE
    ):
        return []

    events = []

    with open(
        EVENTS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if line:

                try:

                    events.append(
                        json.loads(line)
                    )

                except Exception:
                    pass

    return events


def save_event(event):

    with open(
        EVENTS_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(event)
        )

        f.write("\n")


def ingest_events(events):

    existing = load_events()

    existing_ids = {

        event["event_id"]

        for event in existing

        if "event_id" in event
    }

    inserted = 0
    duplicates = 0

    for event in events:

        event_id = event.get(
            "event_id"
        )

        if not event_id:
            continue

        if event_id in existing_ids:

            duplicates += 1

            continue

        save_event(event)

        inserted += 1

        existing_ids.add(
            event_id
        )

    return {

        "status":
            "success",

        "inserted":
            inserted,

        "duplicates":
            duplicates,

        "total_events":
            len(existing_ids)
    }


def get_store_events(
    store_id
):

    events = load_events()

    return [

        event

        for event in events

        if event.get(
            "store_id"
        ) == store_id
    ]


if __name__ == "__main__":

    events = load_events()

    print(
        f"Loaded {len(events)} events"
    )