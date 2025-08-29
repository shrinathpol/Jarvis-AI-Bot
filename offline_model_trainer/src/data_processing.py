import json
import os

def load_data(file_path):
    """Load JSON data from a specified file path."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def preprocess_data(data):
    """Preprocess the data for training or validation."""
    # Example preprocessing steps
    # 1. Remove duplicates
    # 2. Handle missing values
    # 3. Normalize or scale features if necessary
    # This is a placeholder for actual preprocessing logic
    processed_data = data  # Replace with actual processing
    return processed_data

def load_and_preprocess_training_data(training_data_path):
    """Load and preprocess the training data."""
    raw_data = load_data(training_data_path)
    return preprocess_data(raw_data)

def load_and_preprocess_validation_data(validation_data_path):
    """Load and preprocess the validation data."""
    raw_data = load_data(validation_data_path)
    return preprocess_data(raw_data)