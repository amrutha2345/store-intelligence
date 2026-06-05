"""
Validate store metrics.

Requirements:
1. Response must be a dictionary.
2. store_id must exist.
3. unique_visitors must exist.
4. conversion_rate must exist.
5. avg_dwell_time must exist.
6. queue_depth must exist.
7. abandonment_rate must exist.
8. total_revenue must exist.
"""

from app.metrics import (
    calculate_metrics
)


def test_response_type():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert isinstance(
        result,
        dict
    )


def test_store_id_exists():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        "store_id"
        in result
    )


def test_store_id_value():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (

        result[
            "store_id"
        ]

        ==

        "STORE_BLR_002"
    )


def test_unique_visitors_exists():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        "unique_visitors"
        in result
    )


def test_conversion_rate_exists():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        "conversion_rate"
        in result
    )


def test_avg_dwell_time_exists():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        "avg_dwell_time"
        in result
    )


def test_queue_depth_exists():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        "queue_depth"
        in result
    )


def test_abandonment_rate_exists():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        "abandonment_rate"
        in result
    )


def test_total_revenue_exists():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        "total_revenue"
        in result
    )


def test_numeric_fields():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert isinstance(
        result[
            "unique_visitors"
        ],
        int
    )

    assert isinstance(
        result[
            "conversion_rate"
        ],
        (
            int,
            float
        )
    )

    assert isinstance(
        result[
            "avg_dwell_time"
        ],
        (
            int,
            float
        )
    )

    assert isinstance(
        result[
            "queue_depth"
        ],
        int
    )

    assert isinstance(
        result[
            "abandonment_rate"
        ],
        (
            int,
            float
        )
    )

    assert isinstance(
        result[
            "total_revenue"
        ],
        (
            int,
            float
        )
    )


def test_conversion_rate_non_negative():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        result[
            "conversion_rate"
        ] >= 0
    )


def test_revenue_non_negative():

    result = calculate_metrics(
        "STORE_BLR_002"
    )

    assert (
        result[
            "total_revenue"
        ] >= 0
    )