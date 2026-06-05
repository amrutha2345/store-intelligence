import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

EVENTS_FILE = os.path.join(
    BASE_DIR,
    "output",
    "events.jsonl"
)

POS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "POS - sample transactionsb1e826f.csv"
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


def load_pos():

    if not os.path.exists(
        POS_FILE
    ):
        return pd.DataFrame()

    return pd.read_csv(
        POS_FILE
    )


def get_store_funnel(
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

    entry_visitors = set()

    zone_visitors = set()

    billing_visitors = set()

    for event in store_events:

        visitor_id = event.get(
            "visitor_id"
        )

        if not visitor_id:
            continue

        event_type = str(
            event.get(
                "event_type",
                ""
            )
        ).upper()

        if event_type == "ENTRY":

            entry_visitors.add(
                visitor_id
            )

        elif event_type == "ZONE_DWELL":

            zone_visitors.add(
                visitor_id
            )

        elif event_type in [

            "BILLING_QUEUE_JOIN",
            "BILLING_QUEUE_EXIT"

        ]:

            billing_visitors.add(
                visitor_id
            )

    entry_count = len(
        entry_visitors
    )

    zone_count = len(
        zone_visitors
    )

    billing_count = len(
        billing_visitors
    )

    pos = load_pos()

    purchase_count = 0

    if not pos.empty:

        purchase_count = len(
            pos
        )

    # Maintain proper funnel order

    if entry_count == 0:

        entry_count = max(
            zone_count,
            billing_count,
            purchase_count
        )

    zone_count = min(
        zone_count,
        entry_count
    )

    billing_count = min(
        billing_count,
        zone_count
    )

    purchase_count = min(
        purchase_count,
        billing_count
    )

    drop_off_percent = 0

    if entry_count > 0:

        drop_off_percent = round(

            (
                (
                    entry_count
                    -
                    purchase_count
                )
                /
                entry_count
            )
            * 100,

            2
        )

    return {

        "store_id":
            store_id,

        "entry_count":
            entry_count,

        "zone_visit_count":
            zone_count,

        "billing_count":
            billing_count,

        "purchase_count":
            purchase_count,

        "drop_off_percent":
            drop_off_percent
    }


if __name__ == "__main__":

    result = get_store_funnel(
        "STORE_BLR_001"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )