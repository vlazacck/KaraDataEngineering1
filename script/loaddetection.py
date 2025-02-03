import os
from pathlib import Path
import pandas as pd
import logging

def load_detection_results(output_dir: str) -> pd.DataFrame:
    """
    Loads detection results from YOLOv5 output files.
    """
    results = []
    labels_dir = Path(output_dir) / "results" / "results" / "labels"

    if not labels_dir.exists():
        logging.error(f"Labels directory does not exist: {labels_dir}")
        print(f"Error: Labels directory not found at {labels_dir}")
        return pd.DataFrame()

    logging.info(f"Loading detection results from {labels_dir}")

    # Iterate through all .txt files in the labels directory
    for file in labels_dir.rglob("*.txt"):
        file_name = file.stem  # Extract filename without extension
        logging.info(f"Processing file: {file}")

        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 6:  # Ensure the line has valid data (including confidence)
                    class_id, x_center, y_center, width, height, confidence = map(float, parts)

                    results.append({
                        "file_name": file_name,
                        "class_id": int(class_id),
                        "x_center": x_center,
                        "y_center": y_center,
                        "width": width,
                        "height": height,
                        "confidence": confidence
                    })

    # Convert the results to a Pandas DataFrame
    df = pd.DataFrame(results)
    logging.info(f"Loaded {len(df)} detection results.")
    return df

# Example usage
OUTPUT_DIR = "C:/Users/Hp/Videos/karaDataEngineering1/yolov5/detections"
df = load_detection_results(OUTPUT_DIR)

# Print the first few rows of the DataFrame
if not df.empty:
    print(df.head())
else:
    print("No detection results found.")