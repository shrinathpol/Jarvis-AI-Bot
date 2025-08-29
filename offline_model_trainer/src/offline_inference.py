import pickle
import numpy as np
import json
import os

def load_model(model_path):
    """Load the trained offline model from a pickle file."""
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def preprocess_input(input_data):
    """Preprocess the input data for prediction."""
    # Assuming input_data is a dictionary that needs to be converted to a numpy array
    # Modify this function based on the actual input format required by the model
    return np.array([list(input_data.values())])

def make_prediction(model, input_data):
    """Make a prediction using the trained offline model."""
    processed_data = preprocess_input(input_data)
    prediction = model.predict(processed_data)
    return prediction

def main(input_data, model_path='offline_model.pkl'):
    """Main function to load the model and make a prediction."""
    # This line gets the directory of the currently running script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # This line creates the path to the models directory
    model_dir = os.path.join(script_dir, 'models')
    
    # This line creates the full path to the model file
    full_model_path = os.path.join(model_dir, model_path)
    
    # You should also add a check to make sure the file exists
    if not os.path.exists(full_model_path):
        raise FileNotFoundError(f"Model file not found at: {full_model_path}")
        
    model = load_model(full_model_path)
    prediction = make_prediction(model, input_data)
    return prediction

# Example usage
if __name__ == "__main__":
    # Example input data, modify as needed
    example_input = {"feature1": 1.0, "feature2": 2.0}
    result = main(example_input)
    print("Prediction:", result)