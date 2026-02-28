import requests
import sys

# Using Docker networking and port 8002 (as defined in their Dockerfile)
API_URL = "http://10.2.133.39:8002/predict" 

# FIXED PAYLOAD: Exactly matching the 9 features in WineFeatures BaseModel
valid_payload = {
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4
}

# Invalid payload to trigger 422 error
invalid_payload = {
    "volatile_acidity": "invalid_string", # Wrong data type
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4
}

def test_valid_request():
    print("--- Stage 4: Testing Valid Request ---")
    response = requests.post(API_URL, json=valid_payload)
    
    if response.status_code != 200:
        print(f"Failed: Expected status 200, got {response.status_code} - {response.text}")
        sys.exit(1)
        
    data = response.json()
    
    if "wine_quality" not in data: 
        print("Failed: 'wine_quality' field missing")
        sys.exit(1)
        
    if not isinstance(data["wine_quality"], (int, float, list)):
        print("Failed: Prediction is not numeric")
        sys.exit(1)
        
    print(f"Success! Prediction received: {data['wine_quality']}")

def test_invalid_request():
    print("--- Stage 5: Testing Invalid Request ---")
    response = requests.post(API_URL, json=invalid_payload)
    
    if response.status_code == 200:
        print("Failed: API should have returned an error for invalid input")
        sys.exit(1)
        
    print(f"Success! API correctly handled invalid input. Error: {response.status_code}")

if __name__ == "__main__":
    try:
        test_valid_request()
        test_invalid_request()
    except Exception as e:
        print(f"Exception occurred: {e}")
        sys.exit(1)