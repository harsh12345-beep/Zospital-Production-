import requests
import json
# Step 1: Fetch the CSRF token
session = requests.Session()
get_response = session.get("https://pres-api-ap55zon22q-uc.a.run.app")  # Adjust this URL to the one that provides the CSRF token

# Assuming the token is stored in a cookie named 'csrftoken'
csrf_token = session.cookies['csrftoken']
print(csrf_token)
# Step 2: Make the POST request including the CSRF token
url = "https://pres-api-ap55zon22q-uc.a.run.app/api/create_pdf/"
headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrf_token  # Include the CSRF token in the headers
}
payload = {
    "patient_id": "35",
    "date": "2022-01-02",
    "name": "abhi",
    "address": "a ",
    "contact": "ik",
    "age": 3,
    "sex": "Male",
    "height": "1",
    "weight": "70kg",
    "bp": "120/80",
    "investigation": "fiver",
    "advice": "Take rest",
    "chief_complaints": "Fever headache",
    "examination_findings": "Normal",
    "diagnosis": "Viral Fever",
    "treatment_plan": "Medication",
    "medications": [
        {"name": "avvvvvvvvvvvvvvnf", "dosage": "afkjjjjjjjjjv", "instruction": "argkjjjjjjjjjjjjjjrgbet"},
        {"name": "fdbhnnnnnnnnnnnnnnnnnnnnnnnnneabet", "dosage": "dabevb"},  # No instruction
        {"name": "xyz"}  # No dosage, no instruction
    ],
    "next_date": "2024-07-15",
    "footer_address": "Bhamata "
}
response = session.post(url, json=payload, headers=headers)

print(response.status_code)
if response.status_code == 200:
    response_data = response.json()  # Get the response JSON
    if 'url' in response_data:
        gcs_url = response_data['url']
        print(f"URL: {gcs_url}")
    else:
        print("URL not found in the response")
else:
    print(f"Error: {response.status_code}")
    print(response.text)