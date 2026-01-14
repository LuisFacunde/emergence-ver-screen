import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_get_patient_files(patient_id):
    url = f"{BASE_URL}/patients/{patient_id}/files"
    print(f"Testing URL: {url}")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response JSON (first 2 items):")
            if 'data' in data:
                print(json.dumps(data['data'][:2], indent=2))
            else:
                print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

# Test with a dummy ID or one known to exist (trying '1' or '739' from previous context)
test_get_patient_files('739')
