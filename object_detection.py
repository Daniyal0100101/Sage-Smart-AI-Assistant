import contextlib
import io
import torch

def load_model_silently(model_path):
    """Load the YOLOv5 model for object detection silently."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
            return model
        except Exception as e:
            print(f"Error loading YOLOv5 model: {e}")
            return None

model_path = ' Explain_Add_pyolov5s.pt_path'
model = load_model_silently(model_path)
