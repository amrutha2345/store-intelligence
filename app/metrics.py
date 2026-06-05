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


def calculate_metrics(
    store_id
):

    events = load_events()

    store_events = [

        e

        for e in events

        if e.get(
            "store_id"
        ) == store_id
    ]

    unique_visitors = len({

        e.get(
            "visitor_id"
        )

        for e in store_events

        if e.get(
            "visitor_id"
        )
    })

    entries = len({

        e.get(
            "visitor_id"
        )

        for e in store_events

        if e.get(
            "event_type"
        ) == "ENTRY"
    })

    exits = len({

        e.get(
            "visitor_id"
        )

        for e in store_events

        if e.get(
            "event_type"
        ) == "EXIT"
    })

    zone_visits = len({

        (
            e.get(
                "visitor_id"
            ),
            e.get(
                "zone_id"
            )
        )

        for e in store_events

        if e.get(
            "event_type"
        ) == "ZONE_DWELL"
    })

    billing_visitors = {

        e.get(
            "visitor_id"
        )

        for e in store_events

        if e.get(
            "event_type"
        ) == "BILLING_QUEUE_JOIN"
    }

    queue_depth = len(
        billing_visitors
    )

    dwell_values = [

        e.get(
            "dwell_ms",
            0
        )

        for e in store_events

        if e.get(
            "event_type"
        ) == "ZONE_DWELL"
    ]

    avg_dwell_time = 0

    if dwell_values:

        avg_dwell_time = round(

            (
                sum(
                    dwell_values
                )
                /
                len(
                    dwell_values
                )
            )
            /
            1000,

            2
        )

    pos = load_pos()

    transactions = 0
    total_revenue = 0

    if not pos.empty:

        transactions = len(
            pos
        )

        for col in [

            "GMV",
            "NMV",
            "total_amount",
            "amount"
        ]:

            if col in pos.columns:

                total_revenue = float(

                    pos[col]
                    .fillna(0)
                    .sum()

                )

                break

    purchases = min(
        transactions,
        unique_visitors
    )

    conversion_rate = 0

    if unique_visitors > 0:

        conversion_rate = round(

            (
                purchases
                /
                unique_visitors
            )
            * 100,

            2
        )

    abandonment_rate = 0

    return {

        "store_id":
            store_id,

        "unique_visitors":
            unique_visitors,

        "entries":
            entries,

        "exits":
            exits,

        "zone_visits":
            zone_visits,

        "billing_count":
            queue_depth,

        "transactions":
            transactions,

        "total_revenue":
            round(
                total_revenue,
                2
            ),

        "conversion_rate":
            conversion_rate,

        "queue_depth":
            queue_depth,

        "abandonment_rate":
            abandonment_rate,

        "avg_dwell_time":
            avg_dwell_time
    }


if __name__ == "__main__":

    result = calculate_metrics(
        "STORE_BLR_001"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )