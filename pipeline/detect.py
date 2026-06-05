import os
import json
from datetime import datetime, timezone

from ultralytics import YOLO

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

VIDEO_DIR = os.path.join(
    BASE_DIR,
    "data",
    "videos"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

DETECTIONS_FILE = os.path.join(
    OUTPUT_DIR,
    "detections.json"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

model = YOLO(
    "yolov8n.pt"
)


def get_store(video_path):

    path = video_path.lower()

    if "store 1" in path:
        return "STORE_BLR_001"

    if "store 2" in path:
        return "STORE_BLR_002"

    return "STORE_BLR_002"


def get_zone(video_name):

    name = video_name.lower()

    if "cam 1" in name:
        return "SKINCARE"

    if "cam 2" in name:
        return "MAKEUP"

    if "cam 5" in name:
        return "BILLING"

    if "billing" in name:
        return "BILLING"

    if "zone" in name:
        return "FRAGRANCE"

    return "UNKNOWN"


def get_camera(video_name):

    name = video_name.lower()

    if "cam 1" in name:
        return "CAM_ZONE_01"

    if "cam 2" in name:
        return "CAM_ZONE_02"

    if "cam 3" in name:
        return "CAM_ENTRY_01"

    if "cam 5" in name:
        return "CAM_BILLING_01"

    if "entry 1" in name:
        return "CAM_ENTRY_01"

    if "entry 2" in name:
        return "CAM_ENTRY_02"

    if "billing" in name:
        return "CAM_BILLING_01"

    return "CAM_UNKNOWN"


def find_all_videos():

    videos = []

    for root, dirs, files in os.walk(
        VIDEO_DIR
    ):

        for file in files:

            if file.lower().endswith(
                ".mp4"
            ):

                videos.append(

                    os.path.join(
                        root,
                        file
                    )
                )

    return videos


def main():

    detections = []

    video_files = find_all_videos()

    print(
        f"Found {len(video_files)} videos"
    )

    for video_path in video_files:

        video_name = os.path.basename(
            video_path
        )

        print(
            f"Processing {video_name}"
        )

        try:

            results = model.track(
                source=video_path,
                stream=True,
                persist=True,
                classes=[0],
                conf=0.25
            )

            frame_no = 0

            for result in results:

                frame_no += 1

                if (
                    result.boxes is None
                    or
                    result.boxes.id is None
                ):
                    continue

                for box, track_id, conf in zip(

                    result.boxes.xyxy,

                    result.boxes.id,

                    result.boxes.conf

                ):

                    x1, y1, x2, y2 = map(
                        int,
                        box
                    )

                    detections.append({

                        "track_id":
                            int(track_id),

                        "store_id":
                            get_store(
                                video_path
                            ),

                        "camera_id":
                            get_camera(
                                video_name
                            ),

                        "zone_id":
                            get_zone(
                                video_name
                            ),

                        "confidence":
                            round(
                                float(conf),
                                2
                            ),

                        "frame":
                            frame_no,

                        "timestamp":
                            datetime.now(
                                timezone.utc
                            ).isoformat(),

                        "dwell_ms":
                            5000,

                        "bbox": {

                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2
                        }
                    })

        except Exception as e:

            print(
                f"Error processing {video_name}: {e}"
            )

    with open(
        DETECTIONS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            detections,
            f,
            indent=4
        )

    print(
        f"Saved {len(detections)} detections"
    )

    print(
        f"Output: {DETECTIONS_FILE}"
    )


if __name__ == "__main__":
    main()
