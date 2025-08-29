import requests
import json

def fetch_online_predictions(data):
    """Fetch predictions from the online model."""
    url = "https://api.online-model.com/predict"  # Replace with actual online model API endpoint
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()  # Assuming the response is in JSON format
    else:
        raise Exception(f"Error fetching predictions: {response.status_code} - {response.text}")

def enhance_training_data(training_data, online_predictions):
    """Enhance the training data with predictions from the online model."""
    for i in range(len(training_data)):
        training_data[i]['online_prediction'] = online_predictions[i]
    return training_data

def get_enhanced_training_data(training_data):
    """Get enhanced training data by fetching online predictions."""
    online_predictions = fetch_online_predictions(training_data)
    enhanced_data = enhance_training_data(training_data, online_predictions)
    return enhanced_data