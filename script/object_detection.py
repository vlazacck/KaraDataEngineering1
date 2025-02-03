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

# Define paths
IMAGE_DIR = "C:/Users/Hp/Videos/karaDataEngineering1/yolov5/dataImage/images"  # Corrected path
OUTPUT_DIR = "C:/Users/Hp/Videos/karaDataEngineering1/yolov5/detections/results"  # Output folder
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)  # Create output folder if it doesn't exist

# Detect objects in images
def run_yolo_detection(image_dir, output_dir):
    """
    Runs YOLOv5 object detection on images in the specified directory.
    """
    # Call the YOLOv5 detection script
    detect(
         weights="yolov5s.pt",  # Pre-trained weights
        source=str(image_dir),  # Path to the folder containing images
        project=str(output_dir),  # Output folder for detection results
        name="results",  
        save_txt=True,  # Save results as .txt files
        exist_ok=True,  # Overwrite existing results
        save_conf=True  # Include confidence scores in .txt files
    )

# Example usage
run_yolo_detection(IMAGE_DIR, OUTPUT_DIR)