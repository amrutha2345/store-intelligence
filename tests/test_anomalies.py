"""
Validate anomaly detection.

Requirements:
1. Response should be a dictionary.
2. active_anomalies must exist.
3. active_anomalies must be a list.
4. Each anomaly should contain:
   - anomaly_type
   - severity
   - suggested_action
"""

from app.anomalies import (
    detect_anomalies
)


def test_response_type():

    result = detect_anomalies(
        "STORE_BLR_002"
    )

    assert isinstance(
        result,
        dict
    )


def test_store_id():

    result = detect_anomalies(
        "STORE_BLR_002"
    )

    assert (

        result[
            "store_id"
        ]

        ==

        "STORE_BLR_002"
    )


def test_active_anomalies_exists():

    result = detect_anomalies(
        "STORE_BLR_002"
    )

    assert (

        "active_anomalies"

        in

        result
    )


def test_active_anomalies_type():

    result = detect_anomalies(
        "STORE_BLR_002"
    )

    assert isinstance(

        result[
            "active_anomalies"
        ],

        list
    )


def test_total_anomalies_exists():

    result = detect_anomalies(
        "STORE_BLR_002"
    )

    assert (

        "total_anomalies"

        in

        result
    )


def test_anomaly_schema():

    result = detect_anomalies(
        "STORE_BLR_002"
    )

    for anomaly in result[
        "active_anomalies"
    ]:

        assert (
            "anomaly_type"
            in anomaly
        )

        assert (
            "severity"
            in anomaly
        )

        assert (
            "suggested_action"
            in anomaly
        )


def test_severity_values():

    result = detect_anomalies(
        "STORE_BLR_002"
    )

    allowed = [

        "LOW",

        "MEDIUM",

        "HIGH"
    ]

    for anomaly in result[
        "active_anomalies"
    ]:

        assert (

            anomaly[
                "severity"
            ]

            in

            allowed
        )


def test_total_anomalies_count():

    result = detect_anomalies(
        "STORE_BLR_002"
    )

    assert (

        result[
            "total_anomalies"
        ]

        ==

        len(
            result[
                "active_anomalies"
            ]
        )
    )