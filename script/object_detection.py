import os
from pathlib import Path

# Define the path to detect.py
detect_script_path = Path("C:/Users/Hp/Videos/karaDataEngineering1/yolov5/detect.py")

# Dynamically load the detect function
if os.path.exists(detect_script_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("detect", detect_script_path)
    detect_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(detect_module)
    detect = detect_module.run  # Access the detect function
else:
    raise FileNotFoundError(f"Could not find {detect_script_path}")

# Use the detect function
detect(
    weights="yolov5s.pt",
    source="dataImages/images",
    project="detections",
    name="results",
    exist_ok=True
)
# Define paths
IMAGE_DIR = "yolov5/dataImages/images"  # Updated to point to the combined images folder
OUTPUT_DIR = "yolov5/detections"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Detect objects in images
def run_yolo_detection(image_dir, output_dir):
    """
    Runs YOLOv5 object detection on images in the specified directory.
    """
    # Call the YOLOv5 detection script
    detect.run(
        weights="yolov5s.pt",  # Pre-trained weights
        source=image_dir,
        project=output_dir,
        name="results",
        exist_ok=True
    )

# Example usage
run_yolo_detection(IMAGE_DIR, OUTPUT_DIR)