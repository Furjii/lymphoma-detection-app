import os
import json
from PIL import Image

def load_labels(json_path):
    """
    Load class labels from a JSON file.
    
    Args:
        json_path (str): Path to the JSON file containing class indices
        
    Returns:
        list: List of class labels
    """
    try:
        with open(json_path, 'r') as f:
            class_indices = json.load(f)
            # Convert indices to ordered list
            labels = [None] * len(class_indices)
            for cls, idx in class_indices.items():
                labels[idx] = cls
            return labels
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def get_class_info(label):
    """
    Get detailed information about each lymphoma class.
    
    Args:
        label (str): The predicted label
        
    Returns:
        dict: Information about the lymphoma class
    """
    class_info = {
        'CLL': {
            'full_name': 'Chronic Lymphocytic Leukemia',
            'description': 'CLL is a type of cancer that affects the blood and bone marrow. It is the most common type of leukemia in adults.',
            'characteristics': 'Small, mature-appearing lymphocytes in the peripheral blood, bone marrow, and lymphoid tissues.'
        },
        'FL': {
            'full_name': 'Follicular Lymphoma',
            'description': 'FL is a type of non-Hodgkin lymphoma that begins in the lymphatic system. It is typically a slow-growing or indolent form of lymphoma.',
            'characteristics': 'Abnormal growth of B cells in lymph nodes, resembling the normal structure of follicles.'
        },
        'MCL': {
            'full_name': 'Mantle Cell Lymphoma',
            'description': 'MCL is a rare type of B-cell non-Hodgkin lymphoma that affects the lymph nodes and other tissues. It is typically aggressive.',
            'characteristics': 'Malignant B cells from the mantle zone of the lymph node follicle.'
        }
    }
    
    return class_info.get(label, {
        'full_name': 'Unknown',
        'description': 'No information available for this class.',
        'characteristics': 'Not specified.'
    })

def clean_uploads(upload_folder, max_files=100):
    """
    Clean up old upload files if there are too many.
    
    Args:
        upload_folder (str): Path to the upload folder
        max_files (int): Maximum number of files to keep
    """
    files = [os.path.join(upload_folder, f) for f in os.listdir(upload_folder)]
    files.sort(key=os.path.getctime)
    
    if len(files) > max_files:
        for f in files[:-max_files]:
            try:
                os.remove(f)
            except:
                pass
